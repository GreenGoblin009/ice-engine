#!/usr/bin/env python3
"""Settle picks/picks.json from the NHL's final box scores.

For every day in picks.json that still has a 'pending' leg, look up that
day's games on api-web.nhle.com. A leg is only settled once its game is
FINAL, and only hit or miss (never void): if a player can't be matched to a
box score the leg stays pending and a WARNING is printed. Legs already
marked hit or miss are never touched. Slip status is rebuilt from its legs:
any miss = miss, all hit = hit, otherwise pending.

Markets understood: "1+ pt", "2+ pts", "1+ ast", "Anytime goal", "2+ goals".
No money fields exist in picks.json and none are written.
"""
import argparse, json, re, sys, unicodedata, urllib.request

BASE = "https://api-web.nhle.com/v1"
FINAL = {"FINAL", "OFF"}


def fetch(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "ice-engine-settle"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    return re.sub(r"[^a-z]", "", "".join(c for c in s if not unicodedata.combining(c)).lower())


def parse_market(m):
    """-> (stat key, minimum) or None."""
    t = m.lower().strip()
    if "goal" in t:
        n = re.match(r"(\d)\+", t)
        return "goals", int(n.group(1)) if n else 1
    n = re.match(r"(\d)\+\s*(pt|ast)", t)
    if n:
        return ("points" if n.group(2) == "pt" else "assists"), int(n.group(1))
    return None


def day_games(date, cache, fetcher):
    """List of (game id, state, {team abbrev: skaters}) for one ET date."""
    if date in cache:
        return cache[date]
    out = []
    week = fetcher(f"/schedule/{date}")
    for day in week.get("gameWeek", []):
        if day.get("date") != date:
            continue
        for g in day.get("games", []):
            out.append((g["id"], g.get("gameState", ""), g["awayTeam"]["abbrev"], g["homeTeam"]["abbrev"]))
    games = []
    for gid, state, away, home in out:
        skaters = {}
        if state in FINAL:
            box = fetcher(f"/gamecenter/{gid}/boxscore")
            pbg = box.get("playerByGameStats", {})
            for side, abbrev in (("awayTeam", away), ("homeTeam", home)):
                lst = pbg.get(side, {}).get("forwards", []) + pbg.get(side, {}).get("defense", [])
                skaters[abbrev] = lst
        games.append((gid, state, {away, home}, skaters))
    cache[date] = games
    return games


def find_player(name, team, games):
    """-> ('final', stats) | ('notfinal', None) | ('missing', None)."""
    parts = name.split()
    last, first = norm(parts[-1]), norm(parts[0])[:1]
    seen_game = False
    for gid, state, teams, skaters in games:
        if team not in teams:
            continue
        seen_game = True
        if state not in FINAL:
            return "notfinal", None
        hits = []
        for p in skaters.get(team, []):
            pn = p.get("name", {}).get("default", "")
            pp = pn.split()
            if pp and norm(pp[-1]) == last and norm(pp[0])[:1] == first:
                hits.append(p)
        if len(hits) == 1:
            return "final", hits[0]
        return "missing", None
    return ("missing" if seen_game else "nogame"), None


def settle(data, fetcher=fetch, only_date=None):
    cache, changed, notes = {}, 0, []
    for day in data["days"]:
        if only_date and day["date"] != only_date:
            continue
        if not any(l.get("result") == "pending" for s in day["slips"] for l in s["legs"]):
            continue
        games = day_games(day["date"], cache, fetcher)
        for slip in day["slips"]:
            for leg in slip["legs"]:
                if leg.get("result") != "pending":
                    continue
                mk = parse_market(leg["market"])
                if not mk:
                    notes.append(f"WARNING {day['date']}: unknown market '{leg['market']}' ({leg['player']})")
                    continue
                state, p = find_player(leg["player"], leg["team"], games)
                if state == "final":
                    stat, need = mk
                    leg["result"] = "hit" if p.get(stat, 0) >= need else "miss"
                    changed += 1
                    notes.append(f"{day['date']} {leg['player']} {leg['market']}: {leg['result']} "
                                 f"(G{p.get('goals',0)} A{p.get('assists',0)} P{p.get('points',0)})")
                elif state in ("missing", "nogame"):
                    notes.append(f"WARNING {day['date']}: could not match {leg['player']} ({leg['team']}) "
                                 f"to a final box score ({state}); left pending")
            res = [l.get("result") for l in slip["legs"]]
            slip["status"] = ("miss" if "miss" in res else
                              "hit" if all(r == "hit" for r in res) else
                              "void" if all(r == "void" for r in res) else "pending")
    return changed, notes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="picks/picks.json")
    ap.add_argument("--date")
    a = ap.parse_args()
    data = json.load(open(a.file))
    changed, notes = settle(data, only_date=a.date)
    print("\n".join(notes) or "Nothing pending to settle.")
    if changed:
        with open(a.file, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
    print(f"{changed} leg(s) settled.")


if __name__ == "__main__":
    sys.exit(main())
