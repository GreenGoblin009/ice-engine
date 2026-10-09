"""
Ice Engine — Player Prop Backtest, round 2
===========================================
Round 1 (backtest_player_props.py) found that a skater's season-long shrunk
hit rate ("long") carries almost all the signal, and that last-10 form,
consistency and "due" add nothing. This round starts from "long" and asks
whether context adds anything for Points o0.5, Assists o0.5, Goals o0.5 and
Shots o2.5:

  1. toi       average ice time, over the season so far and over the last 10
  2. power play  NOT TESTABLE: player_game_logs has no power-play minutes or
               power-play points column, so there is nothing to derive a
               power-play role from. (The NHL game-log feed does carry
               powerPlayGoals and powerPlayPoints; the daily pull would have
               to start saving them, and last season be re-pulled.)
  3. opponent  the opponent's goals against per game and shot attempts
               allowed per game, up to that date
  4. team_proj the player's team's projected goals for that game, from the
               fitted team model in backtest_team_totals.py
  5. home      home or away
  6. decay     a hit rate where recent games count more, at four speeds
               (each game back counts 0.98, 0.95, 0.90 or 0.80 as much)

Same rules as before: the 2025-26 regular season is replayed in date order,
every input is built from EARLIER dates only, weights are fit on the first
60% by date and scored on the last 40%. The team model that feeds factor 4
is itself fit only on games inside that first 60%.

HOW TO READ THE OUTPUT
  Each factor is added on its own to "long", and the change in log-loss on
  the held-out 40% is printed with a 90% interval (resampling game-days).
  "helps" needs the interval clear of zero AND a gain of at least 0.0005;
  smaller than that is real but too small to matter.

  The "final weights" model is chosen WITHOUT looking at the held-out 40%:
  a factor is kept if it improves log-loss by 0.0005+ on the last quarter of
  the training span. That model is then refit on all training games and
  scored once on the held-out part.

Inputs to the final formula, as used here:
  long         logit of the season hit rate, shrunk (see round 1)
  ln_toi_*     natural log of average minutes
  ln_opp_ga    ln(opponent blended goals against / league average)
  ln_opp_att   ln(opponent shot attempts allowed per game / league average)
  ln_team_proj ln(team projected goals)
  home         1 at home, 0 away
  decay_*      logit of the decay-weighted hit rate
  chance of going over = 1 / (1 + exp(-(intercept + sum(weight x input))))

Run:  python backtest_player_props_v2.py
"""

import math
from collections import defaultdict

import backtest_team_totals as team_model
from backtest_player_props import (MARKETS, MIN_GAMES, NEGLIGIBLE, SHRINK, chance_at_least, fit_logistic,
                                   gain_with_interval, logit, losses, verdict)
from backtest_team_totals import SEASON, TRAIN_SHARE, select_all, split_by_date, supabase_config

DECAYS = [0.98, 0.95, 0.90, 0.80]
DECAY_SHRINK = 5       # games of "what his average implies" mixed into the decay-weighted rate
TEAM_FACTORS = ["blend", "last10", "venue"]   # what the fitted team model kept

FACTORS = {
    "toi": ["ln_toi_season", "ln_toi_last10"],
    "opponent": ["ln_opp_ga", "ln_opp_att"],
    "team_proj": ["ln_team_proj"],
    "home": ["home"],
}
FACTORS.update({f"decay {d:.2f}": [f"decay_{d:.2f}"] for d in DECAYS})


def minutes(toi):
    try:
        m, s = toi.split(":")
        return int(m) + int(s) / 60
    except (AttributeError, ValueError):
        return None


def build_rows(logs, team_rows):
    """One row per skater-game with at least MIN_GAMES earlier games: the
    shared context inputs, plus hit / long / decay values for every market."""
    context = {(r["game_id"], r["team"]): r for r in team_rows}
    by_date = defaultdict(list)
    for r in logs:
        by_date[r["game_date"]].append(r)

    stats = defaultdict(lambda: {m: [] for m in MARKETS})   # player -> market -> stat per earlier game
    toi = defaultdict(list)                                  # player -> minutes per earlier game
    decayed = defaultdict(lambda: {(m, d): [0.0, 0.0] for m in MARKETS for d in DECAYS})  # weighted hits, weights
    league = {m: [0, 0] for m in MARKETS}
    rows = []
    for day in sorted(by_date):
        for r in by_date[day]:
            pid = r["player_id"]
            ctx = context.get((r["game_id"], r["team"]))
            ice = toi[pid]
            if len(ice) < MIN_GAMES or ctx is None:
                continue
            row = {"player_id": pid, "date": day, "game_id": r["game_id"], "team": r["team"],
                   "ln_toi_season": math.log(max(1.0, sum(ice) / len(ice))),
                   "ln_toi_last10": math.log(max(1.0, sum(ice[-10:]) / 10)),
                   "ln_opp_ga": ctx["ln_opp_ga_blend"],
                   "ln_opp_att": ctx["ln_opp_att_against"],
                   "home": ctx["home"]}
            for market, (column, need) in MARKETS.items():
                past = stats[pid][market]
                n = len(past)
                league_mean = league[market][0] / league[market][1] if league[market][1] else 0.0
                implied = chance_at_least((sum(past) + league_mean * SHRINK) / (n + SHRINK), need)
                hits = sum(1 for v in past if v >= need)
                row[(market, "hit")] = int(r[column] >= need)
                row[(market, "long")] = logit((hits + implied * SHRINK) / (n + SHRINK))
                for d in DECAYS:
                    w_hits, w = decayed[pid][(market, d)]
                    row[(market, f"decay_{d:.2f}")] = logit((w_hits + implied * DECAY_SHRINK) / (w + DECAY_SHRINK))
            rows.append(row)
        for r in by_date[day]:  # the day's own results only count from tomorrow
            pid = r["player_id"]
            played = minutes(r["toi"])
            if played is not None:
                toi[pid].append(played)
            for market, (column, need) in MARKETS.items():
                stats[pid][market].append(r[column])
                league[market][0] += r[column]
                league[market][1] += 1
                for d in DECAYS:
                    s = decayed[pid][(market, d)]
                    s[0] = s[0] * d + (r[column] >= need)
                    s[1] = s[1] * d + 1
    return rows


def for_market(rows, market):
    """The rows as one market sees them: shared inputs plus its own hit,
    long and decay columns under plain names."""
    out = []
    for r in rows:
        view = {k: v for k, v in r.items() if isinstance(k, str)}
        view.update({k[1]: v for k, v in r.items() if isinstance(k, tuple) and k[0] == market})
        out.append(view)
    return out


def base_losses(train, test):
    """Held-out log-loss of the baseline: the long-run hit rate on its own."""
    return losses(fit_logistic(train, ["long"]), ["long"], test)


def gain(train, test, base, columns):
    """Log-loss improvement on `test` from adding `columns` to the baseline,
    as (gain, low, high), plus the fitted weights."""
    beta = fit_logistic(train, ["long"] + columns)
    return gain_with_interval(test, base, losses(beta, ["long"] + columns, test)), beta


def main():
    url, key = supabase_config()
    logs = select_all(url, key, f"player_game_logs?season=eq.{SEASON}&game_type=eq.2&sog=not.is.null"
                                "&select=player_id,game_id,game_date,team,goals,assists,points,sog,toi"
                                "&order=game_date,game_id,player_id")
    print(f"Loaded {len(logs)} skater-games, season {SEASON}.")
    team_rows = team_model.build_rows(*team_model.load_data())

    rows = build_rows(logs, team_rows)
    _, _, cut = split_by_date(rows, TRAIN_SHARE)

    # Factor 4: the team model, fit only on games up to the split date.
    team_columns = team_model.columns_for(TEAM_FACTORS)
    team_beta = team_model.fit_poisson([r for r in team_rows if r["date"] <= cut], team_columns)
    projected = {(r["game_id"], r["team"]): team_model.predict(team_beta, team_columns, r) for r in team_rows}
    for r in rows:
        r["ln_team_proj"] = math.log(projected[(r["game_id"], r["team"])])

    print("\nPower-play role: NOT TESTABLE. player_game_logs has no power-play minutes or power-play points "
          "column (columns available: goals, assists, points, sog, shot_attempts, toi).")

    for market in MARKETS:
        view = for_market(rows, market)
        train, test, cut = split_by_date(view, TRAIN_SHARE)
        fit_part, check_part, _ = split_by_date(train, 0.75)
        print(f"\n=== {market} ===  fit on {len(train)} skater-games through {cut}, tested on {len(test)}")

        base_test, base_check = base_losses(train, test), base_losses(fit_part, check_part)
        inner = {}
        for factor, columns in FACTORS.items():
            (g, lo, hi), beta = gain(train, test, base_test, columns)
            inner[factor] = gain(fit_part, check_part, base_check, columns)[0][0]
            weights = ", ".join(f"{c} {b:+.3f}" for c, b in zip(columns, beta[2:]))
            print(f"  {factor:<10} gain {g:+.4f} ({lo:+.4f} to {hi:+.4f})  -> {verdict(g, lo, hi):<19} [{weights}]")

        # Choose the final model inside the training span only.
        best_decay = max((f for f in FACTORS if f.startswith("decay")), key=lambda f: inner[f])
        kept = [f for f in FACTORS if inner[f] >= NEGLIGIBLE and (not f.startswith("decay") or f == best_decay)]
        columns = ["long"] + [c for f in kept for c in FACTORS[f]]
        (g, lo, hi), beta = gain(train, test, base_test, columns[1:])
        print(f"  Final model (chosen inside the training span): long + {', '.join(kept) or 'nothing'}")
        print(f"    held-out gain over long alone: {g:+.4f} ({lo:+.4f} to {hi:+.4f})")
        print("    weights: intercept " + f"{beta[0]:+.4f}, " + ", ".join(f"{c} {b:+.4f}" for c, b in zip(columns, beta[1:])))


if __name__ == "__main__":
    main()
