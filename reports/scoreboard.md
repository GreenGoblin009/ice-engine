# Projection scoreboard

Updated 2026-10-28 07:08 ET. Uses the last slate report committed before first puck each day.
Brier and log-loss: lower is better. 'Naive' guesses the same average for everyone; the model should beat it.

## Skater chances, 1+ goal / point / assist

| Market | N | Avg predicted | Actual rate | Brier | Naive Brier | Log-loss | Naive log-loss |
|---|---|---|---|---|---|---|---|
| Goal | 2411 | 16.4% | 15.7% | 0.1248 | 0.1322 | 0.4073 | 0.4343 |
| Point | 2411 | 36.8% | 36.4% | 0.2080 | 0.2314 | 0.6040 | 0.6555 |
| Assist | 2411 | 25.5% | 25.4% | 0.1773 | 0.1894 | 0.5363 | 0.5665 |

### Calibration, Goal

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 1153 | 7.6% | 8.2% |
| 15-25% | 766 | 19.2% | 17.0% |
| 25-35% | 336 | 28.9% | 28.3% |
| 35-45% | 143 | 39.7% | 35.0% |
| 45-55% | 13 | 46.9% | 61.5% |

### Calibration, Point

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 127 | 11.4% | 12.6% |
| 15-25% | 508 | 19.9% | 20.7% |
| 25-35% | 571 | 29.6% | 29.4% |
| 35-45% | 470 | 39.1% | 37.0% |
| 45-55% | 310 | 49.1% | 49.4% |
| 55-65% | 286 | 59.3% | 59.4% |
| 65-75% | 123 | 68.5% | 62.6% |
| 75-100% | 16 | 78.8% | 87.5% |

### Calibration, Assist

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 437 | 10.7% | 14.2% |
| 15-25% | 877 | 19.3% | 19.3% |
| 25-35% | 574 | 29.2% | 25.8% |
| 35-45% | 313 | 39.1% | 42.8% |
| 45-55% | 149 | 48.9% | 45.0% |
| 55-65% | 57 | 58.0% | 49.1% |
| 65-75% | 4 | 65.5% | 100.0% |

### Point chance by role

| Role | N | Avg predicted | Actual |
|---|---|---|---|
| PP1 | 731 | 54.1% | 57.7% |
| PP2 | 695 | 36.8% | 36.0% |
| no PP | 985 | 23.9% | 20.8% |

## Does recent form add anything? (predicted vs actual by last-3 and last-10 hits)


### Point, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 502 | 26.1% | 26.1% |
| 1/3 | 583 | 35.8% | 33.1% |
| 2/3 | 401 | 46.7% | 48.6% |
| 3/3 | 120 | 54.0% | 50.0% |

### Goal, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 993 | 12.7% | 12.8% |
| 1/3 | 478 | 21.0% | 20.1% |
| 2/3 | 119 | 26.5% | 22.7% |
| 3/3 | 16 | 34.1% | 37.5% |

### Assist, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 721 | 19.8% | 20.5% |
| 1/3 | 605 | 27.2% | 28.9% |
| 2/3 | 240 | 35.2% | 28.3% |
| 3/3 | 40 | 44.1% | 45.0% |

### Point, by hits in the last 10 games

| Last 10 | N | Avg predicted | Actual |
|---|---|---|---|
| 0-2/10 | 824 | 23.7% | 24.4% |
| 3-4/10 | 807 | 35.3% | 32.7% |
| 5-6/10 | 537 | 48.3% | 49.2% |
| 7-8/10 | 211 | 59.6% | 60.2% |
| 9-10/10 | 32 | 67.8% | 65.6% |

### Point and goal, by the game's projected total

| Projected total | Market | N | Avg predicted | Actual |
|---|---|---|---|---|
| 0-5.9 | Point | 614 | 36.1% | 37.3% |
| 0-5.9 | Goal | 614 | 16.0% | 16.1% |
| 5.9-6.2 | Point | 937 | 36.3% | 36.4% |
| 5.9-6.2 | Goal | 937 | 16.2% | 14.9% |
| 6.2-6.4 | Point | 582 | 37.4% | 33.8% |
| 6.2-6.4 | Goal | 582 | 16.6% | 15.3% |
| 6.4-9 | Point | 278 | 38.8% | 39.6% |
| 6.4-9 | Goal | 278 | 17.3% | 18.0% |

## Game totals

Games: 91. Average projected total 6.08, actual 6.24 (actual minus projected: +0.16).
Mean absolute error 1.81 goals, against 1.85 for a flat guess at the average.

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
| 2026-10-26 | LAK@NYR | 5.77 | 9 |
| 2026-10-26 | TOR@CGY | 6.03 | 7 |
| 2026-10-26 | DET@EDM | 6.28 | 7 |
| 2026-10-27 | CBJ@PHI | 5.59 | 7 |
| 2026-10-27 | BOS@CAR | 6.14 | 3 |
| 2026-10-27 | LAK@CHI | 5.67 | 3 |
| 2026-10-27 | MTL@STL | 6.20 | 2 |
| 2026-10-27 | NYI@NSH | 5.66 | 7 |
| 2026-10-27 | NJD@DAL | 5.57 | 6 |
| 2026-10-27 | FLA@WPG | 5.71 | 6 |
| 2026-10-27 | MIN@UTA | 6.27 | 4 |
| 2026-10-27 | OTT@VGK | 6.23 | 5 |
| 2026-10-27 | VAN@ANA | 6.39 | 11 |
| 2026-10-27 | BUF@SJS | 6.33 | 2 |

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
- 2026-10-26: 88 skaters in the report, 0 not matched to a final box score
- 2026-10-27: 343 skaters in the report, 4 not matched to a final box score
