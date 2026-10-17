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
# Market meaning check. For a few named players, print EVERY odd SportsGameOdds
# has for them in the stats we use, with the line and each book's price, so we
# can see exactly what "goals+assists", "assists" and "points" mean.
WANT = ("SEBASTIAN_AHO", "NIKITA_KUCHEROV", "ALEX_TUCH", "KYLE_CONNOR")
print("\nMARKET CHECK")
for ev in events:
    for oid, o in (ev.get("odds") or {}).items():
        pid = o.get("playerID") or ""
        if not any(pid.startswith(w) for w in WANT):
            continue
        if o.get("statID") not in ("points", "goals+assists", "assists", "goals"):
            continue
        by = o.get("byBookmaker") or {}
        row = {b: (d.get("odds"), d.get("overUnder")) for b, d in by.items() if b in ("fanduel", "draftkings")}
        print(f"  {oid} | main line={o.get('bookOverUnder')} price={o.get('bookOdds')} | {row}")
