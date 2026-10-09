"""
Ice Engine — Player Prop Backtest
==================================
Asks: for a skater's next game, which of these actually help predict whether
he goes over Points 0.5, Goals 0.5, Assists 0.5 and Shots 2.5?

  1. long     his hit rate over the season so far, shrunk toward the rate his
              own per-game average implies (so 3 hits in 4 games isn't "75%")
  2. recent   his hit rate over the last 10 games
  3. steady   consistency: how much the stat swings game to game
              (standard deviation / average; lower = steadier)
  4. due      games since he last hit, and how far his last 5 are running
              below his season rate
  5. after 2 misses   per player: is he more (or less) likely to hit right
              after two straight misses than in his other games?

Same rules as backtest_team_totals.py: the 2025-26 regular season is replayed
in date order, every input for a game is built from that player's EARLIER
games only, the weights are fit on the first 60% of the season by date and
everything is scored on the last 40%.

HOW EACH QUESTION IS ANSWERED
  Factors 1-4: a logistic regression per market. "long" alone is the
  baseline; each other factor is added to it on its own, and the change in
  log-loss on the held-out 40% says whether it adds anything. The +/- is a
  90% interval from resampling whole game-days; if it straddles zero the
  factor has not shown real predictive power.

  Factor 5: for each player, hit rate right after two straight misses minus
  hit rate in all his other games, measured in the training part. Then the
  same gap is measured again in the held-out part. If the pattern is real,
  players with a big gap in training keep it; if it is noise, the held-out
  gap falls back to about zero and the two barely correlate.

HONEST LIMITS
  - One season. player_game_logs only has players on an NHL roster now.
  - A player needs 10 earlier games before his games are scored (20 for the
    after-2-misses check to count on each side of the split).
  - No opponent, line or ice-time inputs: this tests the player-history
    factors against each other, not against a sportsbook's line.

Run:  python backtest_player_props.py
"""

import math
import random
import statistics
from collections import defaultdict

from backtest_team_totals import SEASON, TRAIN_SHARE, select_all, solve, split_by_date, supabase_config

MARKETS = {  # market -> (column, goals/points/shots needed to go over)
    "Points o0.5": ("points", 1),
    "Goals o0.5": ("goals", 1),
    "Assists o0.5": ("assists", 1),
    "Shots o2.5": ("sog", 3),
}
MIN_GAMES = 10        # earlier games a player needs before a game is scored
SHRINK = 10           # games of "what his average implies" mixed into the long-run rate
MAX_STREAK = 10       # games-since-last-hit is capped here
MIN_PATTERN_GAMES = 8  # after-2-misses games a player needs on each side of the split
BIG_GAP = 0.10        # a "big" after-2-misses gap: 10 points of hit rate
NEGLIGIBLE = 0.0005   # log-loss gains smaller than this don't matter in practice
WORKED_EXAMPLE = ("Pavel Zacha", "Points o0.5")

FACTORS = {
    "recent": ["recent10"],
    "steady": ["variation"],
    "due": ["miss_streak", "cold_gap"],
}


def chance_at_least(mean, need):
    """P(X >= need) for a Poisson count with this average."""
    below = sum(math.exp(-mean) * mean ** k / math.factorial(k) for k in range(need))
    return 1 - below


def logit(p):
    p = min(max(p, 1e-4), 1 - 1e-4)
    return math.log(p / (1 - p))


def build_rows(logs, column, need):
    """One row per skater-game with at least MIN_GAMES earlier games, plus
    every game's after-2-misses flag for the per-player pattern check."""
    by_date = defaultdict(list)
    for r in logs:
        by_date[r["game_date"]].append(r)

    history = defaultdict(list)   # player -> stat in each earlier game
    league_sum = league_n = 0
    rows, pattern = [], []
    for day in sorted(by_date):
        league_mean = league_sum / league_n if league_n else 0.0
        for r in by_date[day]:
            past = history[r["player_id"]]
            hit = int(r[column] >= need)
            hits = [int(v >= need) for v in past]
            streak = 0
            for h in reversed(hits):
                if h:
                    break
                streak += 1
            if len(past) >= 2:
                pattern.append({"player_id": r["player_id"], "date": day, "hit": hit,
                                "after_two_misses": streak >= 2, "games_before": len(past)})
            if len(past) < MIN_GAMES:
                continue
            n = len(past)
            mean = (sum(past) + league_mean * SHRINK) / (n + SHRINK)
            long_rate = (sum(hits) + chance_at_least(mean, need) * SHRINK) / (n + SHRINK)
            season_rate = sum(hits) / n
            rows.append({
                "player_id": r["player_id"], "date": day, "game_id": r["game_id"], "hit": hit,
                "long_rate": long_rate,
                "long": logit(long_rate),
                "recent10": sum(hits[-10:]) / 10,
                "variation": statistics.pstdev(past) / (sum(past) / n + 0.1),
                "miss_streak": min(streak, MAX_STREAK),
                "cold_gap": max(0.0, season_rate - sum(hits[-5:]) / 5),
            })
        for r in by_date[day]:  # the day's own results only count from tomorrow
            history[r["player_id"]].append(r[column])
            league_sum += r[column]
            league_n += 1
    return rows, pattern


def fit_logistic(rows, columns, ridge=1e-3, iterations=30):
    """Maximum-likelihood logistic regression by Newton's method.
    Returns [intercept, weight per column]."""
    x = [[1.0] + [r[c] for c in columns] for r in rows]
    y = [r["hit"] for r in rows]
    p = len(columns) + 1
    beta = [logit(sum(y) / len(y))] + [0.0] * (p - 1)
    for _ in range(iterations):
        grad = [0.0] * p
        hess = [[0.0] * p for _ in range(p)]
        for xi, yi in zip(x, y):
            mu = 1 / (1 + math.exp(-sum(b * v for b, v in zip(beta, xi))))
            w = mu * (1 - mu)
            for j in range(p):
                grad[j] += (yi - mu) * xi[j]
                for k in range(j, p):
                    hess[j][k] += w * xi[j] * xi[k]
        for j in range(p):
            for k in range(j):
                hess[j][k] = hess[k][j]
            if j:
                grad[j] -= ridge * beta[j]
                hess[j][j] += ridge
        step = solve(hess, grad)
        beta = [b + s for b, s in zip(beta, step)]
        if max(abs(s) for s in step) < 1e-9:
            break
    return beta


def losses(beta, columns, rows):
    """Log-loss of each row (lower = better; 0.693 is a coin flip)."""
    out = []
    for r in rows:
        p = 1 / (1 + math.exp(-(beta[0] + sum(b * r[c] for b, c in zip(beta[1:], columns)))))
        p = min(max(p, 1e-6), 1 - 1e-6)
        out.append(-math.log(p if r["hit"] else 1 - p))
    return out


def gain_with_interval(rows, loss_without, loss_with, draws=1000, seed=7):
    """Mean improvement in log-loss and a 90% interval, resampling whole
    game-days (games on one night aren't independent of each other)."""
    by_day = defaultdict(lambda: [0.0, 0])
    for r, a, b in zip(rows, loss_without, loss_with):
        by_day[r["date"]][0] += a - b
        by_day[r["date"]][1] += 1
    days = list(by_day.values())
    gain = sum(d[0] for d in days) / sum(d[1] for d in days)
    rng, means = random.Random(seed), []
    for _ in range(draws):
        sample = [rng.choice(days) for _ in days]
        means.append(sum(d[0] for d in sample) / sum(d[1] for d in sample))
    means.sort()
    return gain, means[int(0.05 * draws)], means[int(0.95 * draws)]


def verdict(gain, low, high):
    """A gain can be statistically non-zero and still too small to matter:
    under 0.0005 of log-loss is called negligible either way."""
    if low <= 0 <= high:
        return "no real effect"
    if abs(gain) < NEGLIGIBLE:
        return "real but negligible"
    return "helps" if gain > 0 else "hurts"


def pattern_gaps(pattern, cut):
    """Per player: (hit rate after two straight misses) - (hit rate in other
    games), separately before and after the split date."""
    tally = defaultdict(lambda: [[0, 0, 0, 0], [0, 0, 0, 0]])  # player -> [train, test]: after hits/n, other hits/n
    for g in pattern:
        t = tally[g["player_id"]][g["date"] > cut]
        offset = 0 if g["after_two_misses"] else 2
        t[offset] += g["hit"]
        t[offset + 1] += 1
    return tally


def gap(t):
    return t[0] / t[1] - t[2] / t[3]


def correlation(xs, ys):
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy) if sx and sy else 0.0


def main():
    url, key = supabase_config()
    logs = select_all(url, key, f"player_game_logs?season=eq.{SEASON}&game_type=eq.2&sog=not.is.null"
                                "&select=player_id,game_id,game_date,goals,assists,points,sog"
                                "&order=game_date,game_id,player_id")
    names = {p["id"]: p["name"] for p in select_all(url, key, "players?select=id,name&order=id")}
    print(f"Loaded {len(logs)} skater-games for {len({r['player_id'] for r in logs})} skaters, season {SEASON}.")

    for market, (column, need) in MARKETS.items():
        rows, pattern = build_rows(logs, column, need)
        train, test, cut = split_by_date(rows, TRAIN_SHARE)
        print(f"\n=== {market} ===  fit on {len(train)} skater-games through {cut}, tested on {len(test)}; "
              f"hit rate {sum(r['hit'] for r in test) / len(test):.1%}")

        flat = fit_logistic(train, [])
        base = fit_logistic(train, ["long"])
        base_loss = losses(base, ["long"], test)
        g, lo, hi = gain_with_interval(test, losses(flat, [], test), base_loss)
        print(f"  {'long':<7} vs everyone-gets-the-league-rate: log-loss {sum(base_loss) / len(test):.4f}, "
              f"gain {g:+.4f} ({lo:+.4f} to {hi:+.4f})  -> {verdict(g, lo, hi)}")
        for factor, columns in FACTORS.items():
            beta = fit_logistic(train, ["long"] + columns)
            g, lo, hi = gain_with_interval(test, base_loss, losses(beta, ["long"] + columns, test))
            weights = ", ".join(f"{c} {b:+.3f}" for c, b in zip(columns, beta[2:]))
            print(f"  {factor:<7} added to long: gain {g:+.4f} ({lo:+.4f} to {hi:+.4f})  -> {verdict(g, lo, hi)}"
                  f"   [weights: {weights}]")

        # 5. The after-2-misses pattern, player by player.
        tally = pattern_gaps(pattern, cut)
        enough = {p: t for p, t in tally.items()
                  if all(side[1] >= MIN_PATTERN_GAMES and side[3] >= MIN_PATTERN_GAMES for side in t)}
        train_gap = {p: gap(t[0]) for p, t in enough.items()}
        test_gap = {p: gap(t[1]) for p, t in enough.items()}
        players = sorted(enough)
        r = correlation([train_gap[p] for p in players], [test_gap[p] for p in players])
        pooled = [sum(t[side][i] for t in tally.values()) for side in (0, 1) for i in range(4)]
        print(f"  after 2 misses, all players pooled: train {pooled[0] / pooled[1]:.1%} vs {pooled[2] / pooled[3]:.1%} "
              f"in other games; test {pooled[4] / pooled[5]:.1%} vs {pooled[6] / pooled[7]:.1%} "
              f"(lower mostly because weaker players miss twice more often)")
        print(f"  per player ({len(players)} with {MIN_PATTERN_GAMES}+ such games on both sides): "
              f"train gap vs test gap correlation {r:+.2f}")
        for label, group in ((f"bounce back (train gap >= +{BIG_GAP:.0%})", [p for p in players if train_gap[p] >= BIG_GAP]),
                             (f"stay cold   (train gap <= -{BIG_GAP:.0%})", [p for p in players if train_gap[p] <= -BIG_GAP])):
            if group:
                print(f"    {label}: {len(group)} players, avg train gap {sum(train_gap[p] for p in group) / len(group):+.1%}"
                      f" -> avg test gap {sum(test_gap[p] for p in group) / len(group):+.1%}")

        if market == WORKED_EXAMPLE[1]:
            pid = next((i for i, n in names.items() if n == WORKED_EXAMPLE[0]), None)
            if pid in tally:
                a, b = tally[pid]
                def side(t):
                    after = f"{t[0]}/{t[1]} ({t[0] / t[1]:.0%})" if t[1] else "0/0"
                    other = f"{t[2]}/{t[3]} ({t[2] / t[3]:.0%})" if t[3] else "0/0"
                    return f"after 2 misses {after}, other games {other}"
                print(f"  Worked example, {WORKED_EXAMPLE[0]}: train: {side(a)} | test: {side(b)}")
            else:
                print(f"  Worked example: {WORKED_EXAMPLE[0]} has no 2025-26 games in player_game_logs.")


if __name__ == "__main__":
    main()
