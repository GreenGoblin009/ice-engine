"""
Ice Engine — Slate Report
=========================
A read-only, plain-text report of one day's slate, built from the same
numbers the board shows (index.html):

  - game times and projected goals per team (Teams tab model)
  - starting goalie per team, confirmed or expected, with save %
  - injured and scratched players from the day's lineups
  - each team's last 10 regular-season games: goals for/against, shots
    for/against, power play and penalty kill (from NHL.com box scores)
  - every priced skater: role-adjusted chance for goals, points and
    assists (Hot tab model), best price and book, edge, last 10, shots per
    game, minutes and power-play unit
  - top 15 for each stat by chance, and top 15 by edge, with the DraftKings
    and FanDuel price for each leg
  - data checks: games with no prices, priced players missing from the
    lineups, unconfirmed goalies

It only reads (Supabase and the NHL's public API); it never writes to the
database. Run by .github/workflows/slate.yml, which commits the output to
reports/slate_latest.txt.

Usage:
  python tools/slate_report.py                       # today (US Eastern)
  python tools/slate_report.py --date 2026-10-15
  python tools/slate_report.py --out reports/slate_latest.txt --only-at "11:00,16:30,19:15"

Needs SUPABASE_URL and SUPABASE_KEY in the environment.
"""
import argparse
import math
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import ice_engine_daily_pull as engine  # noqa: E402

# ---- constants mirrored from index.html; keep them in step with the board ----
PRIOR_GAMES = 15          # weight (in games) given to last season's rate
LEAGUE_AVG = 3.05
LEAGUE_SV = 0.905
SV_SHRINK = 400           # shots of league-average save % mixed into each goalie's
SHRINK_K = 10             # games of the role pool rate mixed into each player's
MIN_GAMES = 15            # games a player needs before he gets a chance
GREEN_LIGHT = 3.35
TEAM_MODEL = dict(intercept=1.097460, gfBlend=0.649684, oppGaBlend=0.158471,
                  gfLast10=-0.104467, oppGaLast10=0.137525, home=0.043517)
STATS = {"Goals": ("goals", "player_goal_scorer_anytime"),
         "Points": ("points", "player_points"),
         "Assists": ("assists", "player_assists")}
BOOK_SHORT = {"DraftKings": "DK", "FanDuel": "FD", "BetMGM": "MGM", "BetOnline.ag": "BOL",
              "BetRivers": "BR", "Bovada": "BOV"}
TOP_N = 15
LOG_COLS = ("player_id,game_id,season,game_date,team,opponent,goals,assists,points,sog,"
            "shots_against,goals_against,toi")


def select(query):
    """Every row of a Supabase query (paged; the query must have an order=)."""
    return engine.supabase_select_all(query)


def nhl_json(url):
    """GET from the NHL API, None on failure (the report notes the gap)."""
    return engine.fetch_json(url)


# ---------------------------------------------------------------------------
# TEAM MODEL — same as projectTeam() in index.html
# ---------------------------------------------------------------------------
def team_games(games, cur):
    """Per-team list of finished games, oldest first. A shootout winner's
    extra goal is removed for the model (gf/ga) but kept in the raw score."""
    by = {}
    for g in games:
        if g["away_score"] is None or g["home_score"] is None or g["game_state"] not in ("FINAL", "OFF"):
            continue
        a, h = g["away_score"], g["home_score"]
        if g["last_period_type"] == "SO":
            if a > h:
                a -= 1
            else:
                h -= 1
        for tm, opp, gf, ga, rgf, rga, home in ((g["away"], g["home"], a, h, g["away_score"], g["home_score"], False),
                                                 (g["home"], g["away"], h, a, g["home_score"], g["away_score"], True)):
            by.setdefault(tm, []).append(dict(id=g["id"], date=g["game_date"], season=g["season"], opp=opp,
                                              gf=gf, ga=ga, rgf=rgf, rga=rga, home=home))
    for v in by.values():
        v.sort(key=lambda x: x["date"])
    return by


def league_avg(ts, day, cur):
    c = cn = a = an = 0
    for v in ts.values():
        for g in v:
            if g["date"] >= day:
                continue
            a += g["gf"]
            an += 1
            if g["season"] == cur:
                c += g["gf"]
                cn += 1
    if cn >= 200:
        return c / cn
    return a / an if an else LEAGUE_AVG


def rates(ts, tm, day, cur):
    gs = [g for g in ts.get(tm, []) if g["date"] < day]
    prev = [g for g in gs if g["season"] != cur]
    now = [g for g in gs if g["season"] == cur]
    total = lambda arr, k: sum(g[k] for g in arr)
    pgf = total(prev, "gf") / len(prev) if prev else LEAGUE_AVG
    pga = total(prev, "ga") / len(prev) if prev else LEAGUE_AVG
    gf = (pgf * PRIOR_GAMES + total(now, "gf")) / (PRIOR_GAMES + len(now))
    ga = (pga * PRIOR_GAMES + total(now, "ga")) / (PRIOR_GAMES + len(now))
    l10 = now[-10:]
    miss = 10 - len(l10)
    return dict(gf=gf, ga=ga, gf10=(total(l10, "gf") + miss * gf) / 10, ga10=(total(l10, "ga") + miss * ga) / 10)


def project(ts, tm, opp, home, day, cur):
    L = league_avg(ts, day, cur)
    A, B = rates(ts, tm, day, cur), rates(ts, opp, day, cur)
    rel = lambda v: math.log(max(0.5, v) / L)
    m = TEAM_MODEL
    return math.exp(m["intercept"] + m["gfBlend"] * rel(A["gf"]) + m["oppGaBlend"] * rel(B["ga"]) +
                    m["gfLast10"] * rel(A["gf10"]) + m["oppGaLast10"] * rel(B["ga10"]) + (m["home"] if home else 0))


# ---------------------------------------------------------------------------
# PLAYER MODEL — same as renderHot() in index.html
# ---------------------------------------------------------------------------
def toi_min(t):
    m, s = str(t).split(":")
    return int(m) + int(s) / 60


def avg_toi(logs, cur):
    r = [x for x in logs if x["season"] == cur and x["toi"]]
    if len(r) < 5:
        r = [x for x in logs if x["toi"]]
    r = r[:25]
    return sum(toi_min(x["toi"]) for x in r) / len(r) if r else None


def role_bucket(pos, toi):
    if toi is None:
        return None
    if pos == "D":
        return "D1" if toi < 18.5 else ("D2" if toi < 21.5 else "D3")
    return "F1" if toi < 12.5 else ("F2" if toi < 15.5 else ("F3" if toi < 18 else "F4"))


def hits(logs, col):
    v = [r[col] for r in logs if r[col] is not None]
    return len(v), sum(1 for x in v if x > 0.5)


def implied(price):
    return -price / (-price + 100) if price < 0 else 100 / (price + 100)


def load_logs(ids):
    """Regular-season game logs per player, newest first, deduplicated."""
    by = {i: [] for i in ids}
    chunks = [ids[i:i + 12] for i in range(0, len(ids), 12)]
    fetch = lambda c: select(f"player_game_logs?player_id=in.({','.join(map(str, c))})&game_type=eq.2"
                             f"&select={LOG_COLS}&order=game_date.desc,game_id.desc,player_id.asc")
    with ThreadPoolExecutor(4) as ex:
        for rows in ex.map(fetch, chunks):
            seen = set()
            for r in rows:
                k = (r["player_id"], r["game_id"])
                if k not in seen:
                    seen.add(k)
                    by[r["player_id"]].append(r)
    return by


def goalie_sv(logs):
    rows = [r for r in logs if r["shots_against"] is not None]
    sa = sum(r["shots_against"] for r in rows)
    ga = sum(r["goals_against"] or 0 for r in rows)
    return dict(shrunk=((sa - ga) + LEAGUE_SV * SV_SHRINK) / (sa + SV_SHRINK), gp=len(rows),
                raw=(sa - ga) / sa if sa else None)


# ---------------------------------------------------------------------------
# TEAM FORM — last 10 games from NHL.com box scores
# ---------------------------------------------------------------------------
def team_form(ts, teams, day):
    """Last 10 regular-season games before `day` per team: raw goals, shots
    and special teams. Box scores that can't be read are counted and shown."""
    last = {tm: [g for g in ts.get(tm, []) if g["date"] < day][-10:] for tm in teams}
    ids = sorted({g["id"] for gs in last.values() for g in gs})
    with ThreadPoolExecutor(8) as ex:
        rails = dict(zip(ids, ex.map(lambda i: nhl_json(f"{engine.BASE}/gamecenter/{i}/right-rail"), ids)))
    out = {}
    for tm, gs in last.items():
        f = dict(n=len(gs), gf=sum(g["rgf"] for g in gs), ga=sum(g["rga"] for g in gs),
                 sf=0, sa=0, ppg=0, ppo=0, pkga=0, pko=0, boxes=0)
        for g in gs:
            st = {x["category"]: x for x in ((rails.get(g["id"]) or {}).get("teamGameStats") or [])}
            if "sog" not in st or "powerPlay" not in st:
                continue
            me, op = ("homeValue", "awayValue") if g["home"] else ("awayValue", "homeValue")
            f["boxes"] += 1
            f["sf"] += st["sog"][me]
            f["sa"] += st["sog"][op]
            a, b = map(int, str(st["powerPlay"][me]).split("/"))
            f["ppg"] += a
            f["ppo"] += b
            a, b = map(int, str(st["powerPlay"][op]).split("/"))
            f["pkga"] += a
            f["pko"] += b
        out[tm] = f
    return out


# ---------------------------------------------------------------------------
# REPORT
# ---------------------------------------------------------------------------
def fmt_odds(o):
    return "-" if o is None else (f"+{o}" if o > 0 else str(o))


def fmt_et(iso, with_date=False):
    if not iso:
        return "none yet"
    t = datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(engine.nhl_timezone())
    hm = f"{t.hour % 12 or 12}:{t.minute:02d} {'AM' if t.hour < 12 else 'PM'}"
    return f"{t:%b} {t.day}, {hm} ET" if with_date else f"{hm} ET"


def build(day):
    day_s = day.isoformat()
    cur = int(engine.season_for(day))
    prev = cur - 10001

    games = select(f"games?season=in.({prev},{cur})&game_type=eq.2&select=id,season,game_date,start_time_utc,"
                   f"away,home,away_score,home_score,game_state,last_period_type&order=game_date.asc,id.asc")
    players = {p["id"]: p for p in select("players?select=id,name,team,pos&order=id.asc")}
    lineups = select(f"daily_lineups?lineup_date=eq.{day_s}&select=*&order=team.asc,list_order.asc")
    odds = select(f"player_odds?game_date=eq.{day_s}&side=eq.Over&select=player_id,player_name,home,away,market,"
                  f"line,book,price,updated_at&order=player_name.asc,market.asc,book.asc")

    slate = sorted([g for g in games if g["game_date"] == day_s], key=lambda g: (g["start_time_utc"] or "", g["id"]))
    lines = []
    out = lines.append
    out(f"ICE ENGINE SLATE REPORT  {day_s}")
    if not slate:
        out("No regular-season games on this date.")
        return "\n".join(lines) + "\n"

    ts = team_games(games, cur)
    teams = [t for g in slate for t in (g["away"], g["home"])]
    on_slate = set(teams)
    lineups = [l for l in lineups if l["team"] in on_slate]

    goalie_rows = [l for l in lineups if l["slot"] == "goalie"]
    out(f"Lineups pulled: {fmt_et(max((l['updated_at'] for l in lineups), default=None), True)}")
    out(f"Prices pulled:  {fmt_et(max((o['updated_at'] for o in odds), default=None), True)}")
    out(f"Goalies pulled: {fmt_et(max((l['updated_at'] for l in goalie_rows), default=None), True)}")
    out("Times are US Eastern. Read-only: built from the same models as the board.")

    skaters, seen = [], set()
    for l in lineups:
        if l["status"] == "projected" and l["slot"] in ("line", "pair") and l["player_id"] and l["player_id"] not in seen:
            seen.add(l["player_id"])
            skaters.append(l)
    goalie_ids = [l["player_id"] for l in goalie_rows if l["player_id"]]
    logs = load_logs(sorted({l["player_id"] for l in skaters} | set(goalie_ids)))

    # ---- games ----
    proj = {}
    for g in slate:
        proj[g["away"]] = project(ts, g["away"], g["home"], False, day_s, cur)
        proj[g["home"]] = project(ts, g["home"], g["away"], True, day_s, cur)
    out("\nGAMES (start, projected goals, model game total; book game totals are not pulled)")
    for g in slate:
        a, h = g["away"], g["home"]
        green = [t for t in (a, h) if proj[t] >= GREEN_LIGHT]
        out(f"- {fmt_et(g['start_time_utc'])}  {a} {proj[a]:.2f} @ {h} {proj[h]:.2f}  "
            f"(total {proj[a] + proj[h]:.2f}){'  green light: ' + ', '.join(green) if green else ''}")

    # ---- goalies ----
    out("\nGOALIES (shrunk two-season save %, raw save % and games)")
    unconfirmed = []
    for tm in teams:
        gl = sorted([l for l in goalie_rows if l["team"] == tm and l["status"] == "projected"], key=lambda l: l["list_order"])
        if not gl:
            out(f"- {tm}: no goalie listed")
            unconfirmed.append(f"{tm}: no goalie listed")
            continue
        start = next((l for l in gl if l["confirmed_starter"]), gl[0])

        def sv_txt(l):
            if not l["player_id"]:
                return "no stats (unmatched name)"
            s = goalie_sv(logs.get(l["player_id"], []))
            return f"{s['shrunk']:.3f} ({s['raw']:.3f} raw, {s['gp']} GP)" if s["raw"] is not None else f"{s['shrunk']:.3f} (0 GP)"
        label = "CONFIRMED" if start["confirmed_starter"] else "expected"
        others = [l for l in gl if l is not start]
        out(f"- {tm}: {start['player_name']} {label} {sv_txt(start)}" +
            ("" if start["confirmed_starter"] or not others else
             "  | also listed: " + ", ".join(f"{l['player_name']} {sv_txt(l)}" for l in others)))
        if not start["confirmed_starter"]:
            unconfirmed.append(f"{tm}: {start['player_name']} (expected, not confirmed)")

    # ---- injuries ----
    out("\nINJURED / OUT (scratches in brackets)")
    for tm in teams:
        rows = [l for l in lineups if l["team"] == tm and l["status"] != "projected"]
        inj = [f"{l['player_name']} ({l['detail'] or l['status']})" for l in rows if l["status"] != "scratched"]
        scr = [l["player_name"] for l in rows if l["status"] == "scratched"]
        out(f"- {tm}: {'; '.join(inj) or 'none listed'}{' [' + ', '.join(scr) + ']' if scr else ''}")
    noted = [l for l in skaters if l["detail"]]
    out("Questionable: " + (", ".join(f"{l['player_name']} {l['team']} ({l['detail']})" for l in noted)
                            if noted else "no projected skater carries a questionable or day-to-day note."))

    # ---- team form ----
    form = team_form(ts, teams, day_s)
    out("\nTEAM FORM, last 10 regular-season games (per game: GF / GA | shots for / against | PP | PK)")
    for tm in teams:
        f = form[tm]
        if not f["n"]:
            out(f"- {tm}: no games yet")
            continue
        shots = f"{f['sf'] / f['boxes']:.1f} / {f['sa'] / f['boxes']:.1f}" if f["boxes"] else "n/a"
        pp = f"{f['ppg'] / f['ppo'] * 100:.1f}% ({f['ppg']}/{f['ppo']})" if f["ppo"] else "n/a"
        pk = f"{(1 - f['pkga'] / f['pko']) * 100:.1f}%" if f["pko"] else "n/a"
        gap = f"  [{f['boxes']}/{f['n']} box scores read]" if f["boxes"] < f["n"] else ""
        out(f"- {tm}: {f['gf'] / f['n']:.1f} / {f['ga'] / f['n']:.1f} | {shots} | PP {pp} | PK {pk}{gap}")

    # ---- players ----
    priced_ids = {o["player_id"] for o in odds if o["player_id"]}
    res = {}
    for stat, (col, market) in STATS.items():
        best, books = {}, {}
        for o in odds:
            if o["market"] != market or float(o["line"]) != 0.5 or not o["player_id"]:
                continue
            b = best.get(o["player_id"])
            if not b or o["price"] > b["price"]:
                best[o["player_id"]] = o
            books.setdefault(o["player_id"], {})[o["book"]] = o["price"]
        base = []
        for l in skaters:
            lg = logs[l["player_id"]]
            n, over = hits(lg, col)
            if n < MIN_GAMES:
                continue
            pos = (players.get(l["player_id"]) or {}).get("pos") or "F"
            toi = avg_toi(lg, cur)
            base.append(dict(l=l, lg=lg, n=n, over=over, pos=pos, toi=toi, bucket=role_bucket(pos, toi)))
        pool, tot_o, tot_n = {}, 0, 0
        for r in base:
            tot_o += r["over"]
            tot_n += r["n"]
            if r["bucket"]:
                b = pool.setdefault(r["bucket"], [0, 0, 0])
                b[0] += r["over"]
                b[1] += r["n"]
                b[2] += 1
        all_rate = tot_o / tot_n if tot_n else 0.3
        for r in base:
            b = pool.get(r["bucket"])
            p = b[0] / b[1] if b and b[2] >= 8 else all_rate
            adj = (r["over"] + SHRINK_K * p) / (r["n"] + SHRINK_K)
            pid = r["l"]["player_id"]
            pc = best.get(pid)
            l10n, l10o = hits(r["lg"][:10], col)
            sh = [x["sog"] for x in r["lg"][:10] if x["sog"] is not None]
            e = res.setdefault(pid, dict(name=r["l"]["player_name"], team=r["l"]["team"], pp=r["l"]["pp_unit"],
                                         toi=r["toi"], shpg=sum(sh) / len(sh) if sh else None,
                                         note=r["l"]["detail"]))
            e[stat] = dict(adj=adj, l10=f"{l10o}/{l10n}", price=pc["price"] if pc else None,
                           book=pc["book"] if pc else None, edge=(adj - implied(pc["price"])) * 100 if pc else None,
                           dk=books.get(pid, {}).get("DraftKings"), fd=books.get(pid, {}).get("FanDuel"))

    priced = [p for pid, p in res.items() if pid in priced_ids and any(s in p and p[s]["price"] is not None for s in STATS)]
    q = lambda p: " [Q]" if p["note"] else ""
    ppu = lambda p: f"PP{p['pp']}" if p["pp"] else "no PP"
    num = lambda v, f="{:.1f}": f.format(v) if v is not None else "-"

    def leg(x):
        if x is None:
            return "n/a"
        if x["price"] is None:
            return f"{x['adj'] * 100:.0f}% no price, L10 {x['l10']}"
        return f"{x['adj'] * 100:.0f}% {fmt_odds(x['price'])} {BOOK_SHORT.get(x['book'], x['book'])} {x['edge']:+.1f}, L10 {x['l10']}"

    def row(i, p, s, with_stat=False):
        x = p[s]
        return (f"{i}. {p['name']}{q(p)} {p['team']}{' ' + s if with_stat else ''} {x['adj'] * 100:.0f}%; "
                f"best {fmt_odds(x['price'])} {BOOK_SHORT.get(x['book'], x['book'])}; edge {x['edge']:+.1f}; "
                f"DK {fmt_odds(x['dk'])}; FD {fmt_odds(x['fd'])}; L10 {x['l10']}; "
                f"{num(p['shpg'])} shots; {num(p['toi'])} min; {ppu(p)}")

    for s in STATS:
        out(f"\nTOP {TOP_N} {s.upper()} BY ROLE-ADJUSTED CHANCE")
        ranked = sorted([p for p in priced if s in p and p[s]["price"] is not None], key=lambda p: -p[s]["adj"])
        for i, p in enumerate(ranked[:TOP_N], 1):
            out(row(i, p, s))
    out(f"\nTOP {TOP_N} BY EDGE (all three markets)")
    legs = [(p, s) for p in priced for s in STATS if s in p and p[s]["price"] is not None]
    for i, (p, s) in enumerate(sorted(legs, key=lambda r: -r[0][r[1]]["edge"])[:TOP_N], 1):
        out(row(i, p, s, with_stat=True))
    out(f"{sum(1 for p, s in legs if p[s]['edge'] > 0)} of {len(legs)} priced legs show a positive edge at the best book.")

    out("\nALL PRICED SKATERS (shots/game last 10, minutes, PP unit | G | P | A: chance, best price, edge, last 10)")
    for tm in teams:
        out(tm)
        for p in sorted([p for p in priced if p["team"] == tm], key=lambda p: -(p.get("Points") or {"adj": 0})["adj"]):
            out(f"- {p['name']}{q(p)} ({num(p['shpg'])}, {num(p['toi'])}, {ppu(p)}): "
                f"G {leg(p.get('Goals'))} | P {leg(p.get('Points'))} | A {leg(p.get('Assists'))}")

    # ---- data checks ----
    out("\nDATA CHECKS")
    priced_games = {(o["away"], o["home"]) for o in odds}
    no_price = [f"{g['away']} @ {g['home']}" for g in slate if (g["away"], g["home"]) not in priced_games]
    out("Games with no prices: " + (", ".join(no_price) if no_price else "none"))
    no_lineup = [tm for tm in teams if not any(l["team"] == tm for l in lineups)]
    if no_lineup:
        out("Teams with no lineup: " + ", ".join(no_lineup))
    status = {l["player_id"]: l for l in lineups if l["player_id"]}
    missing = []
    for pid in sorted(priced_ids - {l["player_id"] for l in skaters}):
        name = next(o["player_name"] for o in odds if o["player_id"] == pid)
        l = status.get(pid)
        team = (players.get(pid) or {}).get("team", "?")
        missing.append(f"{name} {team} ({'listed ' + l['status'] + (', ' + l['detail'] if l['detail'] else '') if l else 'not on any lineup'})")
    unmatched = sorted({f"{o['player_name']} ({o['away']} @ {o['home']})" for o in odds if not o["player_id"]})
    missing += [f"{u}: price not matched to a player" for u in unmatched]
    out("Priced players missing from the projected lineups:" + (" none" if not missing else ""))
    for m in missing:
        out(f"- {m}")
    out("Unconfirmed goalies:" + (" none" if not unconfirmed else ""))
    for u in unconfirmed:
        out(f"- {u}")
    # The same book price on two players of one team in one market is
    # usually a feed mislabel (e.g. two players sharing a name).
    dup = {}
    for o in odds:
        if o["player_id"]:
            team = (players.get(o["player_id"]) or {}).get("team")
            dup.setdefault((team, o["market"], o["line"], o["book"], o["price"]), set()).add(o["player_name"])
    shared_name = sorted({" / ".join(sorted(v)) for v in dup.values()
                          if len(v) > 1 and len({n.split(" (")[0] for n in v}) == 1})
    if shared_name:
        out("Possible mislabeled prices (same-name players with an identical price): " + "; ".join(shared_name))
    if engine.FAILED_URLS:
        out(f"NHL API requests that failed: {len(engine.FAILED_URLS)} (team form may be incomplete)")
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Write a read-only plain-text report of a day's slate.")
    parser.add_argument("--date", default="", help="YYYY-MM-DD; default is today (US Eastern)")
    parser.add_argument("--out", default="", help="file to write; default prints to stdout")
    parser.add_argument("--only-at", default="",
                        help="for scheduled runs: Eastern times to run at, e.g. '11:00,16:30'; other "
                             "triggers exit quietly (see SCHEDULE GATE in ice_engine_daily_pull.py)")
    args = parser.parse_args(argv)

    go, _slot, slot_day = engine.gate_on_schedule(args.only_at)
    if not go:
        return
    if not (engine.SUPABASE_URL and engine.SUPABASE_KEY):
        sys.exit("SUPABASE_URL and SUPABASE_KEY must be set (see README).")
    day = date.fromisoformat(args.date) if args.date.strip() else (slot_day or engine.nhl_today())

    text = build(day)
    if not args.out:
        sys.stdout.write(text)
        return
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"Wrote {args.out} ({text.count(chr(10))} lines) for {day}.")


if __name__ == "__main__":
    main()
