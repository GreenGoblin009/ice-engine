#!/usr/bin/env python3
"""Write FanDuel and DraftKings NHL player-prop prices (from SportsGameOdds)
to a plain text file in the repo, so Claude can read them when building cards.

Read-only toward Supabase (touches nothing there). Output lines look like
  Mitch Marner: goals+assists O0.5 FD -135 DK -130 | assists O0.5 FD +110 DK +105 | points Yes FD +140 DK +135
statID names are kept exactly as SportsGameOdds gives them; which one is
'goals' vs 'points' is confirmed from the probe. Key: SPORTSGAMEODDS_KEY.
"""
import argparse, collections, datetime as dt, json, os, sys, urllib.parse, urllib.request
from zoneinfo import ZoneInfo

KEY = os.environ.get("SPORTSGAMEODDS_KEY", "").strip()
if not KEY:
    sys.exit("SPORTSGAMEODDS_KEY is not set.")
ET = ZoneInfo("America/New_York")
BOOKS = (("fanduel", "FD"), ("draftkings", "DK"))
STATS = ("goals+assists", "assists", "points", "goals")


def get(path, **params):
    q = urllib.parse.urlencode(dict(params, apiKey=KEY))
    req = urllib.request.Request(f"https://api.sportsgameodds.com/v2{path}?{q}",
                                 headers={"User-Agent": "ice-engine-prices"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} from SportsGameOdds: {e.read()[:200].decode('utf-8','replace')}")


def pretty(pid):
    parts = pid.split("_")
    return " ".join(w.capitalize() for w in parts[:-2])  # drop the _1_NHL tail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="reports/sgo_prices.txt")
    ap.add_argument("--hours", type=int, default=30, help="only games starting within this many hours")
    a = ap.parse_args()
    now = dt.datetime.now(dt.timezone.utc)
    res = get("/events", leagueID="NHL", oddsAvailable="true", limit=30)
    lines = [f"SPORTSGAMEODDS PRICES (FanDuel, DraftKings)  pulled {now.astimezone(ET):%b %d %I:%M %p} ET",
             "Over/Yes sides only. FD/DK = American odds; '-' = book not offering.", ""]
    games = 0
    for ev in res.get("data", []):
        start = dt.datetime.fromisoformat(ev["status"]["startsAt"].replace("Z", "+00:00"))
        if not (now - dt.timedelta(hours=1) <= start <= now + dt.timedelta(hours=a.hours)):
            continue
        t = ev.get("teams", {})
        nm = [(t.get(s, {}).get("names", {}) or {}).get("long", "?") for s in ("away", "home")]
        players = collections.defaultdict(dict)
        for oid, o in (ev.get("odds") or {}).items():
            pid, stat = o.get("playerID"), o.get("statID")
            if not pid or stat not in STATS or o.get("sideID") not in ("over", "yes"):
                continue
            by = o.get("byBookmaker") or {}
            line = next((by[b].get("overUnder") for b, _ in BOOKS if b in by and by[b].get("overUnder") is not None),
                        o.get("bookOverUnder"))
            side = "Yes" if o.get("sideID") == "yes" else f"O{line}"
            prices = " ".join(f"{ab} {by[b]['odds']}" if b in by and by[b].get("available", True) else f"{ab} -"
                              for b, ab in BOOKS)
            if all(b not in by for b, _ in BOOKS):
                continue
            players[pid][(stat, side)] = prices
        if not players:
            continue
        games += 1
        lines.append(f"== {nm[0]} @ {nm[1]}  {start.astimezone(ET):%a %I:%M %p} ET ==")
        for pid in sorted(players):
            bits = [f"{st} {sd} {pr}" for (st, sd), pr in sorted(players[pid].items())]
            lines.append(f"{pretty(pid)}: " + " | ".join(bits))
        lines.append("")
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    open(a.out, "w").write("\n".join(lines) + "\n")
    print(f"Wrote {a.out}: {games} game(s).")


if __name__ == "__main__":
    main()
