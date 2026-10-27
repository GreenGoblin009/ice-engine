"""
Ice Engine - Pattern Backtest
=============================
Tests the patterns the user reads off the game-by-game charts, on every NHL
skater's regular-season game logs (last season + this season). For each
player-game it uses ONLY games played before it, builds a plain baseline
chance (his last-60-game rate shrunk toward the league rate for his position),
then asks: when a pattern is present, does he hit more or less than that
baseline says?

  venue edge     his rate in the same venue as tonight (last 20 there) minus his last-20 rate
  alternating    hit/miss flips 5+ times in his last 8 games (and what happened last game)
  steady         never missed more than 2 in a row in his last 20 / missed 4+ in a row
  even blocks    last 20 split into four 5-game blocks; every block has hits
  miss run       steady players after 0, 1, 2 straight misses (the "due" idea)
  shot volume    last-10 shots per game
  goal heat      3+ goals in last 10 AND 3+ shots a game over the last 10
  hot streak     hit in each of last 3

Result per bucket: n, actual hit %, baseline %, difference, z-score (|z| 2+ is
unlikely to be luck), and the same split by season so a real effect shows up
in both. Many buckets are tested, so a lone |z| of 2-3 can still be luck.

Read-only. Needs SUPABASE_URL and SUPABASE_KEY. Writes reports/pattern_backtest.md
"""
import math
import os
import sys
from collections import defaultdict
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import ice_engine_daily_pull as engine  # noqa: E402
import slate_report as sr  # noqa: E402

K = 10          # shrink: games of league rate mixed into the baseline
MIN_PRIOR = 20  # games a player needs before a game counts
MARKETS = [("points", "Points"), ("assists", "Assists"), ("goals", "Goals")]


def load_rows(prev, cur):
    pos = {p["id"]: (p.get("pos") or "F") for p in sr.select("players?select=id,pos&order=id.asc")}
    rows = sr.select(f"player_game_logs?season=in.({prev},{cur})&game_type=eq.2"
                     "&select=player_id,game_id,season,game_date,home_road,goals,assists,points,sog,shot_attempts,toi"
                     "&order=player_id.asc,game_date.asc,game_id.asc")
    by, seen = defaultdict(list), set()
    for r in rows:
        k = (r["player_id"], r["game_id"])
        if k in seen or pos.get(r["player_id"]) == "G" or not r["toi"]:
            continue
        seen.add(k)
        by[r["player_id"]].append(r)
    return by, pos


def runs(prior):
    """prior newest first, 1 = hit. (longest miss run, current miss run)"""
    longest = cur = 0
    for v in prior:
        cur = 0 if v else cur + 1
        longest = max(longest, cur)
    now = 0
    for v in prior:
        if v:
            break
        now += 1
    return longest, now


def run(prev, cur):
    by, pos = load_rows(prev, cur)
    lg = {}
    for col, _ in MARKETS:
        for g in ("F", "D"):
            n = h = 0
            for pid, rs in by.items():
                if (pos.get(pid) == "D") != (g == "D"):
                    continue
                for r in rs:
                    if r[col] is not None:
                        n += 1
                        h += 1 if r[col] > 0.5 else 0
            lg[(col, g)] = h / n if n else 0.3
    stats = defaultdict(lambda: [0, 0.0, 0.0, 0.0])  # n, hits, baseline sum, variance sum

    def add(col, feat, bucket, season, hit, base):
        for s in (season, "all"):
            a = stats[(col, feat, bucket, s)]
            a[0] += 1
            a[1] += hit
            a[2] += base
            a[3] += base * (1 - base)

    for pid, rs in by.items():
        g = "D" if pos.get(pid) == "D" else "F"
        for col, _ in MARKETS:
            v = [1 if (r[col] or 0) > 0.5 else 0 for r in rs]
            for i in range(MIN_PRIOR, len(rs)):
                row = rs[i]
                if row["season"] not in (prev, cur) or row[col] is None:
                    continue
                season = "this season" if row["season"] == cur else "last season"
                hit = v[i]
                win = v[max(0, i - 60):i]
                base = (sum(win) + K * lg[(col, g)]) / (len(win) + K)
                p20 = v[i - 20:i][::-1]
                r20 = sum(p20) / 20
                longest, now = runs(p20)
                # venue
                same = [v[j] for j in range(i - 1, -1, -1) if rs[j]["home_road"] == row["home_road"]][:20]
                if len(same) >= 8:
                    e = sum(same) / len(same) - r20
                    b = ("much worse here (-15 pts or more)" if e <= -.15 else
                         "worse here (-5 to -15)" if e <= -.05 else
                         "same (within 5)" if e < .05 else
                         "better here (+5 to +15)" if e < .15 else "much better here (+15 or more)")
                    add(col, "venue edge (same-venue last 20 vs last 20)", b, season, hit, base)
                # alternating
                p8 = v[i - 8:i]
                flips = sum(1 for a, b2 in zip(p8, p8[1:]) if a != b2)
                if flips >= 5:
                    add(col, "alternating (5+ flips in last 8)", "last game hit" if p8[-1] else "last game MISS", season, hit, base)
                # steady
                add(col, "steady (longest miss run in last 20)",
                    "2 or less" if longest <= 2 else ("3" if longest == 3 else "4 or more"), season, hit, base)
                # even blocks
                blocks = [sum(p20[k:k + 5]) for k in range(0, 20, 5)]
                need = 1 if col == "goals" else 2
                add(col, f"blocks (every 5-game block has {need}+ hits)", "yes" if min(blocks) >= need else "no", season, hit, base)
                # miss run for steady players
                if longest <= 2:
                    add(col, "steady players: straight misses right now", f"{min(now, 3)}{'+' if now >= 3 else ''}", season, hit, base)
                # shots
                sg = [r["sog"] for r in rs[i - 10:i] if r["sog"] is not None]
                sg5 = [r["sog"] for r in rs[i - 5:i] if r["sog"] is not None]
                if len(sg) >= 8:
                    s10 = sum(sg) / len(sg)
                    b = "under 1.5" if s10 < 1.5 else "1.5-2.2" if s10 < 2.2 else "2.2-3.0" if s10 < 3.0 else "3.0+"
                    add(col, "shots per game, last 10", b, season, hit, base)
                    if col == "goals":
                        g10 = sum(1 for r in rs[i - 10:i] if (r["goals"] or 0) > 0)
                        sea = [r["sog"] for r in rs[:i] if r["season"] == row["season"] and r["sog"] is not None]
                        s_avg = sum(sea) / len(sea) if sea else 0
                        heat = g10 >= 3 and s10 >= 3.0 and sg5 and (sum(sg5) / len(sg5)) >= s_avg
                        add(col, "goal heat (3+ goals in last 10, 3+ shots, last 5 above season rate)", "yes" if heat else "no", season, hit, base)
                # shot attempts (forwards and defensemen shown separately)
                at = [r["shot_attempts"] for r in rs[i - 10:i] if r.get("shot_attempts") is not None]
                if len(at) >= 8:
                    a10 = sum(at) / len(at)
                    lab = "D" if g == "D" else "F"
                    cut = (2, 3, 4, 5) if g == "D" else (3, 4, 5, 6)
                    b = (f"{lab}: under {cut[0]}" if a10 < cut[0] else f"{lab}: {cut[0]}-{cut[1]}" if a10 < cut[1]
                         else f"{lab}: {cut[1]}-{cut[2]}" if a10 < cut[2] else f"{lab}: {cut[2]}-{cut[3]}" if a10 < cut[3] else f"{lab}: {cut[3]}+")
                    add(col, "shot attempts per game, last 10", b, season, hit, base)
                    if g == "F":
                        c4 = sum(1 for a in at if a >= 4)
                        b = "9-10 of 10 games with 4+ attempts" if c4 >= 9 else "7-8 of 10" if c4 >= 7 else "5-6 of 10" if c4 >= 5 else "0-4 of 10"
                        add(col, "forwards: games with 4+ attempts, last 10", b, season, hit, base)
                        c5 = sum(1 for a in at if a >= 5)
                        b = "8-10 of 10 games with 5+ attempts" if c5 >= 8 else "5-7 of 10" if c5 >= 5 else "0-4 of 10"
                        add(col, "forwards: games with 5+ attempts, last 10", b, season, hit, base)
                # hot streak
                add(col, "hit each of last 3", "yes" if sum(v[i - 3:i]) == 3 else "no", season, hit, base)
                # long-history venue edge: same-venue rate over ALL prior games (min 30 there) vs overall rate (min 60 games)
                if i >= 60:
                    same_all = [v[j] for j in range(i) if rs[j]["home_road"] == row["home_road"]]
                    if len(same_all) >= 30:
                        e2 = sum(same_all) / len(same_all) - sum(v[:i]) / i
                        b = ("venue much worse (-10 or more)" if e2 <= -.10 else "venue a bit worse (-4 to -10)" if e2 <= -.04 else
                             "venue same (within 4)" if e2 < .04 else "venue a bit better (+4 to +10)" if e2 < .10 else "venue much better (+10 or more)")
                        add(col, "long-history venue edge (all prior same-venue games, 30+ there, vs all prior games)", b, season, hit, base)
                # recency: L20 and L10 rate minus the 60-game baseline
                d20 = sum(p20) / 20 - base
                b = "L20 well above baseline (+8 or more)" if d20 >= .08 else "L20 above (+3 to +8)" if d20 >= .03 else "L20 near baseline" if d20 > -.03 else "L20 below (-3 to -8)" if d20 > -.08 else "L20 well below (-8 or less)"
                add(col, "recency: last-20 rate minus 60-game baseline", b, season, hit, base)
                d10 = sum(v[i - 10:i]) / 10 - base
                b = "L10 well above baseline (+15 or more)" if d10 >= .15 else "L10 above (+5 to +15)" if d10 >= .05 else "L10 near baseline" if d10 > -.05 else "L10 below (-5 to -15)" if d10 > -.15 else "L10 well below (-15 or less)"
                add(col, "recency: last-10 rate minus 60-game baseline", b, season, hit, base)
                # volume without results (and volume with results), forwards, using shot attempts
                if g == "F":
                    at10 = [r["shot_attempts"] for r in rs[i - 10:i] if r.get("shot_attempts") is not None]
                    sg10 = [r["sog"] for r in rs[i - 10:i] if r["sog"] is not None]
                    if len(at10) >= 8 and len(sg10) >= 8:
                        a10 = sum(at10) / len(at10)
                        s10 = sum(sg10) / len(sg10)
                        gl10 = sum(1 for r in rs[i - 10:i] if (r["goals"] or 0) > 0)
                        if a10 >= 5 or s10 >= 3:
                            b = "high volume, 0-1 goals in last 10 (sleeper)" if gl10 <= 1 else "high volume, 2 goals in last 10" if gl10 == 2 else "high volume, 3+ goals in last 10 (hot)"
                            add(col, "high volume (5+ attempts or 3+ shots a game) by goals in last 10", b, season, hit, base)
                        if 3.5 <= a10 < 5 and 1.5 <= s10 < 3:
                            b = "mid volume, 0-1 goals in last 10" if gl10 <= 1 else "mid volume, 2+ goals in last 10"
                            add(col, "mid volume by goals in last 10", b, season, hit, base)
                # the user's combined read: L10 form + same-venue L10 form + catching him after an off night
                thr = {"points": 6, "assists": 4, "goals": 3}[col]
                l10h = sum(v[i - 10:i])
                sv10 = [v[j] for j in range(i - 1, -1, -1) if rs[j]["home_road"] == row["home_road"]][:10]
                if len(sv10) >= 8:
                    vh = sum(sv10) * 10 / len(sv10)
                    last1, last2 = v[i - 1], v[i - 2]
                    off = (not last1)  # missed last game (1 or 2 straight misses)
                    if l10h >= thr:
                        if vh >= thr:
                            add(col, "USER METHOD: L10 form and same-venue L10 form both at the bar (points 6+, assists 4+, goals 3+)",
                                "both at the bar, hit last game" if not off else "both at the bar, missed last game (off night)", season, hit, base)
                            if off and not (not last1 and not last2 and v[i - 3] == 0):
                                add(col, "USER METHOD: both at the bar and 1-2 straight misses (off night or two)", "yes", season, hit, base)
                        else:
                            add(col, "USER METHOD: L10 form at the bar but same-venue L10 below the bar", "venue form weak", season, hit, base)
                    else:
                        if vh >= thr:
                            add(col, "USER METHOD: L10 below the bar but same-venue L10 at the bar", "venue form strong only", season, hit, base)
                # how long hot runs last: current hit run length (0 if last game missed)
                run_now = 0
                for vv in reversed(v[:i]):
                    if vv:
                        run_now += 1
                    else:
                        break
                add(col, "current hit run (games in a row with a hit)", "0" if run_now == 0 else "1" if run_now == 1 else "2" if run_now == 2 else "3" if run_now == 3 else "4+", season, hit, base)
                add(col, "all games (baseline check)", "all", season, hit, base)
    return stats


def fmt(a):
    n, h, b, var = a
    if not n:
        return None
    z = (h - b) / math.sqrt(var) if var else 0
    return n, h / n * 100, b / n * 100, (h - b) / n * 100, z


def main():
    if not (engine.SUPABASE_URL and engine.SUPABASE_KEY):
        sys.exit("SUPABASE_URL and SUPABASE_KEY must be set.")
    day = engine.nhl_today()
    cur = int(engine.season_for(day))
    prev = cur - 10001
    stats = run(prev, cur)
    out = [f"# Ice Engine pattern backtest ({day})",
           "Regular season, every skater, last season + this season. Each game uses only games before it.",
           "Baseline = last-60-game rate shrunk toward the league rate for F or D. Diff = actual minus baseline, in percentage points.",
           "z: |2| or more is unlikely to be luck. Many buckets are tested, so a lone 2-3 can still be luck; trust an effect that shows in BOTH seasons.", ""]
    for col, label in MARKETS:
        out.append(f"## {label}")
        feats = []
        for k in stats:
            if k[0] == col and k[1] not in feats:
                feats.append(k[1])
        for f in feats:
            out.append(f"\n### {f}")
            out.append("| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |")
            out.append("|---|---|---|---|---|---|---|---|")
            buckets = []
            for k in stats:
                if k[0] == col and k[1] == f and k[2] not in buckets:
                    buckets.append(k[2])
            for b in buckets:
                a = fmt(stats[(col, f, b, "all")])
                ls = fmt(stats[(col, f, b, "last season")]) if (col, f, b, "last season") in stats else None
                ts = fmt(stats[(col, f, b, "this season")]) if (col, f, b, "this season") in stats else None
                cell = lambda x: f"{x[3]:+.1f} ({x[4]:+.1f}), n={x[0]}" if x else "-"
                out.append(f"| {b} | {a[0]} | {a[1]:.1f} | {a[2]:.1f} | {a[3]:+.1f} | {a[4]:+.1f} | {cell(ls)} | {cell(ts)} |")
        out.append("")
    os.makedirs("reports", exist_ok=True)
    with open("reports/pattern_backtest.md", "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"Wrote reports/pattern_backtest.md ({len(out)} lines).")


if __name__ == "__main__":
    main()
