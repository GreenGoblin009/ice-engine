"""
Ice Engine - Daily Player Odds from SportsGameOdds (FanDuel + DraftKings)
=========================================================================
Same job as ice_engine_odds.py, different source: pulls today's NHL player
props from SportsGameOdds and saves FanDuel and DraftKings prices to the
player_odds table, in exactly the shape the board and slate report already
read (markets player_points / player_assists / player_goal_scorer_anytime).

Cost: SportsGameOdds charges per game returned, not per market or book, so
one pull of today's not-yet-started games is cheap. Only games starting
between now and the end of today (US Eastern) are asked for.

Markets (SportsGameOdds name -> board market):
  goals+assists, over/under   -> player_points   (1+ point = over 0.5)
  assists, over/under         -> player_assists
  points, yes/no, yes side    -> player_goal_scorer_anytime (SportsGameOdds calls
                                 goals "points"; confirmed from the probe)

The key comes from SPORTSGAMEODDS_KEY and is never printed.
"""
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

import ice_engine_daily_pull as engine
import ice_engine_odds as base

BOOKS = {"fanduel": "FanDuel", "draftkings": "DraftKings"}
SGO = "https://api.sportsgameodds.com/v2"


def sgo_get(path, key, **params):
    url = f"{SGO}{path}?" + urllib.parse.urlencode(dict(params, apiKey=key))
    req = urllib.request.Request(url, headers={"User-Agent": "IceEngine/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise base.OddsError(f"SportsGameOdds call failed: HTTP {e.code} - {e.read()[:200].decode('utf-8', 'replace')}") from None
    except (urllib.error.URLError, TimeoutError) as e:
        raise base.OddsError(f"could not reach SportsGameOdds: {getattr(e, 'reason', e)}") from None


def player_name(player_id):
    """'ALEX_OVECHKIN_1_NHL' -> 'Alex Ovechkin'."""
    return " ".join(w.capitalize() for w in player_id.split("_")[:-2])


def american(text):
    try:
        return int(str(text).replace("+", "").strip())
    except ValueError:
        return None


def rows_for_event(ev, day, home, away, players, pulled_at, unmatched, settled, lineup, goal_stat=""):
    """One row per price: player x market x line x side x book (FD, DK only)."""
    out = {}
    names = {}
    for o in (ev.get("odds") or {}).values():
        pid = o.get("playerID")
        if pid and pid not in names:
            names[pid] = player_name(pid)
    matched = {}
    claimed = set()
    for pid, nm in sorted(names.items()):
        mid, note = base.match_player(nm, home, away, players, lineup, claimed)
        matched[pid] = mid
        if mid:
            claimed.add(mid)
        if note:
            (unmatched if mid is None else settled)[f"{nm} ({away} at {home})"] = note
    for o in (ev.get("odds") or {}).values():
        pid, stat, bt, side = o.get("playerID"), o.get("statID"), o.get("betTypeID"), o.get("sideID")
        if not pid:
            continue
        if stat == "goals+assists" and bt == "ou" and side == "over":
            market, store_side = "player_points", "Over"
        elif stat == "assists" and bt == "ou" and side == "over":
            market, store_side = "player_assists", "Over"
        elif stat == goal_stat and bt == "yn" and side == "yes":
            market, store_side = "player_goal_scorer_anytime", "Over"   # SGO names goals "points"
        else:
            continue
        for book_id, b in (o.get("byBookmaker") or {}).items():
            if book_id not in BOOKS or not b.get("available", True):
                continue
            price = american(b.get("odds"))
            if price is None:
                continue
            if market == "player_goal_scorer_anytime":
                line = 0.5                       # yes/no market, stored as over 0.5
            else:
                # Each book posts its OWN line (DraftKings 1.5 where FanDuel has 0.5).
                # Use that book's line, never the shared one, or prices get mixed.
                try:
                    line = float(b.get("overUnder"))
                except (TypeError, ValueError):
                    continue
            nm = names[pid]
            out[(nm, market, line, store_side, BOOKS[book_id])] = {
                "game_date": day.isoformat(), "event_id": ev["eventID"], "home": home, "away": away,
                "player_name": nm, "player_id": matched[pid], "market": market,
                "line": line, "side": store_side, "book": BOOKS[book_id],
                "price": price, "updated_at": pulled_at}
    return list(out.values())


def run(day, key, use_supabase, goal_stat):
    now = datetime.now(timezone.utc)
    pulled_at = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    tz = engine.nhl_timezone()
    end = datetime(day.year, day.month, day.day, tzinfo=tz) + timedelta(days=1)
    print(f"Ice Engine odds (SportsGameOdds) - {pulled_at} (NHL date {day})")
    res = sgo_get("/events", key, leagueID="NHL", oddsAvailable="true",
                  startsAfter=now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                  startsBefore=end.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), limit=30)
    events = []
    for e in res.get("data", []):
        start = datetime.fromisoformat(e["status"]["startsAt"].replace("Z", "+00:00"))
        if start > now and start.astimezone(tz).date() == day:   # trust nothing the API filter missed
            events.append(e)
    print(f"{len(events)} game(s) not started yet for {day}.")
    if not events:
        print("Nothing to pull.")
        return
    nick = base.team_abbreviations(day)
    players = base.load_players(sorted(set(nick.values())), use_supabase)
    lineup = base.load_lineup(day, use_supabase)
    rows, event_ids, unmatched, settled, problems = [], [], {}, {}, []
    for e in events:
        t = e.get("teams", {})
        name = lambda s: (t.get(s, {}).get("names", {}) or {}).get("long", "")
        away, home = base.abbreviation(name("away"), nick), base.abbreviation(name("home"), nick)
        label = f"{name('away')} at {name('home')}"
        if not (home and away):
            problems.append(f"{label}: can't map the team names to NHL abbreviations")
            continue
        ev_rows = rows_for_event(e, day, home, away, players, pulled_at, unmatched, settled, lineup, goal_stat)
        print(f"  {away} at {home}: {len(ev_rows)} prices (FanDuel/DraftKings)")
        rows += ev_rows
    unique = {(r["player_name"], r["market"], r["line"], r["side"], r["book"]): r for r in rows}
    rows = list(unique.values())
    with open("daily_odds_sgo.json", "w") as f:
        json.dump({"pulledAt": pulled_at, "date": day.isoformat(), "odds": rows}, f, indent=2)
    print(f"Wrote daily_odds_sgo.json ({len(rows)} rows)")
    if use_supabase and rows:
        engine.supabase_upsert("player_odds", rows, "game_date,player_name,market,line,side,book")
        print("Saved to Supabase.")
        # SportsGameOdds is now the only source: remove every older row (any book, any
        # earlier feed) for the games priced this run, in the markets this job writes.
        mk = "player_points,player_assists,player_goal_scorer_anytime"
        for h, a in sorted({(r["home"], r["away"]) for r in rows}):
            engine.supabase_request(
                "DELETE", f"player_odds?game_date=eq.{day.isoformat()}&home=eq.{h}&away=eq.{a}"
                          f"&market=in.({mk})&updated_at=lt.{pulled_at}")
        print("Removed older prices for these games.")
    base.report_names(unmatched, settled)
    if problems:
        raise base.OddsError(f"{len(problems)} problem(s):\n  - " + "\n  - ".join(problems))


def main():
    ap = argparse.ArgumentParser(description="Save FanDuel/DraftKings NHL player props (SportsGameOdds) to Supabase.")
    ap.add_argument("--date", default="")
    ap.add_argument("--goal-stat", default="points", help="SportsGameOdds statID that is goals (it calls them 'points')")
    ap.add_argument("--require-supabase", action="store_true")
    ap.add_argument("--only-at", default="", help="Eastern times for scheduled runs, e.g. '09:00,11:30'")
    a = ap.parse_args()
    from datetime import date
    go, slot, slot_day = engine.gate_on_schedule(a.only_at)
    if not go:
        return
    day = date.fromisoformat(a.date) if a.date.strip() else (slot_day or engine.nhl_today())
    key = os.environ.get("SPORTSGAMEODDS_KEY", "").strip()
    if not key:
        sys.exit("SPORTSGAMEODDS_KEY is not set.")
    use_supabase = bool(engine.SUPABASE_URL and engine.SUPABASE_KEY)
    if a.require_supabase and not use_supabase:
        sys.exit("SUPABASE_URL and SUPABASE_KEY must be set.")
    try:
        run(day, key, use_supabase, a.goal_stat.strip())
    except base.OddsError as e:
        print(f"[error] {e}", flush=True)
        if os.environ.get("GITHUB_ACTIONS"):
            print(f"::error title=SportsGameOdds pull failed::{str(e).splitlines()[0]}", flush=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
