"""
Ice Engine — Daily Data Pull
=============================
This is the real automation piece: a script meant to run once a day (via
GitHub Actions — see .github/workflows/daily.yml) that pulls actual NHL
data, writes it to a structured JSON file the Props Board can read, and
upserts it into Supabase.

Data source: api-web.nhle.com — the NHL's own public API. No API key, no
account, no cost. It's the same feed NHL.com's website itself uses. It is
NOT officially documented by the NHL, but it's stable and widely used by
hobby projects; the endpoint shapes below match the community reference at
https://github.com/Zmalski/NHL-API-Reference

WHAT THIS SCRIPT DOES, in order:
  1. Pulls today's full schedule (which teams play, when).
  2. For each team playing today, pulls their current roster.
  3. For each rostered player, pulls their season game log (every game
     played this season, with opponent, date, and stat line) — this is
     exactly what feeds the Gamelog table and the real Head-to-Head filter
     in the Props Board.
  4. Pulls every game of the season with its final score (for team goals
     for/against).
  5. Reads the play-by-play of each completed game in those game logs and
     counts every player's shot attempts (shots on goal + missed + blocked).
  6. Writes everything to daily_data.json in a shape the Props Board's
     JavaScript can load directly.
  7. If SUPABASE_URL and SUPABASE_KEY are set, upserts the same data
     into the players / games / player_game_logs tables (supabase/schema.sql).

WHAT THIS SCRIPT DOES NOT DO YET:
  - Multi-season history. NHL's game-log endpoint gives you ONE season at a
    time. To get "several seasons back" for H2H, run this once per past
    season too (a backfill), not just daily — see the BACKFILL section near
    the bottom.
  - Injuries/scratches: the schedule endpoint doesn't reliably include these.
    That still needs the "lineup projections" article approach we used by
    hand, or a separate source — flagged as a known gap, not silently
    ignored.

Verified end-to-end against the live API on 2026-10-08.
"""

import argparse
import json
import os
import socket
import sys
import time
import urllib.request
import urllib.error
from datetime import date, datetime, timedelta, timezone

BASE = "https://api-web.nhle.com/v1"
OUT_FILE = "daily_data.json"

# All 32 team abbreviations as used by the NHL API
ALL_TEAMS = [
    "ANA","BOS","BUF","CAR","CBJ","CGY","CHI","COL","DAL","DET","EDM","FLA",
    "LAK","MIN","MTL","NJD","NSH","NYI","NYR","OTT","PHI","PIT","SEA","SJS",
    "STL","TBL","TOR","UTA","VAN","VGK","WPG","WSH"
]

GAME_TYPE_REGULAR = "2"       # 1=preseason, 2=regular, 3=playoffs
GAME_TYPE_PLAYOFFS = "3"
FINAL_STATES = ("OFF", "FINAL")  # FINAL = just ended, OFF = stats made official

# Play-by-play events that count as a shot attempt, and the field naming the
# shooter on each. A goal is a shot on goal too, but is logged as its own event.
SHOT_ATTEMPT_EVENTS = {
    "goal": "scoringPlayerId",
    "shot-on-goal": "shootingPlayerId",
    "missed-shot": "shootingPlayerId",
    "blocked-shot": "shootingPlayerId",
}

# Supabase credentials come from the environment (GitHub Actions secrets in
# CI). The service key bypasses row-level security, so it must never be
# committed or shipped to the browser.
SUPABASE_URL = os.environ.get("SUPABASE_URL", "").strip().rstrip("/")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "").strip()  # pasted secrets often carry a newline

# URLs that still failed after all retries. A failed fetch is otherwise
# indistinguishable from "no games played", so we track them and exit
# non-zero at the end — that turns the scheduled run red instead of quietly
# saving partial data.
FAILED_URLS = []


def nhl_today():
    """Today's date on the NHL's calendar (US Eastern), not the machine's.
    GitHub Actions runners are on UTC, where a late-evening run would
    otherwise already be asking for tomorrow's schedule."""
    try:
        from zoneinfo import ZoneInfo
        tz = ZoneInfo("America/New_York")
    except Exception:
        # No tz database (e.g. Windows without the tzdata package) — fixed
        # EST offset is only wrong for one hour a night during daylight time.
        tz = timezone(timedelta(hours=-5))
    return datetime.now(tz).date()


def season_for(day):
    """NHL seasons are coded as startyear+endyear, e.g. '20262027'. Seasons
    start in September/October, so anything before September belongs to the
    season that started the previous year."""
    start = day.year if day.month >= 9 else day.year - 1
    return f"{start}{start + 1}"


def fetch_json(url, retries=3, pause=1.0):
    """GET a URL and parse JSON, with basic retry since a daily job that dies
    on one flaky request isn't good enough to trust unattended."""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "IceEngine/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            print(f"  [warn] {url} failed (attempt {attempt+1}/{retries}): {e}")
            if e.code == 404:
                break  # a missing resource won't appear on retry
            time.sleep(pause * (attempt + 1))
        except (urllib.error.URLError, socket.timeout, TimeoutError, ValueError) as e:
            print(f"  [warn] {url} failed (attempt {attempt+1}/{retries}): {e}")
            time.sleep(pause * (attempt + 1))
    print(f"  [error] giving up on {url}")
    FAILED_URLS.append(url)
    return None


def get_todays_schedule(day=None):
    """Real games being played today, with team names and start times."""
    today_str = (day or nhl_today()).isoformat()
    data = fetch_json(f"{BASE}/schedule/{today_str}")
    if not data:
        return []
    games = []
    for d in data.get("gameWeek", []):
        if d.get("date") != today_str:
            continue
        for g in d.get("games", []):
            games.append({
                "gameId": g.get("id"),
                "date": today_str,
                "gameType": g.get("gameType"),
                "away": g.get("awayTeam", {}).get("abbrev"),
                "home": g.get("homeTeam", {}).get("abbrev"),
                "startTimeUTC": g.get("startTimeUTC"),
            })
    return games


def get_roster(team_abbrev):
    """Current roster for a team — real names, positions, sweater numbers.
    This alone replaces most of the manual roster-building work from the
    rest of this project, going forward."""
    data = fetch_json(f"{BASE}/roster/{team_abbrev}/current")
    if not data:
        return []
    players = []
    for group in ("forwards", "defensemen", "goalies"):
        for p in data.get(group, []):
            players.append({
                "id": p.get("id"),
                "name": f"{p['firstName']['default']} {p['lastName']['default']}",
                "team": team_abbrev,
                "number": p.get("sweaterNumber"),
                "pos": p.get("positionCode"),
            })
    return players


def get_player_game_log(player_id, season=None, game_type=GAME_TYPE_REGULAR, goalie=False):
    """Every game this player has played this season: date, opponent, goals,
    assists, shots on goal. This is the real version of the Gamelog table —
    each row here is a real completed game, not a generated one.

    Goalies get a different stat line from the API (no shots/points; saves
    data instead), so pass goalie=True to keep those fields."""
    season = season or season_for(nhl_today())
    data = fetch_json(f"{BASE}/player/{player_id}/game-log/{season}/{game_type}")
    if not data:
        return []
    log = []
    for g in data.get("gameLog", []):
        row = {
            "gameId": g.get("gameId"),
            "season": int(season),
            "gameType": int(game_type),
            "date": g.get("gameDate"),
            "team": g.get("teamAbbrev"),
            "opponent": g.get("opponentAbbrev"),
            "homeRoad": g.get("homeRoadFlag"),
            "goals": g.get("goals"),
            "assists": g.get("assists"),
            "points": g.get("points"),
            "sog": g.get("shots"),
            "toi": g.get("toi"),
        }
        if goalie:
            row.update({
                "points": (g.get("goals") or 0) + (g.get("assists") or 0),
                "gamesStarted": g.get("gamesStarted"),
                "decision": g.get("decision"),
                "shotsAgainst": g.get("shotsAgainst"),
                "goalsAgainst": g.get("goalsAgainst"),
                "savePctg": g.get("savePctg"),
            })
        log.append(row)
    return log


def get_season_games(season, sleep_between=0.3):
    """Every regular-season and playoff game of a season, with the final
    score once it has been played. One request per team; each game shows up
    on both teams' schedules, so they're merged by game id.

    Note for goals for/against: a shootout win is recorded by the NHL as one
    extra goal for the winner, and lastPeriodType ('REG', 'OT', 'SO') says
    which games those are."""
    games = {}
    for team in ALL_TEAMS:
        data = fetch_json(f"{BASE}/club-schedule-season/{team}/{season}")
        for g in (data or {}).get("games", []):
            if str(g.get("gameType")) not in (GAME_TYPE_REGULAR, GAME_TYPE_PLAYOFFS):
                continue
            final = g.get("gameState") in FINAL_STATES  # a live score isn't a final score
            games[g["id"]] = {
                "gameId": g["id"],
                "season": int(season),
                "date": g.get("gameDate"),
                "gameType": g.get("gameType"),
                "gameState": g.get("gameState"),
                "away": g.get("awayTeam", {}).get("abbrev"),
                "home": g.get("homeTeam", {}).get("abbrev"),
                "startTimeUTC": g.get("startTimeUTC"),
                "awayScore": g.get("awayTeam", {}).get("score") if final else None,
                "homeScore": g.get("homeTeam", {}).get("score") if final else None,
                "lastPeriodType": g.get("gameOutcome", {}).get("lastPeriodType") if final else None,
            }
        time.sleep(sleep_between)
    return sorted(games.values(), key=lambda g: (g["date"], g["gameId"]))


def get_game_shot_attempts(game_id):
    """Shot attempts per player for one game, from its play-by-play:
    {player_id: attempts}. An attempt is a goal, a shot on goal, a missed
    shot or a shot that was blocked, credited to the shooter. Shootout
    attempts are left out, the same way the NHL leaves them out of shots on
    goal. Returns None if the game isn't final yet (or the fetch failed), so
    the caller leaves it blank and a later run picks it up."""
    data = fetch_json(f"{BASE}/gamecenter/{game_id}/play-by-play")
    if not data or data.get("gameState") not in FINAL_STATES:
        return None
    attempts = {}
    for play in data.get("plays", []):
        shooter_field = SHOT_ATTEMPT_EVENTS.get(play.get("typeDescKey"))
        if not shooter_field or play.get("periodDescriptor", {}).get("periodType") == "SO":
            continue
        shooter = play.get("details", {}).get(shooter_field)
        if shooter:
            attempts[shooter] = attempts.get(shooter, 0) + 1
    return attempts


def add_shot_attempts(output, only=None, sleep_between=0.3):
    """Fill in 'shotAttempts' on gamelog rows, one play-by-play request per
    game. only=None does every game in the pulled gamelogs; pass a set of
    (player_id, game_id) pairs to limit it to rows that still need a value —
    a full season is ~1,300 games, far too many to re-read every day."""
    rows_by_game = {}
    for team_data in output["teams"].values():
        for p in team_data["roster"]:
            for g in p.get("gamelog", []):
                if only is None or (p["id"], g["gameId"]) in only:
                    rows_by_game.setdefault(g["gameId"], []).append((p["id"], g))

    print(f"Shot attempts: reading play-by-play for {len(rows_by_game)} game(s) ...")
    filled = 0
    for game_id in sorted(rows_by_game):
        attempts = get_game_shot_attempts(game_id)
        if attempts is not None:
            for player_id, g in rows_by_game[game_id]:
                g["shotAttempts"] = attempts.get(player_id, 0)  # played, never shot
                filled += 1
        time.sleep(sleep_between)
    print(f"  {filled} gamelog row(s) filled in")


def write_output(output, out_file=OUT_FILE):
    with open(out_file, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Wrote {out_file}")


def run_daily_pull(teams=None, include_gamelogs=True, sleep_between=0.3,
                   day=None, season=None, out_file=OUT_FILE):
    """The main job. teams=None means 'every team playing today' — pass an
    explicit list (e.g. ["BUF","CBJ"]) to limit scope while testing, since a
    full 32-team, full-roster gamelog pull is a lot of requests."""
    day = day or nhl_today()
    season = season or season_for(day)
    pulled_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    print(f"Ice Engine daily pull — {pulled_at} (NHL date {day}, season {season})")

    schedule = get_todays_schedule(day)
    print(f"Found {len(schedule)} game(s) today.")

    if teams is None:
        teams = sorted({g["away"] for g in schedule} | {g["home"] for g in schedule})
        if not teams:
            print("No games today — pulling rosters/gamelogs for ALL 32 teams instead.")
            teams = ALL_TEAMS

    # Regular season always; playoffs too once playoff games are on the slate,
    # otherwise the gamelogs would silently stop growing in April.
    game_types = [GAME_TYPE_REGULAR]
    if any(g["gameType"] == int(GAME_TYPE_PLAYOFFS) for g in schedule):
        game_types.append(GAME_TYPE_PLAYOFFS)

    output = {"pulledAt": pulled_at, "date": day.isoformat(), "season": season,
              "schedule": schedule, "teams": {}}

    for team in teams:
        print(f"Team {team} ...")
        roster = get_roster(team)
        print(f"  {len(roster)} players")
        team_data = {"roster": roster}

        if include_gamelogs:
            for p in roster:
                p["gamelog"] = []
                for game_type in game_types:
                    p["gamelog"] += get_player_game_log(
                        p["id"], season=season, game_type=game_type, goalie=(p["pos"] == "G"))
                    time.sleep(sleep_between)  # be a reasonable neighbor to a free, unofficial API
            print(f"  {sum(len(p['gamelog']) for p in roster)} gamelog rows")

        team_data["roster"] = roster
        output["teams"][team] = team_data

    print("Season games and final scores ...")
    output["games"] = get_season_games(season, sleep_between)
    played = sum(1 for g in output["games"] if g["homeScore"] is not None)
    print(f"  {len(output['games'])} games, {played} with a final score")

    write_output(output, out_file)
    return output


# ---------------------------------------------------------------------------
# SUPABASE — upsert the pull into Postgres through Supabase's REST API
# (PostgREST). Plain urllib, so the job has no dependencies to install.
# Every write is an upsert on the table's primary key, so re-running a day,
# or re-pulling a whole season, never creates duplicate rows.
# ---------------------------------------------------------------------------
def supabase_request(method, path, rows=None, prefer=None):
    """One call to Supabase's REST API; returns the parsed JSON body, if any.
    Exits non-zero on failure — a job that can't save its results should
    fail loudly."""
    url = f"{SUPABASE_URL}/rest/v1/{path}"
    headers = {"apikey": SUPABASE_KEY, "User-Agent": "IceEngine/1.0"}
    # Legacy service_role keys are JWTs and go in Authorization too. The new
    # sb_secret_/sb_publishable_ keys are not JWTs: they belong in apikey only.
    if not SUPABASE_KEY.startswith("sb_"):
        headers["Authorization"] = f"Bearer {SUPABASE_KEY}"
    if prefer:
        headers["Prefer"] = prefer
    body = None
    if rows is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(rows).encode("utf-8")

    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            text = resp.read().decode("utf-8")
            return json.loads(text) if text else None
    except urllib.error.HTTPError as e:
        # Print Supabase's own response body: it names the actual cause
        # (bad key, missing table, unknown column, RLS, ...).
        detail = e.read().decode("utf-8", "replace")
        print(f"  [error] Supabase request failed: HTTP {e.code} {e.reason}", flush=True)
        print(f"  [error] {method} {url}", flush=True)
        print(f"  [error] response body: {detail or '(empty)'}", flush=True)
        sys.exit(1)
    except (urllib.error.URLError, socket.timeout, TimeoutError) as e:
        print(f"  [error] Supabase request failed: could not reach {url}: {e}", flush=True)
        sys.exit(1)


def supabase_upsert(table, rows, on_conflict, batch_size=500):
    """POST rows to a table, merging on the conflict key."""
    for i in range(0, len(rows), batch_size):
        supabase_request("POST", f"{table}?on_conflict={on_conflict}", rows[i:i + batch_size],
                         prefer="resolution=merge-duplicates,return=minimal")
    print(f"  {table}: upserted {len(rows)} row(s)")


def supabase_rows_missing_shot_attempts(season, page_size=1000):
    """(player_id, game_id) of every saved gamelog row of a season that has
    no shot attempts yet. Paged, because Supabase returns at most 1,000 rows
    per request."""
    missing, offset = set(), 0
    while True:
        rows = supabase_request(
            "GET", "player_game_logs?select=player_id,game_id&shot_attempts=is.null"
                   f"&season=eq.{season}&order=player_id,game_id&limit={page_size}&offset={offset}")
        missing.update((r["player_id"], r["game_id"]) for r in rows or [])
        if not rows or len(rows) < page_size:
            return missing
        offset += page_size


def build_supabase_rows(output):
    """Flatten the nested JSON output into one list of rows per table. Rows
    in a batch must all have the same keys, so skater rows carry the goalie
    columns as null and vice versa.

    Gamelog rows come back as two lists: every row WITHOUT the shot_attempts
    column (so re-saving a row never wipes a value stored on an earlier
    day), and the rows whose shot attempts were counted in this run WITH it."""
    pulled_at = output["pulledAt"]

    # Today's slate is normally part of the season list already; it's the
    # fallback if that list couldn't be fetched.
    season_games = {g["gameId"]: g for g in output["schedule"]}
    season_games.update({g["gameId"]: g for g in output.get("games", [])})
    games = [{
        "id": g["gameId"],
        "season": g.get("season", int(output["season"])),
        "game_date": g["date"],
        "game_type": g["gameType"],
        "game_state": g.get("gameState"),
        "away": g["away"],
        "home": g["home"],
        "start_time_utc": g["startTimeUTC"],
        "away_score": g.get("awayScore"),
        "home_score": g.get("homeScore"),
        "last_period_type": g.get("lastPeriodType"),
        "updated_at": pulled_at,
    } for g in season_games.values()]

    players, logs, logs_with_attempts = [], [], []
    for team_data in output["teams"].values():
        for p in team_data["roster"]:
            players.append({
                "id": p["id"],
                "name": p["name"],
                "team": p["team"],
                "number": p["number"],
                "pos": p["pos"],
                "updated_at": pulled_at,
            })
            for g in p.get("gamelog", []):
                logs.append({
                    "player_id": p["id"],
                    "game_id": g["gameId"],
                    "season": g["season"],
                    "game_type": g["gameType"],
                    "game_date": g["date"],
                    "team": g["team"],
                    "opponent": g["opponent"],
                    "home_road": g["homeRoad"],
                    "goals": g["goals"],
                    "assists": g["assists"],
                    "points": g["points"],
                    "sog": g["sog"],
                    "toi": g["toi"],
                    "games_started": g.get("gamesStarted"),
                    "decision": g.get("decision"),
                    "shots_against": g.get("shotsAgainst"),
                    "goals_against": g.get("goalsAgainst"),
                    "save_pct": g.get("savePctg"),
                    "updated_at": pulled_at,
                })
                if g.get("shotAttempts") is not None:
                    logs_with_attempts.append(dict(logs[-1], shot_attempts=g["shotAttempts"]))
    return games, players, logs, logs_with_attempts


def save_to_supabase(output):
    games, players, logs, _ = build_supabase_rows(output)
    print(f"Saving to Supabase ({SUPABASE_URL}) ...")
    supabase_upsert("games", games, "id")
    supabase_upsert("players", players, "id")  # before logs: logs reference players
    supabase_upsert("player_game_logs", logs, "player_id,game_id")


def save_shot_attempts_to_supabase(output):
    logs_with_attempts = build_supabase_rows(output)[3]
    print("Saving shot attempts to Supabase ...")
    supabase_upsert("player_game_logs", logs_with_attempts, "player_id,game_id")


# ---------------------------------------------------------------------------
# BACKFILL — run this ONCE (not daily) per past season you want real H2H
# history for. This is what actually gives the Head-to-Head filter multiple
# seasons of real meetings instead of generated placeholder ones.
#
# To backfill straight into Supabase instead of a local file, run the pull
# with a past season:  python ice_engine_daily_pull.py --teams ALL --season 20252026
# (or use "Run workflow" on the GitHub Actions tab with those inputs).
# ---------------------------------------------------------------------------
def backfill_season(season_code, teams=None):
    """e.g. backfill_season('20242025') for last season's full history."""
    teams = teams or ALL_TEAMS
    output = {"season": season_code, "teams": {}}
    for team in teams:
        roster = get_roster(team)  # note: current roster, not that season's — a real
                                    # backfill should use that season's roster endpoint
        for p in roster:
            p["gamelog"] = get_player_game_log(p["id"], season=season_code, goalie=(p["pos"] == "G"))
            time.sleep(0.3)
        output["teams"][team] = {"roster": roster}
    with open(f"season_{season_code}.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"Backfilled {season_code}")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Pull NHL schedule, rosters and gamelogs.")
    parser.add_argument("--teams", default="",
                        help="comma-separated abbreviations (e.g. BUF,CBJ) or ALL; "
                             "default is every team playing today")
    parser.add_argument("--date", default="",
                        help="schedule date as YYYY-MM-DD; default is today (US Eastern)")
    parser.add_argument("--season", default="",
                        help="season code for gamelogs, e.g. 20252026; default is the current season")
    parser.add_argument("--no-gamelogs", action="store_true", help="rosters and schedule only")
    parser.add_argument("--no-shot-attempts", action="store_true",
                        help="skip the play-by-play requests that count shot attempts")
    parser.add_argument("--require-supabase", action="store_true",
                        help="fail if the Supabase env vars are missing instead of skipping the upload")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    teams = None
    if args.teams.strip().upper() == "ALL":
        teams = ALL_TEAMS
    elif args.teams.strip():
        teams = [t.strip().upper() for t in args.teams.split(",") if t.strip()]
        unknown = sorted(set(teams) - set(ALL_TEAMS))
        if unknown:
            sys.exit(f"Unknown team abbreviation(s): {', '.join(unknown)}")

    supabase_ready = bool(SUPABASE_URL and SUPABASE_KEY)
    if args.require_supabase and not supabase_ready:
        sys.exit("SUPABASE_URL and SUPABASE_KEY must be set (see README).")

    output = run_daily_pull(
        teams=teams,
        include_gamelogs=not args.no_gamelogs,
        day=date.fromisoformat(args.date) if args.date.strip() else None,
        season=args.season.strip() or None,
    )

    if supabase_ready:
        save_to_supabase(output)
    else:
        print("Supabase env vars not set — skipping upload.")

    if not (args.no_gamelogs or args.no_shot_attempts):
        # With Supabase, only read play-by-play for rows that have no value
        # saved yet (normally just last night's games). Without it there's
        # nothing to compare against, so every game in the gamelogs is read.
        only = supabase_rows_missing_shot_attempts(output["season"]) if supabase_ready else None
        add_shot_attempts(output, only)
        write_output(output)
        if supabase_ready:
            save_shot_attempts_to_supabase(output)

    if FAILED_URLS:
        sys.exit(f"{len(FAILED_URLS)} NHL API request(s) failed; saved data is incomplete.")


if __name__ == "__main__":
    main()
