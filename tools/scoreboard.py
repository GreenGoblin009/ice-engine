#!/usr/bin/env python3
"""Projection scoreboard: how accurate were the slate report's numbers?

For every ET date that has archived slate reports in git history, take the
LAST report committed before that date's first puck (the numbers we would
have used), then compare them with the final box scores:

  * skater chances (Goals / Points / Assists 1+): Brier score, log-loss,
    a calibration table (predicted bucket vs actual hit rate), and the same
    scores for a plain "league average" guess so we know if the model adds
    anything;
  * game totals: the report's projected total vs the real total goals.

Read-only on picks. Writes reports/scoreboard.md and reports/scoreboard_rows.csv.
Players who are not in a final box score (scratched, game not final) are left
out and counted. Needs full git history (actions/checkout fetch-depth: 0) and
the NHL API (api-web.nhle.com).
"""
import csv, json, math, re, subprocess, sys, unicodedata, urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

BASE = "https://api-web.nhle.com/v1"
ET = ZoneInfo("America/New_York")
REPORT = "reports/slate_latest.txt"
FINAL = {"FINAL", "OFF"}
BUCKETS = [(0, .15), (.15, .25), (.25, .35), (.35, .45), (.45, .55), (.55, .65), (.65, .75), (.75, 1.01)]


def fetch(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "ice-engine-scoreboard"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    return re.sub(r"[^a-z]", "", "".join(c for c in s if not unicodedata.combining(c)).lower())


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def start_minutes(txt):
    """Earliest puck drop (minutes after midnight ET) from the GAMES block."""
    mins = []
    for m in re.finditer(r"^- (\d{1,2}):(\d\d) (AM|PM) ET\s+[A-Z]{2,3} [\d.]+ @", txt, re.M):
        h, mi, ap = int(m.group(1)), int(m.group(2)), m.group(3)
        h = h % 12 + (12 if ap == "PM" else 0)
        mins.append(h * 60 + mi)
    return min(mins) if mins else None


def archived_reports():
    """{date: report text} choosing the last report before first puck."""
    out = {}
    log = git("log", "--format=%H %ct", "--", REPORT).split("\n")
    for line in log:
        if not line.strip():
            continue
        h, ct = line.split()
        try:
            txt = git("show", f"{h}:{REPORT}")
        except subprocess.CalledProcessError:
            continue
        m = re.match(r"ICE ENGINE SLATE REPORT\s+(\d{4}-\d\d-\d\d)", txt)
        sm = start_minutes(txt)
        if not m or sm is None:
            continue
        date = m.group(1)
        when = datetime.fromtimestamp(int(ct), timezone.utc).astimezone(ET)
        if when.strftime("%Y-%m-%d") != date or when.hour * 60 + when.minute >= sm:
            continue  # committed after puck drop or on another day
        if date not in out or int(ct) > out[date][0]:
            out[date] = (int(ct), txt)
    return {d: v[1] for d, v in sorted(out.items())}


def parse_report(txt):
    games = []
    for m in re.finditer(r"^- .*?ET\s+([A-Z]{2,3}) ([\d.]+) @ ([A-Z]{2,3}) ([\d.]+)\s+\(total ([\d.]+)\)", txt, re.M):
        games.append(dict(away=m.group(1), away_p=float(m.group(2)), home=m.group(3),
                          home_p=float(m.group(4)), total=float(m.group(5))))
    skaters = []
    if "ALL PRICED SKATERS" not in txt:
        return games, skaters
    sec = txt[txt.index("ALL PRICED SKATERS"):]
    team = None
    for ln in sec.splitlines():
        if re.fullmatch(r"[A-Z]{2,3}", ln.strip()):
            team = ln.strip()
            continue
        m = re.match(r"- (.+?) \(([\d.]+), ([\d.]+), (PP\d|no PP)\): (.*)", ln)
        if not m or not team:
            continue
        rest = m.group(5)
        d = dict(name=m.group(1), team=team, pp=m.group(4), mins=float(m.group(3)))
        for key, rx in (("G", r"G (\d+)%"), ("P", r"\| P (\d+)%"), ("A", r"\| A (\d+)%")):
            x = re.search(rx, rest)
            if x:
                d[key] = int(x.group(1)) / 100
        skaters.append(d)
    return games, skaters


def results_for(date):
    """-> ({team: [skater dicts]}, {frozenset(teams): total goals}) for FINAL games."""
    sk, tot = {}, {}
    week = fetch(f"/schedule/{date}")
    for day in week.get("gameWeek", []):
        if day.get("date") != date:
            continue
        for g in day.get("games", []):
            if g.get("gameState") not in FINAL:
                continue
            box = fetch(f"/gamecenter/{g['id']}/boxscore")
            away, home = g["awayTeam"]["abbrev"], g["homeTeam"]["abbrev"]
            tot[frozenset((away, home))] = (box["awayTeam"].get("score", 0) + box["homeTeam"].get("score", 0),
                                             box["awayTeam"].get("score", 0), box["homeTeam"].get("score", 0), away, home)
            pbg = box.get("playerByGameStats", {})
            for side, ab in (("awayTeam", away), ("homeTeam", home)):
                sk[ab] = pbg.get(side, {}).get("forwards", []) + pbg.get(side, {}).get("defense", [])
    return sk, tot


def match(name, team, sk):
    parts = name.split()
    last, first = norm(parts[-1]), norm(parts[0])[:1]
    hits = []
    for p in sk.get(team, []):
        pp = p.get("name", {}).get("default", "").split()
        if pp and norm(pp[-1]) == last and norm(pp[0])[:1] == first:
            hits.append(p)
    return hits[0] if len(hits) == 1 else None


def main():
    reports = archived_reports()
    print(f"{len(reports)} archived pre-game reports: {', '.join(reports)}")
    rows, grows, notes = [], [], []
    for date, txt in reports.items():
        games, skaters = parse_report(txt)
        if not skaters:
            notes.append(f"{date}: report has no skater section; skipped")
            continue
        sk, tot = results_for(date)
        for g in games:
            r = tot.get(frozenset((g["away"], g["home"])))
            if r:
                grows.append(dict(date=date, game=f"{g['away']}@{g['home']}", proj=g["total"],
                                  actual=r[0], proj_away=g["away_p"], proj_home=g["home_p"],
                                  act_away=r[1], act_home=r[2]))
        miss = 0
        for s in skaters:
            p = match(s["name"], s["team"], sk)
            if p is None:
                miss += 1
                continue
            for key, stat in (("G", "goals"), ("P", "points"), ("A", "assists")):
                if key in s:
                    rows.append(dict(date=date, name=s["name"], team=s["team"], mk=key,
                                     p=s[key], pp=s["pp"], mins=s["mins"],
                                     hit=1 if p.get(stat, 0) >= 1 else 0))
        notes.append(f"{date}: {len(skaters)} skaters in the report, {miss} not matched to a final box score")
    write(rows, grows, notes)


def score(rs):
    n = len(rs)
    if not n:
        return None
    base = sum(r["hit"] for r in rs) / n
    brier = sum((r["p"] - r["hit"]) ** 2 for r in rs) / n
    bbrier = sum((base - r["hit"]) ** 2 for r in rs) / n

    def ll(p, y):
        p = min(max(p, 0.01), 0.99)
        return -(y * math.log(p) + (1 - y) * math.log(1 - p))
    return dict(n=n, pred=sum(r["p"] for r in rs) / n, act=base, brier=brier, base_brier=bbrier,
                ll=sum(ll(r["p"], r["hit"]) for r in rs) / n,
                base_ll=sum(ll(base, r["hit"]) for r in rs) / n)


def write(rows, grows, notes):
    with open("reports/scoreboard_rows.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["date", "name", "team", "mk", "p", "pp", "mins", "hit"])
        w.writeheader()
        w.writerows(rows)
    L = ["# Projection scoreboard", "",
         f"Updated {datetime.now(ET).strftime('%Y-%m-%d %H:%M ET')}. Uses the last slate report committed before first puck each day.",
         "Brier and log-loss: lower is better. 'Naive' guesses the same average for everyone; the model should beat it.", ""]
    L += ["## Skater chances, 1+ goal / point / assist", "",
          "| Market | N | Avg predicted | Actual rate | Brier | Naive Brier | Log-loss | Naive log-loss |", "|---|---|---|---|---|---|---|---|"]
    for key, name in (("G", "Goal"), ("P", "Point"), ("A", "Assist")):
        s = score([r for r in rows if r["mk"] == key])
        if s:
            L.append(f"| {name} | {s['n']} | {s['pred']*100:.1f}% | {s['act']*100:.1f}% | {s['brier']:.4f} | {s['base_brier']:.4f} | {s['ll']:.4f} | {s['base_ll']:.4f} |")
    for key, name in (("G", "Goal"), ("P", "Point"), ("A", "Assist")):
        L += ["", f"### Calibration, {name}", "", "| Predicted | N | Avg predicted | Actual |", "|---|---|---|---|"]
        for lo, hi in BUCKETS:
            b = [r for r in rows if r["mk"] == key and lo <= r["p"] < hi]
            if b:
                L.append(f"| {int(lo*100)}-{min(int(hi*100),100)}% | {len(b)} | {sum(r['p'] for r in b)/len(b)*100:.1f}% | {sum(r['hit'] for r in b)/len(b)*100:.1f}% |")
    L += ["", "### Point chance by role", "", "| Role | N | Avg predicted | Actual |", "|---|---|---|---|"]
    for role in ("PP1", "PP2", "no PP"):
        b = [r for r in rows if r["mk"] == "P" and r["pp"] == role]
        if b:
            L.append(f"| {role} | {len(b)} | {sum(r['p'] for r in b)/len(b)*100:.1f}% | {sum(r['hit'] for r in b)/len(b)*100:.1f}% |")
    if grows:
        n = len(grows)
        mae = sum(abs(g["proj"] - g["actual"]) for g in grows) / n
        bias = sum(g["actual"] - g["proj"] for g in grows) / n
        avg = sum(g["actual"] for g in grows) / n
        naive = sum(abs(avg - g["actual"]) for g in grows) / n
        L += ["", "## Game totals", "",
              f"Games: {n}. Average projected total {sum(g['proj'] for g in grows)/n:.2f}, actual {avg:.2f} (actual minus projected: {bias:+.2f}).",
              f"Mean absolute error {mae:.2f} goals, against {naive:.2f} for a flat guess at the average.", "",
              "| Date | Game | Projected | Actual |", "|---|---|---|---|"]
        for g in grows:
            L.append(f"| {g['date']} | {g['game']} | {g['proj']:.2f} | {g['actual']} |")
    L += ["", "## Data notes", ""] + [f"- {x}" for x in notes]
    open("reports/scoreboard.md", "w").write("\n".join(L) + "\n")
    print("\n".join(L[:30]))


if __name__ == "__main__":
    sys.exit(main())
