#!/usr/bin/env python3
"""Probe SportsGameOdds for NHL: which books price which player props.

Read-only. Saves nothing to Supabase. Prints, for upcoming NHL games, how many
player-prop odds exist per stat (points/assists/goals...) and per bookmaker,
so we can see whether FanDuel, DraftKings, theScore and Fanatics are covered.
Key comes from the SPORTSGAMEODDS_KEY environment variable and is never printed.
"""
import collections, json, os, sys, urllib.parse, urllib.request

KEY = os.environ.get("SPORTSGAMEODDS_KEY", "").strip()
if not KEY:
    sys.exit("SPORTSGAMEODDS_KEY is not set (add it as a GitHub secret).")


def get(path, **params):
    q = urllib.parse.urlencode(dict(params, apiKey=KEY))
    req = urllib.request.Request(f"https://api.sportsgameodds.com/v2{path}?{q}",
                                 headers={"User-Agent": "ice-engine-probe"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} from SportsGameOdds: {e.read()[:300].decode('utf-8','replace')}")


res = get("/events", leagueID="NHL", oddsAvailable="true", limit=20)
events = res.get("data", [])
print(f"success={res.get('success')} events returned={len(events)}")
by_stat_book = collections.defaultdict(lambda: collections.Counter())
books_all = collections.Counter()
for ev in events:
    t = ev.get("teams", {})
    names = [(t.get(s, {}).get("names", {}) or {}).get("long", "?") for s in ("away", "home")]
    print("-", " @ ".join(names), "|", (ev.get("status") or {}).get("startsAt", ""))
    for oid, o in (ev.get("odds") or {}).items():
        if not o.get("playerID"):
            continue
        stat = o.get("statID", "?")
        for book, b in (o.get("byBookmaker") or {}).items():
            if b.get("available", True):
                by_stat_book[stat][book] += 1
                books_all[book] += 1
print("\nPlayer-prop odds by stat and bookmaker (count of priced lines):")
for stat, c in sorted(by_stat_book.items()):
    print(f"  {stat}: " + ", ".join(f"{b}={n}" for b, n in c.most_common()))
print("\nAll bookmakers on player props:", ", ".join(f"{b}={n}" for b, n in books_all.most_common()))
for want in ("fanduel", "draftkings", "thescore", "fanatics"):
    print(f"  {want}: {'YES' if books_all.get(want) else 'not seen'} ({books_all.get(want, 0)} lines)")
# Market meaning check: for the first game, show a few players' lines for the
# stats we care about, with each book's price and line, so we can confirm which
# statID is goals, which is points (G+A) and which is assists.
ev = events[0] if events else {}
print("\nMARKET CHECK (first game):")
shown = collections.Counter()
for oid, o in (ev.get("odds") or {}).items():
    stat = o.get("statID")
    if not o.get("playerID") or stat not in ("points", "goals+assists", "assists", "goals"):
        continue
    key = (stat, o.get("betTypeID"), o.get("sideID"))
    if shown[key] >= 2:
        continue
    shown[key] += 1
    row = {b: (d.get("odds"), d.get("overUnder")) for b, d in (o.get("byBookmaker") or {}).items()
           if b in ("fanduel", "draftkings")}
    print(f"  {oid} | line={o.get('bookOverUnder')} | {row}")
print("stat/bet/side combos seen:", sorted({(o.get('statID'), o.get('betTypeID'), o.get('sideID'))
      for o in (ev.get('odds') or {}).values() if o.get('playerID')}))
