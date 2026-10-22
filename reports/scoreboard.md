# Projection scoreboard

Updated 2026-10-22 16:58 ET. Uses the last slate report committed before first puck each day.
Brier and log-loss: lower is better. 'Naive' guesses the same average for everyone; the model should beat it.

## Skater chances, 1+ goal / point / assist

| Market | N | Avg predicted | Actual rate | Brier | Naive Brier | Log-loss | Naive log-loss |
|---|---|---|---|---|---|---|---|
| Goal | 1201 | 16.4% | 15.4% | 0.1224 | 0.1303 | 0.4028 | 0.4297 |
| Point | 1201 | 36.9% | 36.4% | 0.2077 | 0.2315 | 0.6030 | 0.6556 |
| Assist | 1201 | 25.6% | 24.9% | 0.1752 | 0.1870 | 0.5306 | 0.5612 |

### Calibration, Goal

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 575 | 7.7% | 7.3% |
| 15-25% | 382 | 19.3% | 18.3% |
| 25-35% | 167 | 29.0% | 24.0% |
| 35-45% | 71 | 39.8% | 40.8% |
| 45-55% | 6 | 47.0% | 66.7% |

### Calibration, Point

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 59 | 11.1% | 10.2% |
| 15-25% | 253 | 19.9% | 20.9% |
| 25-35% | 282 | 29.5% | 28.4% |
| 35-45% | 233 | 39.1% | 38.2% |
| 45-55% | 166 | 49.1% | 48.2% |
| 55-65% | 137 | 59.2% | 59.9% |
| 65-75% | 62 | 68.7% | 62.9% |
| 75-100% | 9 | 77.9% | 88.9% |

### Calibration, Assist

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 210 | 10.7% | 13.3% |
| 15-25% | 435 | 19.2% | 17.9% |
| 25-35% | 285 | 29.2% | 27.0% |
| 35-45% | 171 | 38.8% | 39.8% |
| 45-55% | 69 | 49.1% | 44.9% |
| 55-65% | 30 | 58.3% | 53.3% |
| 65-75% | 1 | 65.0% | 100.0% |

### Point chance by role

| Role | N | Avg predicted | Actual |
|---|---|---|---|
| PP1 | 361 | 54.1% | 57.6% |
| PP2 | 341 | 37.1% | 36.7% |
| no PP | 499 | 24.4% | 20.8% |

## Does recent form add anything? (predicted vs actual by last-3 and last-10 hits)


### Point, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 124 | 26.4% | 21.8% |
| 1/3 | 142 | 36.3% | 36.6% |
| 2/3 | 96 | 48.1% | 46.9% |
| 3/3 | 34 | 53.1% | 44.1% |

### Goal, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 250 | 13.1% | 13.6% |
| 1/3 | 109 | 21.4% | 18.3% |
| 2/3 | 33 | 26.6% | 21.2% |

### Assist, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 182 | 20.3% | 19.2% |
| 1/3 | 140 | 28.2% | 27.1% |
| 2/3 | 63 | 35.0% | 28.6% |
| 3/3 | 11 | 44.0% | 45.5% |

### Point, by hits in the last 10 games

| Last 10 | N | Avg predicted | Actual |
|---|---|---|---|
| 0-2/10 | 404 | 23.5% | 22.5% |
| 3-4/10 | 415 | 36.0% | 35.4% |
| 5-6/10 | 268 | 48.2% | 50.4% |
| 7-8/10 | 100 | 60.9% | 56.0% |
| 9-10/10 | 14 | 64.9% | 57.1% |

### Point and goal, by the game's projected total

| Projected total | Market | N | Avg predicted | Actual |
|---|---|---|---|---|
| 0-5.9 | Point | 193 | 36.5% | 27.5% |
| 0-5.9 | Goal | 193 | 16.1% | 11.4% |
| 5.9-6.2 | Point | 605 | 36.3% | 37.9% |
| 5.9-6.2 | Goal | 605 | 16.2% | 15.2% |
| 6.2-6.4 | Point | 242 | 37.8% | 36.0% |
| 6.2-6.4 | Goal | 242 | 16.9% | 16.9% |
| 6.4-9 | Point | 161 | 38.4% | 42.2% |
| 6.4-9 | Goal | 161 | 17.0% | 18.6% |

## Game totals

Games: 46. Average projected total 6.10, actual 6.15 (actual minus projected: +0.05).
Mean absolute error 1.56 goals, against 1.63 for a flat guess at the average.

| Date | Game | Projected | Actual |
|---|---|---|---|
| 2026-10-15 | BUF@TOR | 6.38 | 9 |
| 2026-10-15 | NYI@OTT | 5.88 | 3 |
| 2026-10-15 | SEA@TBL | 6.06 | 7 |
| 2026-10-15 | VAN@FLA | 6.16 | 5 |
| 2026-10-15 | NYR@NJD | 5.68 | 8 |
| 2026-10-15 | PHI@DET | 5.75 | 3 |
| 2026-10-15 | WPG@CHI | 5.79 | 7 |
| 2026-10-15 | SJS@NSH | 6.11 | 5 |
| 2026-10-15 | STL@MIN | 5.93 | 9 |
| 2026-10-15 | UTA@EDM | 6.53 | 6 |
| 2026-10-15 | CGY@VGK | 6.00 | 8 |
| 2026-10-16 | PIT@COL | 6.59 | 7 |
| 2026-10-16 | BOS@ANA | 6.22 | 6 |
| 2026-10-17 | NJD@WSH | 6.09 | 6 |
| 2026-10-17 | CAR@WPG | 6.08 | 5 |
| 2026-10-17 | VAN@TBL | 6.30 | 6 |
| 2026-10-17 | SEA@FLA | 5.93 | 11 |
| 2026-10-17 | NYI@TOR | 5.93 | 5 |
| 2026-10-17 | BUF@MTL | 6.55 | 7 |
| 2026-10-17 | SJS@DET | 5.94 | 7 |
| 2026-10-17 | OTT@PHI | 5.79 | 4 |
| 2026-10-17 | NYR@CBJ | 5.94 | 1 |
| 2026-10-17 | DAL@CHI | 5.69 | 4 |
| 2026-10-17 | STL@NSH | 5.94 | 7 |
| 2026-10-17 | BOS@LAK | 5.93 | 5 |
| 2026-10-17 | EDM@UTA | 6.50 | 8 |
| 2026-10-17 | PIT@VGK | 6.36 | 8 |
| 2026-10-18 | CBJ@MIN | 6.07 | 3 |
| 2026-10-18 | CAR@CGY | 6.14 | 5 |
| 2026-10-19 | ANA@NYR | 5.93 | 7 |
| 2026-10-19 | COL@PHI | 6.14 | 5 |
| 2026-10-19 | SJS@TOR | 6.32 | 4 |
| 2026-10-19 | PIT@UTA | 6.55 | 9 |
| 2026-10-20 | SJS@MTL | 6.40 | 7 |
| 2026-10-20 | COL@NJD | 6.32 | 7 |
| 2026-10-20 | ANA@NYI | 5.93 | 5 |
| 2026-10-20 | LAK@WSH | 6.04 | 7 |
| 2026-10-20 | TOR@CBJ | 6.14 | 8 |
| 2026-10-20 | WPG@STL | 5.98 | 3 |
| 2026-10-20 | BOS@DAL | 5.72 | 5 |
| 2026-10-20 | MIN@EDM | 6.37 | 7 |
| 2026-10-20 | DET@SEA | 5.98 | 7 |
| 2026-10-20 | CAR@VAN | 6.34 | 9 |
| 2026-10-20 | TBL@VGK | 6.23 | 8 |
| 2026-10-21 | PHI@BUF | 5.95 | 4 |
| 2026-10-21 | FLA@OTT | 6.00 | 6 |

## Data notes

- 2026-10-15: 359 skaters in the report, 9 not matched to a final box score
- 2026-10-16: 61 skaters in the report, 1 not matched to a final box score
- 2026-10-17: 226 skaters in the report, 4 not matched to a final box score
- 2026-10-18: 60 skaters in the report, 1 not matched to a final box score
- 2026-10-19: 119 skaters in the report, 5 not matched to a final box score
- 2026-10-20: 342 skaters in the report, 5 not matched to a final box score
- 2026-10-21: 60 skaters in the report, 1 not matched to a final box score
- 2026-10-22: 374 skaters in the report, 374 not matched to a final box score
