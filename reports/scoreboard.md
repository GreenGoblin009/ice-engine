# Projection scoreboard

Updated 2026-10-26 07:05 ET. Uses the last slate report committed before first puck each day.
Brier and log-loss: lower is better. 'Naive' guesses the same average for everyone; the model should beat it.

## Skater chances, 1+ goal / point / assist

| Market | N | Avg predicted | Actual rate | Brier | Naive Brier | Log-loss | Naive log-loss |
|---|---|---|---|---|---|---|---|
| Goal | 1984 | 16.4% | 15.8% | 0.1240 | 0.1329 | 0.4044 | 0.4359 |
| Point | 1984 | 36.9% | 36.8% | 0.2090 | 0.2326 | 0.6062 | 0.6579 |
| Assist | 1984 | 25.6% | 25.6% | 0.1785 | 0.1905 | 0.5391 | 0.5689 |

### Calibration, Goal

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 945 | 7.6% | 7.7% |
| 15-25% | 632 | 19.2% | 17.6% |
| 25-35% | 277 | 28.9% | 27.8% |
| 35-45% | 119 | 39.8% | 37.8% |
| 45-55% | 11 | 46.9% | 63.6% |

### Calibration, Point

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 99 | 11.2% | 14.1% |
| 15-25% | 417 | 20.0% | 20.1% |
| 25-35% | 476 | 29.6% | 30.5% |
| 35-45% | 381 | 39.1% | 36.7% |
| 45-55% | 259 | 49.2% | 49.8% |
| 55-65% | 234 | 59.2% | 59.0% |
| 65-75% | 104 | 68.6% | 65.4% |
| 75-100% | 14 | 78.6% | 85.7% |

### Calibration, Assist

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 348 | 10.7% | 13.8% |
| 15-25% | 727 | 19.3% | 19.8% |
| 25-35% | 471 | 29.2% | 25.7% |
| 35-45% | 263 | 39.0% | 41.8% |
| 45-55% | 124 | 48.9% | 46.8% |
| 55-65% | 48 | 58.1% | 50.0% |
| 65-75% | 3 | 65.3% | 100.0% |

### Point chance by role

| Role | N | Avg predicted | Actual |
|---|---|---|---|
| PP1 | 601 | 54.2% | 57.6% |
| PP2 | 575 | 36.8% | 36.7% |
| no PP | 808 | 24.1% | 21.4% |

## Does recent form add anything? (predicted vs actual by last-3 and last-10 hits)


### Point, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 371 | 26.2% | 26.1% |
| 1/3 | 426 | 36.3% | 35.4% |
| 2/3 | 304 | 46.9% | 48.0% |
| 3/3 | 78 | 54.8% | 48.7% |

### Goal, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 731 | 12.8% | 13.0% |
| 1/3 | 349 | 21.2% | 20.3% |
| 2/3 | 87 | 26.5% | 21.8% |
| 3/3 | 12 | 34.4% | 50.0% |

### Assist, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 539 | 20.0% | 20.6% |
| 1/3 | 439 | 27.7% | 30.8% |
| 2/3 | 176 | 35.5% | 28.4% |
| 3/3 | 25 | 45.9% | 36.0% |

### Point, by hits in the last 10 games

| Last 10 | N | Avg predicted | Actual |
|---|---|---|---|
| 0-2/10 | 673 | 23.8% | 24.5% |
| 3-4/10 | 672 | 35.5% | 34.1% |
| 5-6/10 | 443 | 48.3% | 50.1% |
| 7-8/10 | 171 | 60.1% | 57.9% |
| 9-10/10 | 25 | 67.8% | 60.0% |

### Point and goal, by the game's projected total

| Projected total | Market | N | Avg predicted | Actual |
|---|---|---|---|---|
| 0-5.9 | Point | 434 | 36.3% | 36.4% |
| 0-5.9 | Goal | 434 | 16.2% | 15.7% |
| 5.9-6.2 | Point | 880 | 36.3% | 36.2% |
| 5.9-6.2 | Goal | 880 | 16.2% | 14.9% |
| 6.2-6.4 | Point | 392 | 37.7% | 36.5% |
| 6.2-6.4 | Goal | 392 | 16.7% | 16.3% |
| 6.4-9 | Point | 278 | 38.8% | 39.6% |
| 6.4-9 | Goal | 278 | 17.3% | 18.0% |

## Game totals

Games: 77. Average projected total 6.10, actual 6.35 (actual minus projected: +0.25).
Mean absolute error 1.74 goals, against 1.81 for a flat guess at the average.

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
| 2026-10-24 | ANA@PHI | 5.75 | 9 |
| 2026-10-24 | LAK@NJD | 5.84 | 4 |
| 2026-10-24 | SJS@BOS | 6.13 | 10 |
| 2026-10-24 | NYR@OTT | 5.84 | 11 |
| 2026-10-24 | NSH@PIT | 6.34 | 5 |
| 2026-10-24 | BUF@WSH | 6.37 | 7 |
| 2026-10-24 | VGK@CBJ | 6.20 | 3 |
| 2026-10-24 | CAR@STL | 6.20 | 4 |
| 2026-10-24 | TOR@EDM | 6.67 | 9 |
| 2026-10-24 | TBL@UTA | 6.50 | 9 |
| 2026-10-24 | DET@CGY | 5.73 | 5 |
| 2026-10-24 | MIN@SEA | 6.12 | 6 |
| 2026-10-25 | FLA@CHI | 5.85 | 5 |
| 2026-10-25 | NYI@DAL | 5.36 | 9 |
| 2026-10-25 | MTL@WPG | 6.05 | 3 |
| 2026-10-25 | COL@NSH | 6.26 | 8 |
| 2026-10-25 | MIN@VAN | 6.15 | 6 |

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
- 2026-10-24: 206 skaters in the report, 6 not matched to a final box score
- 2026-10-25: 158 skaters in the report, 2 not matched to a final box score
