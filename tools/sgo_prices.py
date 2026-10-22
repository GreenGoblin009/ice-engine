#!/usr/bin/env python3
"""Write FanDuel and DraftKings NHL player-prop prices (from SportsGameOdds)
to a plain text file in the repo, so Claude can read them when building cards.

Read-only toward Supabase (touches nothing there). Output lines look like
  Mitch Marner: goals+assists O0.5 FD -135 DK -130 | assists O0.5 FD +110 DK +105 | points Yes FD +140 DK +135
Labels: pts = 1+ point lines (goals+assists), ast = assists, goal = anytime goal
(SportsGameOdds calls goals 'points'). Each book's OWN line is used. Key: SPORTSGAMEODDS_KEY.
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
        players = collections.defaultdict(lambda: collections.defaultdict(dict))
        for oid, o in (ev.get("odds") or {}).items():
            pid, stat, bt, side = o.get("playerID"), o.get("statID"), o.get("betTypeID"), o.get("sideID")
            if not pid or o.get("periodID", "game") != "game" or "-game-" not in oid:
                continue   # full-game props only, never 1st/2nd-period ones
            by = o.get("byBookmaker") or {}
            for b, ab in BOOKS:
                d = by.get(b)
                if not d or not d.get("available", True) or d.get("odds") is None:
                    continue
                if stat == "goals+assists" and bt == "ou" and side == "over":
                    label = f"pts O{d.get('overUnder')}"
                elif stat == "assists" and bt == "ou" and side == "over":
                    label = f"ast O{d.get('overUnder')}"
                elif stat == "points" and bt == "yn" and side == "yes":
                    label = "goal"
                else:
                    continue
                players[pid][label][ab] = d["odds"]
        # Book game totals (full-game over/under on total goals), one line per book.
        tot = {}
        for oid, o in (ev.get("odds") or {}).items():
            if not oid.startswith("points-all-game-ou-"):
                continue
            side = "over" if oid.endswith("-over") else "under" if oid.endswith("-under") else None
            for b, ab in BOOKS:
                d = (o.get("byBookmaker") or {}).get(b)
                if side and d and d.get("available", True) and d.get("odds") is not None:
                    e = tot.setdefault(ab, {})
                    e["line"] = d.get("overUnder")
                    e[side] = d["odds"]
        if not players:
            continue
        games += 1
        lines.append(f"== {nm[0]} @ {nm[1]}  {start.astimezone(ET):%a %I:%M %p} ET ==")
        if tot:
            lines.append("GAME TOTAL: " + " | ".join(
                f"{ab} {v.get('line','?')} (o {v.get('over','-')} / u {v.get('under','-')})" for ab, v in sorted(tot.items())))
        for pid in sorted(players):
            bits = [f"{lb} " + " ".join(f"{ab} {pr.get(ab, '-')}" for _, ab in BOOKS)
                    for lb, pr in sorted(players[pid].items())]
            lines.append(f"{pretty(pid)}: " + " | ".join(bits))
        lines.append("")
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    open(a.out, "w").write("\n".join(lines) + "\n")
    print(f"Wrote {a.out}: {games} game(s).")


if __name__ == "__main__":
    main()
