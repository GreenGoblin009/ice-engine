"""
Ice Engine — Daily Player Odds
===============================
Pulls player-prop prices for today's NHL games from The Odds API
(the-odds-api.com) and saves every bookmaker's price to the player_odds
table in Supabase (supabase/player_odds.sql).

WHAT IT DOES, in order:
  1. Lists today's NHL events. This call is free and also reports how many
     credits are left; with fewer than MIN_CREDITS the run stops there.
  2. For each game that hasn't started yet, asks for the MARKETS below from
     US bookmakers — one call per game. This is the part that costs credits:
     1 per market that comes back, so 3 per game with three markets.
  3. Matches each player name to the players table: accents, punctuation
     and spelling variants ignored, the two teams in the game and tonight's
     saved lineup used to settle shared names. Rows it can't match are still
     saved, with an empty player_id.
  4. Upserts the rows, then removes that game's rows left over from an
     earlier run today (a book that moved a line from 0.5 to 1.5 would
     otherwise leave the old line behind).
  5. Prints credits used and credits left, then every priced name that
     still has no player id and why, and every shared name it had to settle.

THE KEY comes from the ODDS_API_KEY environment variable (a GitHub secret in
the workflow). It is never written to a file or printed. For a run on your
own PC, set that variable, or pass --clipboard to take it from the clipboard.

Games already under way are skipped on purpose: books pull player props at
puck drop, and the call would be paid for and come back nearly empty.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
import urllib.error
from datetime import date, datetime, timezone

import ice_engine_daily_pull as engine
from ice_engine_lineups import find_players, normalize

# Markets to pull. Add or remove keys here; each one costs 1 credit per game.
# Full list: https://the-odds-api.com/sports-odds-data/betting-markets.html
MARKETS = ["player_points", "player_assists", "player_goal_scorer_anytime"]
YES_NO_SIDES = {"Yes": "Over", "No": "Under"}  # how Yes/No markets are stored

REGIONS = "us"
MIN_CREDITS = 50      # stop before spending anything once fewer than this are left
ODDS_API = "https://api.the-odds-api.com/v4/sports/icehockey_nhl"
OUT_FILE = "daily_odds.json"
YEAR_HINT = re.compile(r"\s*\((\d{4})\)\s*$")  # "Elias Pettersson (2004)": a book's birth-year tag


class OddsError(Exception):
    """Something this job can't carry on from."""


def odds_api(path, key, **params):
    """GET an Odds API endpoint. Returns (body, headers). The key travels in
    the query string (the API's only option), so the URL is never printed."""
    url = f"{ODDS_API}{path}?" + urllib.parse.urlencode(dict(params, apiKey=key))
    req = urllib.request.Request(url, headers={"User-Agent": "IceEngine/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8")), resp.headers
    except urllib.error.HTTPError as e:
        try:
            message = json.loads(e.read().decode("utf-8")).get("message", e.reason)
        except ValueError:
            message = e.reason
        raise OddsError(f"Odds API {path.split('/')[1]} call failed: HTTP {e.code} — {message}") from None
    except (urllib.error.URLError, TimeoutError) as e:
        raise OddsError(f"could not reach the Odds API: {getattr(e, 'reason', e)}") from None


def key_from_clipboard():
    """The key, read from the Windows clipboard, for local runs. Only
    something shaped like an Odds API key (32 hex characters) is accepted."""
    text = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-Clipboard"],
                          capture_output=True, text=True).stdout.strip()
    if not re.fullmatch(r"[0-9a-fA-F]{32}", text):
        sys.exit("The clipboard doesn't hold an Odds API key (32 letters and digits). Copy just the key and retry.")
    return text


def team_abbreviations(day):
    """{normalized nickname: abbreviation} for the teams playing on a day,
    e.g. 'maple leafs' -> 'TOR'. The Odds API uses full names ('Toronto
    Maple Leafs', 'St Louis Blues'); the nickname at the end is the stable part."""
    data = engine.fetch_json(f"{engine.BASE}/schedule/{day.isoformat()}")
    nicknames = {}
    for d in (data or {}).get("gameWeek", []):
        if d.get("date") != day.isoformat():
            continue
        for g in d.get("games", []):
            for team in (g["awayTeam"], g["homeTeam"]):
                nicknames[normalize(team["commonName"]["default"])] = team["abbrev"]
    return nicknames


def abbreviation(full_name, nicknames):
    name = normalize(full_name)
    found = [abbr for nick, abbr in nicknames.items() if name == nick or name.endswith(" " + nick)]
    return found[0] if len(found) == 1 else None


def load_players(teams, use_supabase):
    """Every player to match names against: the Supabase players table, or
    without Supabase the NHL API rosters of the teams playing."""
    if use_supabase:
        players = engine.supabase_select_all("players?select=id,name,team,pos&order=id")
    else:
        players = [p for team in teams for p in engine.get_roster(team)]
    return [dict(p, key=normalize(p["name"])) for p in players]


def load_lineup(day, use_supabase):
    """Tonight's saved lineup rows (team, name, player id, status); empty
    when there is no Supabase or no lineup has been saved yet."""
    if not use_supabase:
        return []
    return engine.supabase_select_all(
        f"daily_lineups?select=team,player_name,player_id,status"
        f"&lineup_date=eq.{day.isoformat()}&order=team,list_order")


def birth_year(player, cache={}):
    """A player's birth year, from his team's NHL roster (one call per team,
    kept for the run). None if the roster doesn't list him."""
    team = player["team"]
    if team not in cache:
        data = engine.fetch_json(f"{engine.BASE}/roster/{team}/current") or {}
        cache[team] = {p["id"]: int(p["birthDate"][:4]) for group in data.values()
                       if isinstance(group, list) for p in group if p.get("birthDate")}
    return cache[team].get(player["id"])


def match_player(name, home, away, players, lineup=(), claimed=()):
    """(player_id, note) for a name in the odds feed. note is None for a
    plain match. With an id, it says how a name shared by several players
    was settled; without one, why the name has no player id.

    Looks among the two teams in the game first, then league-wide for a
    player whose team in the table is stale. A shared name is settled by the
    book's birth-year tag, then by who is in tonight's saved lineup, then by
    leaving out anyone in `claimed` (ids other names in this game matched)."""
    bare = YEAR_HINT.sub("", name)
    found = find_players(bare, [p for p in players if p["team"] in (home, away)])
    if not found:
        key = normalize(bare).replace(" ", "")
        found = [p for p in players if p["key"].replace(" ", "") == key]
    if len(found) == 1:
        return found[0]["id"], None
    if not found:
        listed = [l for l in lineup if l["team"] in (home, away) and normalize(l["player_name"]) == normalize(bare)]
        if listed:
            return None, (f"in tonight's {listed[0]['team']} lineup ({listed[0]['status']}) but not in the "
                          f"players table — the NHL roster feed doesn't list him")
        return None, "no player with this name on either team, or anywhere in the players table"

    shared = f"{len(found)} players share this name ({', '.join(sorted(p['team'] + ' ' + (p['pos'] or '?') for p in found))})"
    tag = YEAR_HINT.search(name)
    if tag:
        born = [p for p in found if birth_year(p) == int(tag.group(1))]
        if len(born) == 1:
            return born[0]["id"], f"{shared}; picked the {born[0]['pos']} born in {tag.group(1)}"
    in_lineup = {l["player_id"] for l in lineup if l["status"] == "projected"}
    dressed = [p for p in found if p["id"] in in_lineup]
    if len(dressed) == 1:
        return dressed[0]["id"], f"{shared}; picked the {dressed[0]['pos']}, the only one in tonight's lineup"
    if not dressed:
        return None, f"{shared} and none is in tonight's saved lineup"
    left = [p for p in dressed if p["id"] not in claimed]
    if len(left) == 1:
        return left[0]["id"], (f"{shared} and {len(dressed)} are dressed tonight; picked the {left[0]['pos']} "
                               f"because the other is priced under his own tagged name in this game")
    return None, f"{shared}, {len(dressed)} are dressed tonight and the feed doesn't say which one this is"


def rows_for_event(event, odds, day, home, away, players, pulled_at, unmatched, settled, lineup=()):
    """One row per price: player x market x line x side x bookmaker.
    unmatched and settled collect {name (game): reason} for the end-of-run report."""
    outcomes = [(book, market, o) for book in odds.get("bookmakers", []) for market in book.get("markets", [])
                if market["key"] in MARKETS for o in market.get("outcomes", [])
                if (o.get("description") or "").strip() and o.get("price") is not None]
    # Names carrying a birth-year tag first: what they match tells a plain
    # "Elias Pettersson" in the same game which of the two it must be.
    names = sorted({o["description"].strip() for _, _, o in outcomes}, key=lambda n: not YEAR_HINT.search(n))
    matched = {}
    for name in names:
        claimed = {player_id for player_id, _ in matched.values()}
        matched[name] = player_id, note = match_player(name, home, away, players, lineup, claimed)
        if note:
            (unmatched if player_id is None else settled)[f"{name} ({away} at {home})"] = note

    rows = {}
    for book, market, o in outcomes:
        name = o["description"].strip()
        # Yes/No markets (anytime goal scorer) come with no line: "Yes" to
        # scoring is the same bet as over 0.5 goals, and is stored that way.
        line = o["point"] if o.get("point") is not None else 0.5
        side = YES_NO_SIDES.get(o["name"], o["name"])
        row = {
            "game_date": day.isoformat(), "event_id": event["id"], "home": home, "away": away,
            "player_name": name, "player_id": matched[name][0], "market": market["key"],
            "line": line, "side": side, "book": book["title"],
            "price": int(round(o["price"])), "updated_at": pulled_at,
        }
        rows[(name, market["key"], line, side, book["title"])] = row  # one per primary key
    return list(rows.values())


def report_names(unmatched, settled):
    """The end-of-run list of every priced name without a player id, and of
    every shared name that had to be settled, each with the reason."""
    if settled:
        print(f"{len(settled)} shared name(s) settled:")
        for name in sorted(settled):
            print(f"  - {name}: {settled[name]}")
    if not unmatched:
        print("Every priced name was matched to a player.")
        return
    print(f"[warn] {len(unmatched)} priced name(s) saved with no player id:")
    for name in sorted(unmatched):
        print(f"  - {name}: {unmatched[name]}")


def save_to_supabase(rows, day, event_ids, pulled_at):
    print(f"Saving to Supabase ({engine.SUPABASE_URL}) ...")
    engine.supabase_upsert("player_odds", rows, "game_date,player_name,market,line,side,book")
    # Drop these games' rows from an earlier run today that this run didn't rewrite.
    engine.supabase_request(
        "DELETE", f"player_odds?game_date=eq.{day.isoformat()}"
                  f"&event_id=in.({','.join(event_ids)})&updated_at=lt.{pulled_at}")


def run(day, key, use_supabase, max_events=None):
    pulled_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    now = datetime.now(timezone.utc)
    tz = engine.nhl_timezone()
    print(f"Ice Engine odds — {pulled_at} (NHL date {day}); markets: {', '.join(MARKETS)}")

    events, headers = odds_api("/events", key)  # free
    left = int(float(headers.get("x-requests-remaining") or 0))
    start = lambda e: datetime.fromisoformat(e["commence_time"].replace("Z", "+00:00"))
    todays = sorted((e for e in events if start(e).astimezone(tz).date() == day), key=start)
    upcoming = [e for e in todays if start(e) > now]
    print(f"{len(todays)} game(s) listed for {day}; {len(upcoming)} not started yet. Credits left: {left}.")
    if left < MIN_CREDITS:
        raise OddsError(f"only {left} Odds API credits left (minimum {MIN_CREDITS}) — nothing was pulled")
    if not upcoming:
        print("Nothing to pull.")
        return
    if max_events:
        upcoming = upcoming[:max_events]

    nicknames = team_abbreviations(day)
    teams = {e["id"]: (abbreviation(e["home_team"], nicknames), abbreviation(e["away_team"], nicknames)) for e in upcoming}
    players = load_players(sorted({t for pair in teams.values() for t in pair if t}), use_supabase)
    lineup = load_lineup(day, use_supabase)

    rows, saved_events, unmatched, settled, problems, spent = [], [], {}, {}, [], 0
    for e in upcoming:
        home, away = teams[e["id"]]
        label = f"{e['away_team']} at {e['home_team']}"
        if not (home and away):
            problems.append(f"{label}: can't map the team names to NHL abbreviations")
            continue
        if left < MIN_CREDITS:
            problems.append(f"{label}: skipped, only {left} credits left")
            continue
        odds, headers = odds_api(f"/events/{e['id']}/odds", key, regions=REGIONS,
                                 markets=",".join(MARKETS), oddsFormat="american")
        cost = int(float(headers.get("x-requests-last") or 0))
        spent += cost
        left = int(float(headers.get("x-requests-remaining") or left))
        event_rows = rows_for_event(e, odds, day, home, away, players, pulled_at, unmatched, settled, lineup)
        books = sorted({r["book"] for r in event_rows})
        print(f"  {away} at {home}: {len(event_rows)} prices from {len(books)} book(s), {cost} credit(s)")
        rows += event_rows
        if event_rows:
            saved_events.append(e["id"])

    # The table's primary key has no game or team in it, so two players with
    # the same name on the same night would be the same row. Keep one (the
    # later game's) rather than have the whole save rejected.
    unique = {(r["player_name"], r["market"], r["line"], r["side"], r["book"]): r for r in rows}
    if len(unique) < len(rows):
        print(f"  [warn] {len(rows) - len(unique)} price(s) dropped: same player name, market, line, side "
              f"and book in two games")
        rows = list(unique.values())

    with open(OUT_FILE, "w") as f:
        json.dump({"pulledAt": pulled_at, "date": day.isoformat(), "odds": rows}, f, indent=2)
    print(f"Wrote {OUT_FILE} ({len(rows)} rows)")

    if use_supabase and rows:
        save_to_supabase(rows, day, saved_events, pulled_at)
    print(f"Credits: this run used {spent}; {left} left.")
    report_names(unmatched, settled)
    if problems:
        raise OddsError(f"{len(problems)} problem(s):\n  - " + "\n  - ".join(problems))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Save NHL player-prop odds to Supabase.")
    parser.add_argument("--date", default="", help="NHL date to pull, YYYY-MM-DD; default is today (US Eastern)")
    parser.add_argument("--max-events", type=int, default=0, help="only price this many games (for cheap tests)")
    parser.add_argument("--clipboard", action="store_true",
                        help="local runs: take the Odds API key from the clipboard instead of ODDS_API_KEY")
    parser.add_argument("--require-supabase", action="store_true",
                        help="fail if the Supabase env vars are missing instead of skipping the upload")
    parser.add_argument("--only-at", default="",
                        help="for scheduled runs: Eastern times to run at, e.g. '16:00'; other triggers "
                             "exit quietly (see SCHEDULE GATE in ice_engine_daily_pull.py)")
    args = parser.parse_args(argv)

    go, _, slot_day = engine.gate_on_schedule(args.only_at)
    if not go:
        return
    day = date.fromisoformat(args.date) if args.date.strip() else (slot_day or engine.nhl_today())

    key = key_from_clipboard() if args.clipboard else os.environ.get("ODDS_API_KEY", "").strip()
    if not key:
        sys.exit("ODDS_API_KEY is not set (add it as a GitHub secret, or use --clipboard on your own PC).")
    use_supabase = bool(engine.SUPABASE_URL and engine.SUPABASE_KEY)
    if args.require_supabase and not use_supabase:
        sys.exit("SUPABASE_URL and SUPABASE_KEY must be set.")
    if not use_supabase:
        print("Supabase env vars not set — matching against NHL API rosters and skipping the upload.")

    try:
        run(day, key, use_supabase, args.max_events or None)
    except OddsError as e:
        print(f"[error] {e}", flush=True)
        if os.environ.get("GITHUB_ACTIONS"):
            print(f"::error title=Odds pull failed::{str(e).splitlines()[0]}", flush=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
