# Projection scoreboard

Updated 2026-10-24 06:53 ET. Uses the last slate report committed before first puck each day.
Brier and log-loss: lower is better. 'Naive' guesses the same average for everyone; the model should beat it.

## Skater chances, 1+ goal / point / assist

| Market | N | Avg predicted | Actual rate | Brier | Naive Brier | Log-loss | Naive log-loss |
|---|---|---|---|---|---|---|---|
| Goal | 1628 | 16.4% | 15.5% | 0.1232 | 0.1313 | 0.4032 | 0.4320 |
| Point | 1628 | 37.0% | 36.1% | 0.2092 | 0.2307 | 0.6065 | 0.6541 |
| Assist | 1628 | 25.7% | 25.1% | 0.1769 | 0.1878 | 0.5353 | 0.5630 |

### Calibration, Goal

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 779 | 7.6% | 7.7% |
| 15-25% | 514 | 19.3% | 17.7% |
| 25-35% | 229 | 29.0% | 26.2% |
| 35-45% | 98 | 39.9% | 37.8% |
| 45-55% | 8 | 47.0% | 62.5% |

### Calibration, Point

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 79 | 11.2% | 12.7% |
| 15-25% | 344 | 19.9% | 20.3% |
| 25-35% | 387 | 29.5% | 30.0% |
| 35-45% | 313 | 39.2% | 36.7% |
| 45-55% | 217 | 49.1% | 48.4% |
| 55-65% | 190 | 59.2% | 56.3% |
| 65-75% | 86 | 68.5% | 64.0% |
| 75-100% | 12 | 78.3% | 83.3% |

### Calibration, Assist

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 281 | 10.7% | 13.2% |
| 15-25% | 599 | 19.2% | 19.7% |
| 25-35% | 384 | 29.3% | 26.0% |
| 35-45% | 223 | 38.9% | 37.7% |
| 45-55% | 99 | 49.0% | 46.5% |
| 55-65% | 40 | 58.2% | 52.5% |
| 65-75% | 2 | 65.0% | 100.0% |

### Point chance by role

| Role | N | Avg predicted | Actual |
|---|---|---|---|
| PP1 | 490 | 54.4% | 55.9% |
| PP2 | 468 | 36.9% | 35.9% |
| no PP | 670 | 24.2% | 21.8% |

## Does recent form add anything? (predicted vs actual by last-3 and last-10 hits)


### Point, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 254 | 26.1% | 25.2% |
| 1/3 | 293 | 36.4% | 35.2% |
| 2/3 | 219 | 47.1% | 45.7% |
| 3/3 | 57 | 53.8% | 40.4% |

### Goal, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 511 | 12.9% | 12.9% |
| 1/3 | 241 | 21.3% | 19.9% |
| 2/3 | 62 | 25.7% | 21.0% |

### Assist, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 369 | 20.1% | 20.9% |
| 1/3 | 312 | 27.7% | 28.8% |
| 2/3 | 123 | 35.4% | 25.2% |
| 3/3 | 19 | 45.1% | 36.8% |

### Point, by hits in the last 10 games

| Last 10 | N | Avg predicted | Actual |
|---|---|---|---|
| 0-2/10 | 540 | 23.6% | 23.1% |
| 3-4/10 | 566 | 35.7% | 34.3% |
| 5-6/10 | 366 | 48.4% | 50.5% |
| 7-8/10 | 135 | 60.1% | 54.1% |
| 9-10/10 | 21 | 66.8% | 52.4% |

### Point and goal, by the game's projected total

| Projected total | Market | N | Avg predicted | Actual |
|---|---|---|---|---|
| 0-5.9 | Point | 284 | 36.2% | 30.3% |
| 0-5.9 | Goal | 284 | 16.1% | 13.0% |
| 5.9-6.2 | Point | 817 | 36.4% | 36.8% |
| 5.9-6.2 | Goal | 817 | 16.2% | 15.1% |
| 6.2-6.4 | Point | 277 | 37.8% | 37.2% |
| 6.2-6.4 | Goal | 277 | 16.8% | 17.3% |
| 6.4-9 | Point | 250 | 38.8% | 39.2% |
| 6.4-9 | Goal | 250 | 17.1% | 18.0% |

## Game totals

Games: 60. Average projected total 6.10, actual 6.27 (actual minus projected: +0.17).
Mean absolute error 1.62 goals, against 1.70 for a flat guess at the average.

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
| 2026-10-23 | MTL@CHI | 6.19 | 5 |
| 2026-10-23 | TBL@COL | 6.43 | 9 |

## Data notes

- 2026-10-15: 359 skaters in the report, 9 not matched to a final box score
- 2026-10-16: 61 skaters in the report, 1 not matched to a final box score
- 2026-10-17: 226 skaters in the report, 4 not matched to a final box score
- 2026-10-18: 60 skaters in the report, 1 not matched to a final box score
- 2026-10-19: 119 skaters in the report, 5 not matched to a final box score
- 2026-10-20: 342 skaters in the report, 5 not matched to a final box score
- 2026-10-21: 60 skaters in the report, 1 not matched to a final box score
- 2026-10-22: 374 skaters in the report, 9 not matched to a final box score
- 2026-10-23: 63 skaters in the report, 1 not matched to a final box score
