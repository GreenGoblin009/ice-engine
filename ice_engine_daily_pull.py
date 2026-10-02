"""
Ice Engine — Daily Data Pull
=============================
This is the real automation piece: a script meant to run once a day (via a
scheduler — see the bottom of this file for options) that pulls actual NHL
data and writes it to a structured JSON file the Props Board can read.

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
  4. Writes everything to daily_data.json in a shape the Props Board's
     JavaScript can load directly.

WHAT THIS SCRIPT DOES NOT DO YET:
  - Multi-season history. NHL's game-log endpoint gives you ONE season at a
    time (param below). To get "several seasons back" for H2H, this needs
    to run once per past season too (a backfill), not just daily — see the
    BACKFILL section near the bottom.
  - Shot-on-goal totals are included per-game (the 'sog' field) since the
    real API provides them — this finally makes Shots real everywhere, not
    just Buffalo/Columbus.
  - Injuries/scratches: the schedule endpoint doesn't reliably include these.
    That still needs the "lineup projections" article approach we used by
    hand, or a separate source — flagged as a known gap, not silently
    ignored.

IMPORTANT — I have not been able to run this end-to-end myself: my sandbox
has no network access, so this is written correctly against the documented
endpoint shapes but hasn't been execution-tested against the live API. Treat
the first run as a debugging pass, not a guaranteed clean run.
"""

import json
import time
import urllib.request
import urllib.error
from datetime import date, datetime

BASE = "https://api-web.nhle.com/v1"
OUT_FILE = "daily_data.json"

# All 32 team abbreviations as used by the NHL API
ALL_TEAMS = [
    "ANA","BOS","BUF","CAR","CBJ","CGY","CHI","COL","DAL","DET","EDM","FLA",
    "LAK","MIN","MTL","NJD","NYI","NYR","OTT","PHI","PIT","SEA","SJS","STL",
    "TBL","TOR","UTA","VAN","VGK","WPG","WSH"
]

CURRENT_SEASON = "20262027"   # NHL seasons are coded as startyear+endyear
GAME_TYPE_REGULAR = "2"       # 1=preseason, 2=regular, 3=playoffs


def fetch_json(url, retries=3, pause=1.0):
    """GET a URL and parse JSON, with basic retry since a daily job that dies
    on one flaky request isn't good enough to trust unattended."""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "IceEngine/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            print(f"  [warn] {url} failed (attempt {attempt+1}/{retries}): {e}")
            time.sleep(pause)
    print(f"  [error] giving up on {url}")
    return None


def get_todays_schedule():
    """Real games being played today, with team names and start times."""
    today_str = date.today().isoformat()
    data = fetch_json(f"{BASE}/schedule/{today_str}")
    if not data:
        return []
    games = []
    for day in data.get("gameWeek", []):
        if day.get("date") != today_str:
            continue
        for g in day.get("games", []):
            games.append({
                "gameId": g.get("id"),
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


def get_player_game_log(player_id, season=CURRENT_SEASON, game_type=GAME_TYPE_REGULAR):
    """Every game this player has played this season: date, opponent, goals,
    assists, shots on goal. This is the real version of the Gamelog table —
    each row here is a real completed game, not a generated one."""
    data = fetch_json(f"{BASE}/player/{player_id}/game-log/{season}/{game_type}")
    if not data:
        return []
    log = []
    for g in data.get("gameLog", []):
        log.append({
            "date": g.get("gameDate"),
            "opponent": g.get("opponentAbbrev"),
            "homeRoad": g.get("homeRoadFlag"),
            "goals": g.get("goals"),
            "assists": g.get("assists"),
            "points": g.get("points"),
            "sog": g.get("shots"),
            "toi": g.get("toi"),
        })
    return log


def run_daily_pull(teams=None, include_gamelogs=True, sleep_between=0.3):
    """The main job. teams=None means 'every team playing today' — pass an
    explicit list (e.g. ["BUF","CBJ"]) to limit scope while testing, since a
    full 32-team, full-roster gamelog pull is a lot of requests."""
    print(f"Ice Engine daily pull — {datetime.now().isoformat()}")

    schedule = get_todays_schedule()
    print(f"Found {len(schedule)} game(s) today.")

    if teams is None:
        teams = sorted({g["away"] for g in schedule} | {g["home"] for g in schedule})
        if not teams:
            print("No games today — pulling rosters/gamelogs for ALL 32 teams instead.")
            teams = ALL_TEAMS

    output = {"pulledAt": datetime.now().isoformat(), "schedule": schedule, "teams": {}}

    for team in teams:
        print(f"Team {team} ...")
        roster = get_roster(team)
        print(f"  {len(roster)} players")
        team_data = {"roster": roster}

        if include_gamelogs:
            for p in roster:
                p["gamelog"] = get_player_game_log(p["id"])
                time.sleep(sleep_between)  # be a reasonable neighbor to a free, unofficial API

        team_data["roster"] = roster
        output["teams"][team] = team_data

    with open(OUT_FILE, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Wrote {OUT_FILE}")
    return output


# ---------------------------------------------------------------------------
# BACKFILL — run this ONCE (not daily) per past season you want real H2H
# history for. This is what actually gives the Head-to-Head filter multiple
# seasons of real meetings instead of generated placeholder ones.
# ---------------------------------------------------------------------------
def backfill_season(season_code, teams=None):
    """e.g. backfill_season('20242025') for last season's full history."""
    teams = teams or ALL_TEAMS
    output = {"season": season_code, "teams": {}}
    for team in teams:
        roster = get_roster(team)  # note: current roster, not that season's — a real
                                    # backfill should use that season's roster endpoint
        for p in roster:
            p["gamelog"] = get_player_game_log(p["id"], season=season_code)
            time.sleep(0.3)
        output["teams"][team] = {"roster": roster}
    with open(f"season_{season_code}.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"Backfilled {season_code}")


if __name__ == "__main__":
    # Quick manual test run — limit to Buffalo + Columbus first rather than
    # all 32 teams, since this hasn't been verified against the live API yet.
    run_daily_pull(teams=["BUF", "CBJ"])


# ---------------------------------------------------------------------------
# HOW TO ACTUALLY RUN THIS ON A SCHEDULE (pick one — all are free):
#
# 1. GitHub Actions (easiest, zero cost, no server to maintain):
#    - Put this script in a GitHub repo.
#    - Add .github/workflows/daily.yml with a `schedule: cron: '0 12 * * *'`
#      trigger (runs once a day) that runs `python ice_engine_daily_pull.py`
#      and commits daily_data.json back to the repo.
#    - The Props Board can then fetch the raw JSON straight from GitHub.
#
# 2. A free-tier cloud scheduler (Render, Railway, Fly.io cron jobs) —
#    similar idea, slightly more setup, more control.
#
# 3. Run it manually each morning on your own computer — works, but isn't
#    really "automatic," which defeats the point.
#
# This part — writing the workflow file, wiring it to actually run, and
# debugging the first live execution — is real software engineering, not
# research. It's a better fit for Claude Code than for this chat.
# ---------------------------------------------------------------------------
