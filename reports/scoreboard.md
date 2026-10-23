# Projection scoreboard

Updated 2026-10-23 06:56 ET. Uses the last slate report committed before first puck each day.
Brier and log-loss: lower is better. 'Naive' guesses the same average for everyone; the model should beat it.

## Skater chances, 1+ goal / point / assist

| Market | N | Avg predicted | Actual rate | Brier | Naive Brier | Log-loss | Naive log-loss |
|---|---|---|---|---|---|---|---|
| Goal | 1566 | 16.4% | 15.5% | 0.1232 | 0.1311 | 0.4027 | 0.4316 |
| Point | 1566 | 36.9% | 36.3% | 0.2095 | 0.2313 | 0.6071 | 0.6553 |
| Assist | 1566 | 25.6% | 25.2% | 0.1769 | 0.1883 | 0.5353 | 0.5641 |

### Calibration, Goal

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 751 | 7.6% | 7.6% |
| 15-25% | 494 | 19.3% | 18.0% |
| 25-35% | 222 | 29.0% | 26.6% |
| 35-45% | 92 | 39.8% | 37.0% |
| 45-55% | 7 | 47.1% | 57.1% |

### Calibration, Point

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 78 | 11.2% | 12.8% |
| 15-25% | 335 | 19.9% | 20.6% |
| 25-35% | 366 | 29.5% | 30.1% |
| 35-45% | 302 | 39.2% | 37.4% |
| 45-55% | 211 | 49.2% | 48.8% |
| 55-65% | 183 | 59.2% | 56.3% |
| 65-75% | 80 | 68.6% | 63.7% |
| 75-100% | 11 | 78.4% | 90.9% |

### Calibration, Assist

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 274 | 10.7% | 13.5% |
| 15-25% | 577 | 19.3% | 19.6% |
| 25-35% | 368 | 29.3% | 26.1% |
| 35-45% | 213 | 38.8% | 38.5% |
| 45-55% | 94 | 49.0% | 45.7% |
| 55-65% | 38 | 58.2% | 55.3% |
| 65-75% | 2 | 65.0% | 100.0% |

### Point chance by role

| Role | N | Avg predicted | Actual |
|---|---|---|---|
| PP1 | 472 | 54.2% | 56.4% |
| PP2 | 448 | 36.9% | 36.2% |
| no PP | 646 | 24.1% | 21.8% |

## Does recent form add anything? (predicted vs actual by last-3 and last-10 hits)


### Point, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 233 | 26.0% | 25.3% |
| 1/3 | 275 | 36.4% | 36.0% |
| 2/3 | 198 | 46.5% | 46.5% |
| 3/3 | 55 | 53.6% | 38.2% |

### Goal, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 473 | 12.9% | 12.9% |
| 1/3 | 224 | 21.1% | 19.6% |
| 2/3 | 55 | 25.1% | 21.8% |

### Assist, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 340 | 20.1% | 21.2% |
| 1/3 | 290 | 27.6% | 28.6% |
| 2/3 | 112 | 34.8% | 25.9% |
| 3/3 | 19 | 45.1% | 36.8% |

### Point, by hits in the last 10 games

| Last 10 | N | Avg predicted | Actual |
|---|---|---|---|
| 0-2/10 | 521 | 23.4% | 22.8% |
| 3-4/10 | 540 | 35.7% | 35.4% |
| 5-6/10 | 354 | 48.2% | 50.3% |
| 7-8/10 | 130 | 59.9% | 53.8% |
| 9-10/10 | 21 | 66.8% | 52.4% |

### Point and goal, by the game's projected total

| Projected total | Market | N | Avg predicted | Actual |
|---|---|---|---|---|
| 0-5.9 | Point | 284 | 36.2% | 30.3% |
| 0-5.9 | Goal | 284 | 16.1% | 13.0% |
| 5.9-6.2 | Point | 785 | 36.4% | 37.5% |
| 5.9-6.2 | Goal | 785 | 16.2% | 15.3% |
| 6.2-6.4 | Point | 277 | 37.8% | 37.2% |
| 6.2-6.4 | Goal | 277 | 16.8% | 17.3% |
| 6.4-9 | Point | 220 | 38.2% | 39.1% |
| 6.4-9 | Goal | 220 | 16.8% | 17.3% |

## Game totals

Games: 58. Average projected total 6.09, actual 6.24 (actual minus projected: +0.15).
Mean absolute error 1.61 goals, against 1.69 for a flat guess at the average.

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
| 2026-10-22 | NSH@BOS | 5.97 | 6 |
| 2026-10-22 | NYR@TOR | 5.87 | 9 |
| 2026-10-22 | SJS@OTT | 6.05 | 8 |
| 2026-10-22 | ANA@NJD | 6.17 | 5 |
| 2026-10-22 | FLA@PIT | 6.43 | 4 |
| 2026-10-22 | LAK@NYI | 5.64 | 5 |
| 2026-10-22 | VGK@STL | 6.19 | 8 |
| 2026-10-22 | WPG@DAL | 5.58 | 5 |
| 2026-10-22 | MIN@CGY | 5.94 | 3 |
| 2026-10-22 | CAR@EDM | 6.58 | 11 |
| 2026-10-22 | UTA@SEA | 6.33 | 8 |
| 2026-10-22 | DET@VAN | 6.06 | 7 |

## Data notes

- 2026-10-15: 359 skaters in the report, 9 not matched to a final box score
- 2026-10-16: 61 skaters in the report, 1 not matched to a final box score
- 2026-10-17: 226 skaters in the report, 4 not matched to a final box score
- 2026-10-18: 60 skaters in the report, 1 not matched to a final box score
- 2026-10-19: 119 skaters in the report, 5 not matched to a final box score
- 2026-10-20: 342 skaters in the report, 5 not matched to a final box score
- 2026-10-21: 60 skaters in the report, 1 not matched to a final box score
- 2026-10-22: 374 skaters in the report, 9 not matched to a final box score
