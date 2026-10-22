#!/usr/bin/env python3
"""First-period / early-goal report for a slate (for 'quickest first goal' contests).

Reads this season's final regular-season games from the NHL play-by-play and writes
reports/first_period.txt:
  * per team: first-period goals for / against per game, share of games with a goal
    in the first 5 / 10 / 20 minutes, average clock time of the first goal of the game
  * per goalie: first-period save % (goals against on shots on goal in period 1)
  * per skater on the games listed in reports/slate_latest.txt that start at the chosen
    time: first-period goals, first-period shots on goal per game, times he scored the
    first goal of the game.
Usage: python tools/first_period.py [--start 2026-10-01] [--slate-time "7:00 PM ET"]
"""
import argparse, json, re, sys, urllib.request
from collections import defaultdict
from datetime import date, datetime, timedelta

BASE = "https://api-web.nhle.com/v1"
FINAL = {"FINAL", "OFF"}


def fetch(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "ice-engine-first-period"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def clock(t):  # "MM:SS" -> minutes into the period
    m, s = t.split(":")
    return int(m) + int(s) / 60


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2026-10-01")
    ap.add_argument("--slate-time", default="7:00 PM ET")
    a = ap.parse_args()

    ids, seen = [], set()
    d = datetime.strptime(a.start, "%Y-%m-%d").date()
    end = date.today()
    while d <= end:
        try:
            wk = fetch(f"/schedule/{d}")
        except Exception as e:
            print("schedule fail", d, e)
            d += timedelta(days=7)
            continue
        for day in wk.get("gameWeek", []):
            for g in day.get("games", []):
                if g.get("gameType") == 2 and g.get("gameState") in FINAL and g["id"] not in seen:
                    seen.add(g["id"])
                    ids.append(g["id"])
        d += timedelta(days=7)
    print(len(ids), "final games")

    team = defaultdict(lambda: dict(gp=0, gf1=0, ga1=0, early5=0, early10=0, early20=0, first_t=[], first_scored=0))
    goalie = defaultdict(lambda: dict(sog=0, ga=0, gp=0, name=""))
    sk = defaultdict(lambda: dict(name="", team="", gp=0, g1=0, sog1=0, first=0, first_times=[]))

    for gid in ids:
        try:
            pbp = fetch(f"/gamecenter/{gid}/play-by-play")
        except Exception as e:
            print("pbp fail", gid, e)
            continue
        away, home = pbp["awayTeam"], pbp["homeTeam"]
        tid = {away["id"]: away["abbrev"], home["id"]: home["abbrev"]}
        names = {}
        for r in pbp.get("rosterSpots", []):
            names[r["playerId"]] = (f"{r['firstName']['default']} {r['lastName']['default']}", tid.get(r["teamId"], ""))
        plays = pbp.get("plays", [])
        goalies_seen = set()
        for ab in tid.values():
            team[ab]["gp"] += 1
        played = set()
        first_goal = None
        for p in plays:
            per = p.get("periodDescriptor", {}).get("number")
            typ = p.get("typeDescKey")
            det = p.get("details", {})
            owner = tid.get(det.get("eventOwnerTeamId"))
            t = clock(p.get("timeInPeriod", "00:00")) if per else 0
            gameclock = (per - 1) * 20 + t if per else 0
            if typ == "goal":
                scorer = det.get("scoringPlayerId")
                other = [x for x in tid.values() if x != owner][0] if owner else None
                if first_goal is None and per:
                    first_goal = (gameclock, owner, scorer)
                if per == 1:
                    if owner:
                        team[owner]["gf1"] += 1
                    if other:
                        team[other]["ga1"] += 1
                    gk = det.get("goalieInNetId")
                    if gk is not None:
                        goalie[gk]["sog"] += 1
                        goalie[gk]["ga"] += 1
                        goalie[gk]["name"], goalie[gk]["team"] = names.get(gk, ("?", ""))
                    if scorer in names:
                        s = sk[scorer]
                        s["name"], s["team"] = names[scorer]
                        s["g1"] += 1
            elif typ == "shot-on-goal" and per == 1:
                shooter = det.get("shootingPlayerId")
                gk = det.get("goalieInNetId")
                if gk is not None:
                    goalie[gk]["sog"] += 1
                    goalie[gk]["name"], goalie[gk]["team"] = names.get(gk, ("?", ""))
                if shooter in names:
                    s = sk[shooter]
                    s["name"], s["team"] = names[shooter]
                    s["sog1"] += 1
        # games played counts for every rostered skater in this game
        for pid, (nm, ab) in names.items():
            s = sk[pid]
            s["name"], s["team"] = nm, ab
            s["gp"] += 1
        if first_goal:
            gt, owner, scorer = first_goal
            for ab in tid.values():
                team[ab]["first_t"].append(gt)
            if owner:
                team[owner]["first_scored"] += 1
            for ab in tid.values():
                if gt <= 5:
                    team[ab]["early5"] += 1
                if gt <= 10:
                    team[ab]["early10"] += 1
                if gt <= 20:
                    team[ab]["early20"] += 1
            if scorer in names:
                sk[scorer]["first"] += 1
                sk[scorer]["first_times"].append(gt)

    # tonight's games from the slate report
    txt = open("reports/slate_latest.txt").read()
    games = re.findall(rf"^- {re.escape(a.slate_time)}\s+([A-Z]{{2,3}}) [\d.]+ @ ([A-Z]{{2,3}}) ", txt, re.M)
    tonight = {x for g in games for x in g}
    out = [f"FIRST-PERIOD REPORT  built {datetime.now():%Y-%m-%d %H:%M} from {len(ids)} final games since {a.start}",
           f"Slate: {a.slate_time}: " + ", ".join(f"{x}@{y}" for x, y in games), ""]
    out.append("TEAMS (per game): 1st-period GF / GA, share of games with a goal by minute 5 / 10 / 20, average game minute of the first goal, share of games the team scored the first goal")
    for ab in sorted(tonight):
        t = team[ab]
        n = max(t["gp"], 1)
        ft = sum(t["first_t"]) / max(len(t["first_t"]), 1)
        out.append(f"- {ab}: GP {t['gp']}  1P GF {t['gf1']/n:.2f} / GA {t['ga1']/n:.2f}  by 5:{t['early5']/n*100:.0f}% by 10:{t['early10']/n*100:.0f}% by 20:{t['early20']/n*100:.0f}%  first goal avg {ft:.1f} min  scored first {t['first_scored']}/{t['gp']}")
    out.append("")
    out.append("SKATERS on those teams, min 6 GP: 1P goals, 1P shots on goal per game, times he scored the game's first goal (avg minute); sorted by 1P goals then 1P shots/game")
    rows = [s for s in sk.values() if s["team"] in tonight and s["gp"] >= 6]
    rows.sort(key=lambda s: (-s["g1"], -s["sog1"] / s["gp"]))
    for s in rows[:40]:
        ft = f"{sum(s['first_times'])/len(s['first_times']):.1f}" if s["first_times"] else "-"
        out.append(f"- {s['name']} {s['team']}: GP {s['gp']}  1P G {s['g1']}  1P SOG/g {s['sog1']/s['gp']:.2f}  first goal of game {s['first']} (avg min {ft})")
    out.append("")
    out.append("GOALIES on those teams, first-period save % over the shots they faced in period 1 this season (min 25 shots)")
    for g in sorted((g for g in goalie.values() if g.get("team") in tonight and g["sog"] >= 25), key=lambda g: g["team"]):
        out.append(f"- {g['name']} {g['team']}: 1P shots {g['sog']}  goals {g['ga']}  save % {1-g['ga']/g['sog']:.3f}")
    open("reports/first_period.txt", "w").write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    sys.exit(main())
