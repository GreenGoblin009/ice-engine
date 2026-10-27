"""
Ice Engine - Form Sheet
========================
Reads every priced skater's game-by-game "form" (did he get a point / goal /
assist in each of his last 20 regular-season games) and lists who lines up
for tonight, using the checks the user uses by hand:

  1. price       points -130 or better (assists and goals: his best price is
                 not shorter than his last-20 hit rate says it should be)
  2. hit rate    last 10 and last 20 at or above what the price implies
  3. steady      points/assists: never missed more than 2 games in a row in
                 his last 20 (not used for goals, they are too rare)
  4. shots       last-10 shots per game (forwards 2.0+, defensemen 1.5+)
  5. venue       tonight's home/away hit rate this season is not far below
                 his season rate (skipped under 4 games)
  6. no hot-streak penalty: skip points 3 of 3, skip assists 2+ of last 3

It also prints the model chance (same role-adjusted rate as the slate
report) so the bars and the stats sit side by side. It only reads (Supabase)
and never writes to the database.

Usage:
  python tools/form_report.py --out reports/form_latest.txt [--date YYYY-MM-DD]

Needs SUPABASE_URL and SUPABASE_KEY in the environment.
"""
import argparse
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import ice_engine_daily_pull as engine  # noqa: E402
import slate_report as sr  # noqa: E402

COLS = ("player_id,game_id,season,game_date,team,opponent,home_road,goals,assists,points,sog,toi")
STATS = [("Points", "points", "player_points"),
         ("Assists", "assists", "player_assists"),
         ("Goals", "goals", "player_goal_scorer_anytime")]


def load(ids):
    by = {i: [] for i in ids}
    chunks = [ids[i:i + 12] for i in range(0, len(ids), 12)]
    fetch = lambda c: sr.select(f"player_game_logs?player_id=in.({','.join(map(str, c))})&game_type=eq.2"
                                f"&select={COLS}&order=game_date.desc,game_id.desc,player_id.asc")
    with ThreadPoolExecutor(4) as ex:
        for rows in ex.map(fetch, chunks):
            seen = set()
            for r in rows:
                k = (r["player_id"], r["game_id"])
                if k not in seen:
                    seen.add(k)
                    by[r["player_id"]].append(r)
    return by


def runs(vals):
    """vals newest first (True = hit). Returns (longest miss run, current miss run)."""
    longest = cur = 0
    for v in vals:
        cur = 0 if v else cur + 1
        longest = max(longest, cur)
    now = 0
    for v in vals:
        if v:
            break
        now += 1
    return longest, now


def bar_text(vals):
    """Oldest on the left, newest on the right; X = hit, . = miss."""
    return "".join("X" if v else "." for v in reversed(vals))


def build(day):
    day_s = day.isoformat()
    cur = int(engine.season_for(day))
    prev = cur - 10001
    games = sr.select(f"games?season=in.({prev},{cur})&game_type=eq.2&select=id,season,game_date,start_time_utc,"
                      f"away,home&order=game_date.asc,id.asc")
    slate = sorted([g for g in games if g["game_date"] == day_s], key=lambda g: (g["start_time_utc"] or "", g["id"]))
    lines = []
    out = lines.append
    out(f"ICE ENGINE FORM SHEET  {day_s}")
    if not slate:
        out("No regular-season games on this date.")
        return "\n".join(lines) + "\n"
    game_of = {}
    for g in slate:
        game_of[g["away"]] = (g, False)
        game_of[g["home"]] = (g, True)
    players = {p["id"]: p for p in sr.select("players?select=id,name,team,pos&order=id.asc")}
    odds = sr.select(f"player_odds?game_date=eq.{day_s}&side=eq.Over&select=player_id,player_name,home,away,market,"
                     f"line,book,price,updated_at&order=player_name.asc,market.asc,book.asc")
    out(f"Prices pulled: {sr.fmt_et(max((o['updated_at'] for o in odds), default=None), True)}")
    out("X = got it, . = missed. Oldest game on the left, newest on the right. Last 20 regular-season games.")
    out("Every player shows tonight's opponent and start time so the game can be checked.")

    ids = sorted({o["player_id"] for o in odds if o["player_id"] and o["player_id"] in players})
    logs = load(ids)

    # role pools for the model chance (same method as slate_report)
    info = {}
    for pid in ids:
        p = players[pid]
        tm = p["team"]
        if tm not in game_of or p.get("pos") == "G":
            continue
        lg = logs.get(pid, [])
        if len(lg) < 10:
            continue
        info[pid] = dict(p=p, lg=lg, toi=sr.avg_toi(lg, cur))
    pools = {}
    for stat, col, _m in STATS:
        pool, to, tn = {}, 0, 0
        for pid, d in info.items():
            n, o = sr.hits(d["lg"], col)
            b = sr.role_bucket(d["p"].get("pos") or "F", d["toi"])
            to += o
            tn += n
            if b:
                x = pool.setdefault(b, [0, 0, 0])
                x[0] += o
                x[1] += n
                x[2] += 1
        pools[col] = (pool, to / tn if tn else 0.3)

    results = {s[1]: [] for s in STATS}
    for pid, d in info.items():
        p, lg = d["p"], d["lg"]
        tm = p["team"]
        g, home = game_of[tm]
        opp = g["home"] if not home else g["away"]
        sh = [x["sog"] for x in lg[:10] if x["sog"] is not None]
        shpg = sum(sh) / len(sh) if sh else None
        is_d = p.get("pos") == "D"
        for stat, col, market in STATS:
            best = None
            books = {}
            for o in odds:
                if o["player_id"] != pid or o["market"] != market or float(o["line"]) != 0.5:
                    continue
                books[o["book"]] = o["price"]
                if best is None or o["price"] > best:
                    best = o["price"]
            if best is None:
                continue
            vals = [bool(x[col] and x[col] > 0.5) for x in lg if x[col] is not None]
            if len(vals) < 10:
                continue
            l20, l10, l5, l3 = vals[:20], vals[:10], vals[:5], vals[:3]
            h20, h10, h3 = sum(l20), sum(l10), sum(l3)
            longest, now = runs(l20)
            season = [x for x in lg if x["season"] == cur and x[col] is not None]
            s_rate = sum(1 for x in season if x[col] > 0.5) / len(season) if season else None
            venue = [x for x in season if x["home_road"] == ("H" if home else "R")]
            v_n = len(venue)
            v_h = sum(1 for x in venue if x[col] > 0.5)
            hr = "H" if home else "R"
            l20v = [x for x in lg[:20] if x["home_road"] == hr and x[col] is not None]
            lv_n, lv_h = len(l20v), sum(1 for x in l20v if x[col] > 0.5)
            s_n, s_h = len(season), sum(1 for x in season if x[col] > 0.5)
            imp = sr.implied(best)
            pool, allr = pools[col]
            n_all, o_all = sr.hits(lg, col)
            chance = None
            if n_all >= sr.MIN_GAMES:
                b = sr.role_bucket(p.get("pos") or "F", d["toi"])
                pr = pool.get(b)
                pr = pr[0] / pr[1] if pr and pr[2] >= 8 else allr
                chance = (o_all + sr.SHRINK_K * pr) / (n_all + sr.SHRINK_K)

            ck = {}
            ck["price"] = (best >= -130) if col == "points" else (h20 / len(l20) >= imp)
            ck["hit rate"] = (h10 / len(l10) >= imp) and (h20 / len(l20) >= imp)
            if col != "goals":
                ck["steady"] = longest <= 2
            if shpg is not None:
                ck["shots"] = shpg >= (1.5 if is_d else 2.0)
            if v_n >= 4 and s_rate is not None:
                ck["venue"] = (v_h / v_n) >= s_rate - 0.20
            if col == "points":
                ck["streak"] = h3 < 3
            elif col == "assists":
                ck["streak"] = h3 < 2
            results[col].append(dict(
                name=p["name"], team=tm, opp=opp, home=home, when=sr.fmt_et(g["start_time_utc"]),
                pos=p.get("pos") or "F", price=best, dk=books.get("DraftKings"), fd=books.get("FanDuel"),
                chance=chance, h10=h10, n10=len(l10), h20=h20, n20=len(l20), h3=h3, longest=longest, now=now,
                shpg=shpg, bars=bar_text(l20), v=(v_h, v_n), lv=(lv_h, lv_n), sea=(s_h, s_n), ck=ck, imp=imp))

    def head(r):
        at = "vs" if r["home"] else "@"
        ch = f"{r['chance'] * 100:.0f}%" if r["chance"] is not None else "n/a"
        sh = f"{r['shpg']:.1f}" if r["shpg"] is not None else "-"
        ven = 'home' if r['home'] else 'away'
        v = (f" | {ven} season {r['v'][0]}/{r['v'][1]}, {ven} in L20 {r['lv'][0]}/{r['lv'][1]}")
        return (f"{r['name']} {r['team']} {at} {r['opp']} {r['when']} | {sr.fmt_odds(r['price'])} "
                f"(DK {sr.fmt_odds(r['dk']) if r['dk'] is not None else '-'}, FD {sr.fmt_odds(r['fd']) if r['fd'] is not None else '-'}) | "
                f"model {ch} | L10 {r['h10']}/{r['n10']} L20 {r['h20']}/{r['n20']} season {r['sea'][0]}/{r['sea'][1]} | max miss run {r['longest']}, "
                f"missed last {r['now']} | shots L10 {sh}{v} | {r['bars']}")

    for stat, col, _m in STATS:
        rows = results[col]
        full = [r for r in rows if all(r["ck"].values())]
        near = [r for r in rows if not all(r["ck"].values()) and sum(1 for v in r["ck"].values() if not v) == 1]
        by_chance = lambda r: -(r["chance"] if r["chance"] is not None else -1)
        out(f"\n=== {stat.upper()}: LINES UP on every check ({len(full)} of {len(rows)} priced) ===")
        for r in sorted(full, key=by_chance)[:25]:
            out("- " + head(r))
        if not full:
            out("- none")
        out(f"\n--- {stat.upper()}: misses exactly one check ({len(near)}) ---")
        for r in sorted(near, key=by_chance)[:20]:
            failed = [k for k, v in r["ck"].items() if not v][0]
            out(f"- [{failed}] " + head(r))
    out("\nChecks: price (points -130 or better; assists/goals last-20 rate at or above the price), hit rate "
        "(L10 and L20 at or above the price), steady (points/assists never missed more than 2 in a row in last 20), "
        "shots (F 2.0+, D 1.5+ per game, last 10), venue (tonight's home/away rate not 20+ points under his season "
        "rate, 4+ games), streak (points not 3 of 3, assists not 2+ of last 3).")
    out("Lineups and power-play units are NOT in this report: check the slate report once they post.")
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default="")
    ap.add_argument("--out", default="")
    a = ap.parse_args(argv)
    if not (engine.SUPABASE_URL and engine.SUPABASE_KEY):
        sys.exit("SUPABASE_URL and SUPABASE_KEY must be set.")
    day = date.fromisoformat(a.date) if a.date.strip() else engine.nhl_today()
    text = build(day)
    if not a.out:
        sys.stdout.write(text)
        return
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"Wrote {a.out} ({text.count(chr(10))} lines) for {day}.")


if __name__ == "__main__":
    main()
