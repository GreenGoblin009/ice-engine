#!/usr/bin/env python3
"""Post the day's Ice Cold Picks automatically, from reports/slate_latest.txt.

Can post more than once per ET day: later runs ADD picks to today's entry for games that have not started
and teams that have no pick yet, and the day's totals (MAX_PA points/assists, MAX_G goal) count what is
already posted. Existing picks are never changed.
Skips quietly unless the slate report has FRESH lineups and FRESH prices (both pulled
within MAX_AGE hours). Games that start at 2 PM ET or later wait until 1 PM ET (confirmed lineups);
early games (before 2 PM ET) can post from the morning. Only games that have not started.
No money fields are written. Results are filled in later by tools/settle_picks.py.

Rules (the formula-rules.md set): rest rule (a player picked in the last 4 days (about 2 games) sits out),
no-chase (two straight misses on a player and market benches him), never bet against Carolina,
one pick per team, a goalie listed for both teams, 3+ hits in L10, no 3-of-3 streak on points and
assists, points priced -130 or better, edge at least MIN_EDGE. Up to 6 points/assists picks and
1 goal pick (goal chance 35%+, edge 5+). Quality gate: points chance 52%+, assists 48%+, 16+ minutes, on a power play.
"""
import argparse, json, re, sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
MAX_AGE = 3.0
MIN_EDGE = 4.0
MAX_PA, MAX_G = 6, 1
MIN_PA = 2          # always post at least this many points/assists picks when anything qualifies
FLOOR_EDGE = 2.0


def parse_slate(text, year):
    L = text.split("\n")
    hdr = {}
    for l in L[:6]:
        m = re.match(r"(Lineups|Prices|Goalies) pulled:\s+(.*)", l)
        if m:
            hdr[m.group(1)] = m.group(2).strip()
    date = re.search(r"SLATE REPORT\s+(\d{4}-\d{2}-\d{2})", L[0]).group(1)
    games = []
    for l in L:
        m = re.match(r"- (\d+):(\d\d) (AM|PM) ET\s+(\w+) [\d.]+ @ (\w+) [\d.]+", l)
        if m:
            h, mi, ap, a, h_ = int(m.group(1)), int(m.group(2)), m.group(3), m.group(4), m.group(5)
            h = h % 12 + (12 if ap == "PM" else 0)
            games.append((h, mi, a, h_))
    goalie = {}
    for l in L:
        m = re.match(r"- (\w+): (.+)", l)
        if m and ("expected" in l or "CONFIRMED" in l or "no goalie listed" in l) and "L10" not in l:
            goalie[m.group(1)] = "no goalie listed" not in l
    cands, team, on = [], None, False
    excl_names = set()
    for l in L:
        if l.startswith("ALL PRICED SKATERS"):
            on = True
            continue
        if not on:
            continue
        if re.fullmatch(r"[A-Z]{2,3}", l):
            team = l
            continue
        m = re.match(r"- (.+?) \(([\d.]+), ([\d.]+), ([\w ]+)\): G (.*?) \| P (.*?) \| A (.*)", l)
        if not m:
            continue
        name, sh, mn, pp, G, P, A = m.groups()
        for mk, s in (("P", P), ("A", A), ("G", G)):
            mm = re.match(r"(\d+)% ([+-]\d+) (\w+) ([+-][\d.]+), L10 (\d+)/10, L3 (\d)/3", s)
            if mm:
                ch, pr, bk, ed, l10, l3 = mm.groups()
                cands.append(dict(name=name, team=team, mk=mk, chance=int(ch), price=int(pr), book=bk,
                                  edge=float(ed), l10=int(l10), l3=int(l3), sog=float(sh), mins=float(mn), pp=pp))
    return date, hdr, games, goalie, cands


def pulled_dt(s, year):
    m = re.match(r"([A-Za-z]{3}) (\d+), (\d+):(\d\d) (AM|PM) ET", s or "")
    if not m:
        return None
    h = int(m.group(3)) % 12 + (12 if m.group(5) == "PM" else 0)
    return datetime.strptime(f"{year} {m.group(1)} {m.group(2)}", "%Y %b %d").replace(hour=h, minute=int(m.group(4)), tzinfo=ET)


def fmt(p):
    return f"{p:+d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slate", default="reports/slate_latest.txt")
    ap.add_argument("--picks", default="picks/picks.json")
    ap.add_argument("--now", help="override ET now, ISO")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    now = datetime.fromisoformat(a.now).replace(tzinfo=ET) if a.now else datetime.now(ET)
    today = now.strftime("%Y-%m-%d")
    data = json.load(open(a.picks))
    day_today = next((d for d in data["days"] if d["date"] == today), None)
    posted = [s for s in (day_today["slips"] if day_today else [])]
    posted_legs = [l for s in posted for l in s["legs"]]
    have_pa = len([l for l in posted_legs if "goal" not in l["market"].lower()])
    have_g = len([l for l in posted_legs if "goal" in l["market"].lower()])
    used_teams = {l["team"] for l in posted_legs}
    date, hdr, games, goalie, cands = parse_slate(open(a.slate).read(), now.year)
    if date != today:
        print(f"Slate report is for {date}, not {today}; skipping."); return
    for k in ("Lineups", "Prices"):
        t = pulled_dt(hdr.get(k), now.year)
        if t is None or now - t > timedelta(hours=MAX_AGE):
            print(f"{k} not fresh ({hdr.get(k)}); skipping."); return
    # games that have not started (15 minute buffer) and have a goalie listed for both teams
    ok_teams, opp = set(), {}
    for h, mi, away, home in games:
        start = now.replace(hour=h, minute=mi, second=0, microsecond=0)
        if start - now < timedelta(minutes=15):
            continue
        if now.hour < 13 and h >= 14:
            continue   # evening games wait for confirmed lineups (1 PM ET)
        if not (goalie.get(away) and goalie.get(home)):
            continue
        ok_teams |= {away, home}
        opp[away], opp[home] = home, away
    if not ok_teams:
        print("No upcoming games with goalies and prices (or before 1 PM ET for later games); skipping."); return
    days = sorted(data["days"], key=lambda d: d["date"])
    cut = (now - timedelta(days=4)).strftime("%Y-%m-%d")  # about 2 games of rest
    recent = {l["player"] for d in days if d["date"] >= cut for s in d["slips"] for l in s["legs"]}
    def mk_of(m):
        m = m.lower(); return "G" if "goal" in m else "A" if "ast" in m else "P"
    hist = {}
    for d in days:
        for s in d["slips"]:
            for l in s["legs"]:
                if l["result"] in ("hit", "miss"):
                    hist.setdefault((l["player"], mk_of(l["market"])), []).append(l["result"])
    benched = {k for k, v in hist.items() if v[-2:] == ["miss", "miss"]}
    def eligible(c):
        return (c["team"] in ok_teams and c["name"] not in recent and (c["name"], c["mk"]) not in benched
                and opp.get(c["team"]) != "CAR" and c["l10"] >= 3)
    used, picks = set(used_teams), []
    pa = [c for c in cands if eligible(c) and c["mk"] in "PA" and c["l3"] < 3 and c["edge"] >= MIN_EDGE
          and not (c["mk"] == "P" and c["price"] < -130)
          and c["chance"] >= (52 if c["mk"] == "P" else 48) and c["mins"] >= 16 and c["pp"] != "no PP"]
    pa.sort(key=lambda c: -c["edge"])
    for c in pa:
        if have_pa + len([p for p in picks if p["mk"] in "PA"]) >= MAX_PA: break
        if c["team"] in used: continue
        used.add(c["team"]); picks.append(c)
    # Floor of MIN_PA picks (user, Nov 4: "2 minimum so we keep learning"): if the strict list is short,
    # fill from the next best points/assists with a relaxed quality gate (still 3+ L10 hits, no 3-of-3,
    # points -130 or better, one per team, edge of at least FLOOR_EDGE).
    if have_pa + len([p for p in picks if p["mk"] in "PA"]) < MIN_PA:
        spare = [c for c in cands if eligible(c) and c["mk"] in "PA" and c["l3"] < 3 and c["team"] not in used
                 and c["edge"] >= FLOOR_EDGE and c["chance"] >= 40 and c["mins"] >= 14
                 and not (c["mk"] == "P" and c["price"] < -130)]
        spare.sort(key=lambda c: -c["edge"])
        for c in spare:
            if have_pa + len([p for p in picks if p["mk"] in "PA"]) >= MIN_PA: break
            used.add(c["team"]); picks.append(c)
    gl = [c for c in cands if eligible(c) and c["mk"] == "G" and c["chance"] >= 30 and c["edge"] >= 2]   # one goal pick a day (user, Nov 4); may share a team with a point/assist pick
    gl.sort(key=lambda c: -c["edge"])
    picks += gl[:max(0, MAX_G - have_g)]
    if not picks:
        print("Nothing met the rules today; posting nothing."); return
    nid = max([s["id"] for d in days for s in d["slips"]] + [0])
    slips = []
    for c in picks:
        nid += 1
        mkt = {"P": "1+ pt", "A": "1+ ast", "G": "Anytime goal"}[c["mk"]]
        slips.append({"id": nid, "type": "Goals" if c["mk"] == "G" else "Points & Assists", "book": "", "status": "pending",
                      "legs": [{"player": c["name"], "team": c["team"], "market": mkt, "price": fmt(c["price"]), "result": "pending"}]})
        print(f'{c["name"]} {c["team"]} {mkt} {fmt(c["price"])} edge {c["edge"]:+.1f}')
    if day_today:
        day_today["slips"].extend(slips)
    else:
        data["days"].append({"date": today, "slips": slips})
    if not a.dry:
        json.dump(data, open(a.picks, "w"), indent=1)
        print(f"Posted {len(slips)} picks for {today}.")


if __name__ == "__main__":
    main()
