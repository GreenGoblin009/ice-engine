"""
Ice Engine — Team Goal Projection Backtest
===========================================
Asks one question: would a fitted model have projected team goals better
than the formula the Props Board uses today?

It replays the 2025-26 regular season in date order. For every game it
builds each team's inputs from games played on EARLIER dates only (nothing
from the same day or later), fits the weights on the first 60% of the season,
and scores both the fitted model and the current formula on the last 40%.

WHAT IT READS (read-only; nothing is written to Supabase):
  - games, player_game_logs for 2025-26 from Supabase.
  - team_game_shot_attempts, the view in supabase/team_game_shot_attempts.sql.
    If the view hasn't been created yet, the same totals are computed here
    from player_game_logs (slower: ~44 requests instead of 3).
  - 2024-25 final scores from the NHL API, only for "last season counts as
    15 games" and prior head-to-head meetings — Supabase has no 2024-25.

THE INPUTS, per team per game:
  1. blend    blended goals for, and the opponent's blended goals against
              (last season's rate counts as 15 games)
  2. last10   goals for over the last 10 games; opponent's goals against
  3. goalie   save % of the goalie who started for the opponent, from his
              earlier games, shrunk toward .905
  4. attempts team shot attempts for per game; opponent's attempts against
  5. h2h      goals per game against this opponent, shrunk hard to average
  6. venue    home or away
  7. rest     back-to-back, or 2+ days off

THE MODEL is a Poisson regression: expected goals = exp(b0 + sum(b * input)),
with rates entered as logs. So a weight of 0.5 on blended goals-for means "a
team that scores 10% more than average is projected about 5% higher", and a
weight of 0.04 on home means "+4% at home".

HONEST LIMITS:
  - One season, ~1,050 team-games in the test set. Goals are noisy; small
    differences between models are inside the noise (see the +/- printed).
  - player_game_logs only has players who are on an NHL roster now, so about
    one skater in seven is missing from 2025-26 games. Shot attempts are
    scaled up by 18 / skaters found; goalies who have left the league have
    no save % and get .905.
  - Which factors "helped" is decided on the last quarter of the training
    span, never on the test set.

Run:  python backtest_team_totals.py
Supabase URL and key come from SUPABASE_URL / SUPABASE_KEY, or failing that
from the public (read-only) ones in index.html.
"""

import json
import math
import os
import random
import re
import urllib.request
import urllib.error
from collections import defaultdict
from datetime import date

import ice_engine_daily_pull as engine

SEASON, PREV_SEASON = 20252026, 20242025
PRIOR_GAMES = 15      # last season's rate counts as this many games
LEAGUE_SV = 0.905
GOALIE_SHRINK = 400   # shots of league-average goaltending mixed in (same as the board)
H2H_SHRINK = 10       # games of league-average scoring mixed into head-to-head
ATTEMPT_SHRINK = 10   # games of league-average attempts mixed in
TRAIN_SHARE = 0.60

FACTORS = {  # factor -> the model inputs it contributes
    "blend": ["ln_gf_blend", "ln_opp_ga_blend"],
    "last10": ["ln_gf_last10", "ln_opp_ga_last10"],
    "goalie": ["opp_goalie_sv_pts"],
    "attempts": ["ln_att_for", "ln_opp_att_against"],
    "h2h": ["ln_h2h"],
    "venue": ["home"],
    "rest": ["back_to_back", "rested"],
}


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------
def supabase_config():
    url = os.environ.get("SUPABASE_URL", "").strip().rstrip("/")
    key = os.environ.get("SUPABASE_KEY", "").strip()
    if not (url and key):
        html = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html"), encoding="utf-8").read()
        url = re.search(r"SB_URL = '([^']+)'", html).group(1)
        key = re.search(r"SB_KEY = '([^']+)'", html).group(1)
    return url, key


def select_all(url, key, query, page_size=1000):
    """Every row of a read-only query, paged. Returns None if the table or
    view doesn't exist."""
    rows, offset = [], 0
    while True:
        req = urllib.request.Request(f"{url}/rest/v1/{query}&limit={page_size}&offset={offset}",
                                     headers={"apikey": key, "User-Agent": "IceEngine/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                page = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            raise SystemExit(f"Supabase read failed: HTTP {e.code} {e.read().decode('utf-8', 'replace')[:300]}")
        rows += page
        if len(page) < page_size:
            return rows
        offset += page_size


def regulation_goals(away_score, home_score, last_period_type):
    """Final score without the extra goal the NHL credits a shootout winner."""
    if last_period_type == "SO":
        if away_score > home_score:
            away_score -= 1
        else:
            home_score -= 1
    return away_score, home_score


def load_data():
    url, key = supabase_config()
    games = select_all(url, key, f"games?season=eq.{SEASON}&game_type=eq.2&home_score=not.is.null"
                                 "&select=id,game_date,away,home,away_score,home_score,last_period_type"
                                 "&order=game_date,id")
    goalies = select_all(url, key, f"player_game_logs?season=eq.{SEASON}&game_type=eq.2&shots_against=not.is.null"
                                   "&select=player_id,game_id,team,games_started,shots_against,goals_against"
                                   "&order=game_id,player_id")
    attempts = select_all(url, key, f"team_game_shot_attempts?season=eq.{SEASON}&game_type=eq.2"
                                    "&select=game_id,team,attempts_for,skaters_logged&order=game_id,team")
    source = "the team_game_shot_attempts view"
    if attempts is None:
        source = "player_game_logs (view not created yet)"
        logs = select_all(url, key, f"player_game_logs?season=eq.{SEASON}&game_type=eq.2&shot_attempts=not.is.null"
                                    "&select=game_id,team,sog,shot_attempts&order=game_id,player_id")
        totals = defaultdict(lambda: {"attempts_for": 0, "skaters_logged": 0})
        for r in logs:
            t = totals[(r["game_id"], r["team"])]
            t["attempts_for"] += r["shot_attempts"]
            t["skaters_logged"] += r["sog"] is not None  # goalies have no sog
        attempts = [dict(game_id=g, team=t, **v) for (g, t), v in totals.items()]

    print(f"Loaded {len(games)} games, {len(goalies)} goalie rows, {len(attempts)} team-game attempt totals from {source}.")
    print(f"Fetching {PREV_SEASON} final scores from the NHL API for the prior ...")
    previous = [g for g in engine.get_season_games(str(PREV_SEASON), sleep_between=0.1)
                if g["gameType"] == 2 and g["homeScore"] is not None]
    return games, goalies, attempts, previous


# ---------------------------------------------------------------------------
# Features — everything here sees only games from earlier dates
# ---------------------------------------------------------------------------
def build_rows(games, goalies, attempts, previous):
    """Two rows per game (one per team): the pre-game inputs and the goals
    that team then scored."""
    prev = defaultdict(lambda: [0, 0, 0])          # team -> [games, gf, ga] last season
    h2h = defaultdict(lambda: [0, 0])              # (team, opp) -> [goals, games]
    for g in previous:
        a, h = regulation_goals(g["awayScore"], g["homeScore"], g["lastPeriodType"])
        for team, opp, gf, ga in ((g["away"], g["home"], a, h), (g["home"], g["away"], h, a)):
            prev[team][0] += 1; prev[team][1] += gf; prev[team][2] += ga
            h2h[(team, opp)][0] += gf; h2h[(team, opp)][1] += 1
    prev_avg = sum(p[1] for p in prev.values()) / max(1, sum(p[0] for p in prev.values()))

    starter = {}                                   # (game_id, team) -> goalie id
    goalie_lines = defaultdict(list)               # game_id -> [(goalie id, shots, goals against)]
    for r in goalies:
        goalie_lines[r["game_id"]].append((r["player_id"], r["shots_against"], r["goals_against"] or 0))
        if r["games_started"] == 1:
            starter[(r["game_id"], r["team"])] = r["player_id"]
    att = {}                                       # (game_id, team) -> attempts, scaled to a full 18 skaters
    for r in attempts:
        if r["skaters_logged"] and r["skaters_logged"] >= 10:
            att[(r["game_id"], r["team"])] = r["attempts_for"] * 18.0 / r["skaters_logged"]

    team = defaultdict(lambda: {"gf": [], "ga": [], "att_for": [], "att_against": [], "last": None})
    goalie_career = defaultdict(lambda: [0, 0])    # goalie id -> [shots, goals against] so far
    league = {"goals": 0.0, "team_games": 0, "att": 0.0, "att_games": 0}

    def blended(t, key, prev_index):
        p = prev[t]
        prior_rate = p[prev_index] / p[0] if p[0] else prev_avg
        return (prior_rate * PRIOR_GAMES + sum(team[t][key])) / (PRIOR_GAMES + len(team[t][key]))

    def last10(t, key, fallback):
        recent = team[t][key][-10:]  # short early in the season: top up with the blended rate
        return (sum(recent) + fallback * (10 - len(recent))) / 10

    def attempts_rate(t, key, league_att):
        values = team[t][key]
        return (sum(values) + league_att * ATTEMPT_SHRINK) / (len(values) + ATTEMPT_SHRINK)

    rows, by_date = [], defaultdict(list)
    for g in games:
        by_date[g["game_date"]].append(g)

    for day in sorted(by_date):
        league_goals = league["goals"] / league["team_games"] if league["team_games"] else prev_avg
        league_att = league["att"] / league["att_games"] if league["att_games"] >= 20 else 60.0
        results = []
        for g in by_date[day]:
            away_goals, home_goals = regulation_goals(g["away_score"], g["home_score"], g["last_period_type"])
            for t, opp, is_home, goals, allowed in ((g["away"], g["home"], 0, away_goals, home_goals),
                                                   (g["home"], g["away"], 1, home_goals, away_goals)):
                gf_blend, opp_ga_blend = blended(t, "gf", 1), blended(opp, "ga", 2)
                opp_goalie = starter.get((g["id"], opp))
                shots, against = goalie_career[opp_goalie] if opp_goalie else (0, 0)
                sv = ((shots - against) + LEAGUE_SV * GOALIE_SHRINK) / (shots + GOALIE_SHRINK)
                meet = h2h[(t, opp)]
                h2h_rate = (meet[0] + league_goals * H2H_SHRINK) / (meet[1] + H2H_SHRINK)
                days = (date.fromisoformat(day) - date.fromisoformat(team[t]["last"])).days if team[t]["last"] else None
                opener = days is None or days > 30
                rows.append({
                    "game_id": g["id"], "date": day, "team": t, "opp": opp, "goals": goals,
                    # raw values, for the current formula
                    "gf_blend": gf_blend, "opp_ga_blend": opp_ga_blend, "sv": sv,
                    "has_goalie": opp_goalie is not None, "days": None if opener else days,
                    # model inputs
                    "ln_gf_blend": math.log(gf_blend / league_goals),
                    "ln_opp_ga_blend": math.log(opp_ga_blend / league_goals),
                    "ln_gf_last10": math.log(max(0.5, last10(t, "gf", gf_blend)) / league_goals),
                    "ln_opp_ga_last10": math.log(max(0.5, last10(opp, "ga", opp_ga_blend)) / league_goals),
                    "opp_goalie_sv_pts": (sv - LEAGUE_SV) * 100,
                    "ln_att_for": math.log(attempts_rate(t, "att_for", league_att) / league_att),
                    "ln_opp_att_against": math.log(attempts_rate(opp, "att_against", league_att) / league_att),
                    "ln_h2h": math.log(h2h_rate / league_goals),
                    "home": is_home,
                    "back_to_back": int(not opener and days <= 1),
                    "rested": int(not opener and days >= 3),
                })
                results.append((g["id"], t, opp, goals, allowed))

        # Only now does the day's own result enter the running totals.
        for game_id, t, opp, goals, allowed in results:
            s = team[t]
            s["gf"].append(goals); s["ga"].append(allowed); s["last"] = day
            if (game_id, t) in att:
                s["att_for"].append(att[(game_id, t)])
                league["att"] += att[(game_id, t)]; league["att_games"] += 1
            if (game_id, opp) in att:
                s["att_against"].append(att[(game_id, opp)])
            h2h[(t, opp)][0] += goals; h2h[(t, opp)][1] += 1
            league["goals"] += goals; league["team_games"] += 1
        for g in by_date[day]:
            for goalie, shots, against in goalie_lines[g["id"]]:
                goalie_career[goalie][0] += shots; goalie_career[goalie][1] += against
    return rows


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
def current_formula(r):
    """The Props Board's projectTeam(), as of October 2026."""
    base = 0.6 * r["gf_blend"] + 0.4 * r["opp_ga_blend"]
    goalie = (r["sv"] - LEAGUE_SV) * -4 if r["has_goalie"] else 0.0
    venue = 0.05 if r["home"] else -0.05
    rest = 0.0 if r["days"] is None else (-0.10 if r["days"] <= 1 else 0.03 if r["days"] >= 3 else 0.0)
    return base * (1 + goalie) * (1 + venue) * (1 + rest)


def solve(a, b):
    """Solve a x = b by Gaussian elimination with partial pivoting."""
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(m[r][col]))
        m[col], m[pivot] = m[pivot], m[col]
        for r in range(col + 1, n):
            f = m[r][col] / m[col][col]
            for c in range(col, n + 1):
                m[r][c] -= f * m[col][c]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (m[r][n] - sum(m[r][c] * x[c] for c in range(r + 1, n))) / m[r][r]
    return x


def fit_poisson(rows, columns, ridge=1e-3, iterations=40):
    """Maximum-likelihood Poisson regression (Newton's method), with a touch
    of ridge so near-duplicate inputs can't blow the weights up. Returns
    [intercept, weight per column]."""
    x = [[1.0] + [r[c] for c in columns] for r in rows]
    y = [r["goals"] for r in rows]
    p = len(columns) + 1
    beta = [math.log(sum(y) / len(y))] + [0.0] * (p - 1)
    for _ in range(iterations):
        grad = [0.0] * p
        hess = [[0.0] * p for _ in range(p)]
        for xi, yi in zip(x, y):
            mu = math.exp(sum(b * v for b, v in zip(beta, xi)))
            for j in range(p):
                grad[j] += (yi - mu) * xi[j]
                for k in range(j, p):
                    hess[j][k] += mu * xi[j] * xi[k]
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


def predict(beta, columns, r):
    return math.exp(beta[0] + sum(b * r[c] for b, c in zip(beta[1:], columns)))


def poisson_loss(pred, goals):
    """Negative log-likelihood of the actual score under Poisson(pred)."""
    return pred - goals * math.log(pred) + math.lgamma(goals + 1)


def score(rows, preds):
    n = len(rows)
    return {"mae": sum(abs(p - r["goals"]) for p, r in zip(preds, rows)) / n,
            "logloss": sum(poisson_loss(p, r["goals"]) for p, r in zip(preds, rows)) / n,
            "bias": sum(p - r["goals"] for p, r in zip(preds, rows)) / n}


def columns_for(factors):
    return [c for f in FACTORS if f in factors for c in FACTORS[f]]


def split_by_date(rows, share):
    dates = sorted({r["date"] for r in rows})
    counts, running = [], 0
    for d in dates:
        running += sum(1 for r in rows if r["date"] == d)
        counts.append(running)
    cut = next(d for d, c in zip(dates, counts) if c >= share * len(rows))
    return [r for r in rows if r["date"] <= cut], [r for r in rows if r["date"] > cut], cut


def bootstrap_gain(rows, loss_a, loss_b, draws=2000, seed=7):
    """90% interval for mean(loss_a - loss_b), resampling whole games."""
    by_game = defaultdict(list)
    for i, r in enumerate(rows):
        by_game[r["game_id"]].append(loss_a[i] - loss_b[i])
    games = list(by_game.values())
    rng, means = random.Random(seed), []
    for _ in range(draws):
        sample = [d for _ in games for d in rng.choice(games)]
        means.append(sum(sample) / len(sample))
    means.sort()
    return means[int(0.05 * draws)], means[int(0.95 * draws)]


def main():
    games, goalies, attempts, previous = load_data()
    if engine.FAILED_URLS:
        raise SystemExit(f"{len(engine.FAILED_URLS)} NHL API request(s) failed; the prior would be incomplete.")
    rows = build_rows(games, goalies, attempts, previous)
    train, test, cut = split_by_date(rows, TRAIN_SHARE)
    fit_part, check_part, _ = split_by_date(train, 0.75)

    # Which factors earn their place? Judged inside the training span only:
    # drop one factor, refit on the first 75% of train, score on the rest.
    everything = list(FACTORS)
    full = fit_poisson(fit_part, columns_for(everything))
    full_loss = score(check_part, [predict(full, columns_for(everything), r) for r in check_part])["logloss"]
    effect = {}
    for f in everything:
        without = [x for x in everything if x != f]
        beta = fit_poisson(fit_part, columns_for(without))
        loss = score(check_part, [predict(beta, columns_for(without), r) for r in check_part])["logloss"]
        effect[f] = loss - full_loss  # positive = the model got worse without it
    kept = [f for f in everything if effect[f] > 0] or ["blend"]
    dropped = [f for f in everything if f not in kept]

    columns = columns_for(kept)
    beta = fit_poisson(train, columns)
    model_preds = [predict(beta, columns, r) for r in test]
    all_beta = fit_poisson(train, columns_for(everything))
    all_preds = [predict(all_beta, columns_for(everything), r) for r in test]
    formula_preds = [current_formula(r) for r in test]
    flat = sum(r["goals"] for r in train) / len(train)

    m, a, c = score(test, model_preds), score(test, all_preds), score(test, formula_preds)
    k = score(test, [flat] * len(test))
    low, high = bootstrap_gain(test, [poisson_loss(p, r["goals"]) for p, r in zip(formula_preds, test)],
                               [poisson_loss(p, r["goals"]) for p, r in zip(model_preds, test)])
    coverage = sum(1 for r in rows if r["has_goalie"]) / len(rows)

    print(f"\nSeason {SEASON}: {len(rows)} team-games; fit on {len(train)} (through {cut}), tested on {len(test)}.")
    print(f"Opponent starter known for {coverage:.0%} of team-games; the rest use {LEAGUE_SV}.")
    print("\nFactor check inside the training span (log-loss change when the factor is removed; + = it helped):")
    for f in sorted(everything, key=lambda f: -effect[f]):
        print(f"  {f:<9} {effect[f]:+.4f}  {'keep' if f in kept else 'drop'}")
    print("\nFinal weights (fit on all training games, kept factors only):")
    print(f"  intercept {beta[0]:+.3f}  (= {math.exp(beta[0]):.2f} goals when every input below is zero)")
    for name, b in zip(columns, beta[1:]):
        print(f"  {name:<19} {b:+.3f}")
    print(f"\nTest set ({len(test)} team-games)        avg error   Poisson log-loss   bias")
    for label, s in (("current formula", c), ("fitted, kept factors", m), ("fitted, all factors", a), ("flat league average", k)):
        print(f"  {label:<22} {s['mae']:>10.3f} {s['logloss']:>18.4f} {s['bias']:>+7.2f}")
    print(f"\nFitted (kept factors) vs current formula: avg error {c['mae'] - m['mae']:+.3f} goals "
          f"({(c['mae'] - m['mae']) / c['mae']:+.1%}), log-loss {c['logloss'] - m['logloss']:+.4f} "
          f"(90% interval {low:+.4f} to {high:+.4f}; positive = fitted is better).")
    print(f"Kept: {', '.join(kept)}. Dropped: {', '.join(dropped) or 'none'}.")


if __name__ == "__main__":
    main()
