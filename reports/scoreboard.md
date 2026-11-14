# Projection scoreboard

Updated 2026-11-14 11:40 ET. Uses the last slate report committed before first puck each day.
Brier and log-loss: lower is better. 'Naive' guesses the same average for everyone; the model should beat it.

## Skater chances, 1+ goal / point / assist

| Market | N | Avg predicted | Actual rate | Brier | Naive Brier | Log-loss | Naive log-loss |
|---|---|---|---|---|---|---|---|
| Goal | 5067 | 16.2% | 15.8% | 0.1255 | 0.1334 | 0.4088 | 0.4371 |
| Point | 5067 | 36.6% | 36.8% | 0.2071 | 0.2325 | 0.6023 | 0.6577 |
| Assist | 5067 | 25.4% | 25.9% | 0.1768 | 0.1918 | 0.5347 | 0.5717 |

### Calibration, Goal

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 2419 | 7.6% | 8.3% |
| 15-25% | 1627 | 19.2% | 17.9% |
| 25-35% | 714 | 28.7% | 26.6% |
| 35-45% | 281 | 39.8% | 38.4% |
| 45-55% | 26 | 47.0% | 50.0% |

### Calibration, Point

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 279 | 11.4% | 15.1% |
| 15-25% | 1077 | 19.9% | 20.1% |
| 25-35% | 1178 | 29.6% | 28.2% |
| 35-45% | 1007 | 39.3% | 39.0% |
| 45-55% | 667 | 49.1% | 49.9% |
| 55-65% | 582 | 59.4% | 61.9% |
| 65-75% | 240 | 68.5% | 65.0% |
| 75-100% | 37 | 78.9% | 83.8% |

### Calibration, Assist

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 927 | 10.7% | 14.1% |
| 15-25% | 1830 | 19.3% | 18.6% |
| 25-35% | 1232 | 29.1% | 26.9% |
| 35-45% | 637 | 39.0% | 44.9% |
| 45-55% | 313 | 48.6% | 47.3% |
| 55-65% | 118 | 58.0% | 55.1% |
| 65-75% | 10 | 66.6% | 90.0% |

### Point chance by role

| Role | N | Avg predicted | Actual |
|---|---|---|---|
| PP1 | 1535 | 53.9% | 58.2% |
| PP2 | 1453 | 36.8% | 35.7% |
| no PP | 2079 | 23.8% | 21.7% |

## Does recent form add anything? (predicted vs actual by last-3 and last-10 hits)


### Point, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 1284 | 26.1% | 25.5% |
| 1/3 | 1552 | 35.1% | 33.8% |
| 2/3 | 1052 | 45.2% | 46.9% |
| 3/3 | 374 | 55.0% | 58.6% |

### Goal, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 2585 | 12.7% | 12.6% |
| 1/3 | 1285 | 20.1% | 19.8% |
| 2/3 | 356 | 26.0% | 24.4% |
| 3/3 | 36 | 34.1% | 33.3% |

### Assist, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 1886 | 19.7% | 19.1% |
| 1/3 | 1569 | 26.5% | 29.0% |
| 2/3 | 677 | 35.0% | 34.3% |
| 3/3 | 130 | 44.9% | 46.9% |

### Point, by hits in the last 10 games

| Last 10 | N | Avg predicted | Actual |
|---|---|---|---|
| 0-2/10 | 1752 | 23.8% | 24.0% |
| 3-4/10 | 1585 | 34.4% | 32.1% |
| 5-6/10 | 1130 | 47.6% | 49.6% |
| 7-8/10 | 523 | 57.9% | 61.4% |
| 9-10/10 | 77 | 67.8% | 67.5% |

### Point and goal, by the game's projected total

| Projected total | Market | N | Avg predicted | Actual |
|---|---|---|---|---|
| 0-5.9 | Point | 1509 | 35.6% | 36.4% |
| 0-5.9 | Goal | 1509 | 15.7% | 15.7% |
| 5.9-6.2 | Point | 1968 | 36.7% | 37.2% |
| 5.9-6.2 | Goal | 1968 | 16.3% | 15.6% |
| 6.2-6.4 | Point | 1072 | 37.3% | 33.9% |
| 6.2-6.4 | Goal | 1072 | 16.5% | 15.0% |
| 6.4-9 | Point | 518 | 38.1% | 42.3% |
| 6.4-9 | Goal | 518 | 17.0% | 18.9% |

## Game totals

Games: 204. Average projected total 6.07, actual 6.38 (actual minus projected: +0.31).
Mean absolute error 1.80 goals, against 1.81 for a flat guess at the average.

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
| 2026-10-28 | PHI@WSH | 5.83 | 7 |
| 2026-10-28 | CGY@EDM | 6.31 | 4 |
| 2026-10-28 | NJD@COL | 6.32 | 7 |
| 2026-10-28 | TOR@SEA | 6.39 | 9 |
| 2026-10-29 | WPG@TBL | 6.00 | 10 |
| 2026-10-29 | UTA@PIT | 6.71 | 7 |
| 2026-10-29 | CBJ@CAR | 6.07 | 5 |
| 2026-10-29 | CHI@DET | 5.58 | 5 |
| 2026-10-29 | BOS@STL | 5.90 | 5 |
| 2026-10-29 | WSH@NSH | 6.13 | 7 |
| 2026-10-29 | MTL@DAL | 5.81 | 7 |
| 2026-10-29 | NYI@MIN | 5.76 | 7 |
| 2026-10-29 | BUF@ANA | 6.42 | 13 |
| 2026-10-29 | OTT@LAK | 5.88 | 11 |
| 2026-10-29 | VAN@SJS | 6.35 | 5 |
| 2026-10-30 | NJD@VGK | 5.96 | 7 |
| 2026-10-30 | WPG@FLA | 5.82 | 7 |
| 2026-10-30 | SEA@CGY | 5.93 | 8 |
| 2026-10-31 | CHI@BOS | 5.66 | 9 |
| 2026-10-31 | STL@DET | 5.65 | 9 |
| 2026-10-31 | TBL@NSH | 6.15 | 9 |
| 2026-10-31 | EDM@NYI | 6.15 | 4 |
| 2026-10-31 | BUF@LAK | 6.06 | 5 |
| 2026-10-31 | OTT@SJS | 6.16 | 6 |
| 2026-10-31 | PIT@MTL | 6.38 | 9 |
| 2026-10-31 | TOR@VAN | 6.43 | 6 |
| 2026-10-31 | CBJ@DAL | 5.76 | 4 |
| 2026-10-31 | CGY@COL | 6.15 | 7 |
| 2026-11-01 | WPG@CAR | 6.00 | 7 |
| 2026-11-01 | MIN@WSH | 6.04 | 6 |
| 2026-11-01 | UTA@PHI | 5.95 | 9 |
| 2026-11-01 | EDM@NYR | 6.32 | 5 |
| 2026-11-01 | OTT@ANA | 6.41 | 9 |
| 2026-11-02 | VGK@BOS | 6.12 | 5 |
| 2026-11-02 | DET@FLA | 5.76 | 8 |
| 2026-11-02 | COL@CHI | 6.18 | 7 |
| 2026-11-02 | CGY@SJS | 5.67 | 3 |
| 2026-11-03 | UTA@TOR | 6.53 | 5 |
| 2026-11-03 | WPG@MTL | 5.96 | 9 |
| 2026-11-03 | DET@TBL | 6.13 | 6 |
| 2026-11-03 | STL@NYR | 5.88 | 4 |
| 2026-11-03 | MIN@PHI | 5.60 | 6 |
| 2026-11-03 | VGK@PIT | 6.46 | 5 |
| 2026-11-03 | DAL@WSH | 5.92 | 11 |
| 2026-11-03 | COL@CBJ | 6.25 | 9 |
| 2026-11-03 | EDM@NJD | 6.15 | 7 |
| 2026-11-03 | CAR@NSH | 6.02 | 5 |
| 2026-11-03 | ANA@VAN | 6.51 | 9 |
| 2026-11-04 | OTT@BUF | 6.32 | 3 |
| 2026-11-04 | CHI@FLA | 5.72 | 8 |
| 2026-11-04 | SJS@LAK | 5.72 | 9 |
| 2026-11-04 | CGY@SEA | 5.76 | 3 |
| 2026-11-05 | UTA@MTL | 6.38 | 9 |
| 2026-11-05 | VGK@DET | 5.90 | 3 |
| 2026-11-05 | CHI@TBL | 6.06 | 5 |
| 2026-11-05 | STL@NJD | 5.68 | 9 |
| 2026-11-05 | CAR@NYI | 5.88 | 8 |
| 2026-11-05 | PHI@NYR | 5.60 | 5 |
| 2026-11-05 | BOS@PIT | 6.30 | 8 |
| 2026-11-05 | DAL@CBJ | 5.80 | 3 |
| 2026-11-05 | VAN@WPG | 6.09 | 8 |
| 2026-11-05 | ANA@EDM | 6.76 | 9 |
| 2026-11-05 | NSH@COL | 6.39 | 5 |
| 2026-11-06 | CBJ@BUF | 5.90 | 7 |
| 2026-11-06 | SJS@MIN | 5.87 | 5 |
| 2026-11-06 | ANA@CGY | 5.97 | 8 |
| 2026-11-07 | FLA@WSH | 6.17 | 7 |
| 2026-11-07 | STL@NSH | 5.85 | 4 |
| 2026-11-07 | NYR@SEA | 6.12 | 7 |
| 2026-11-07 | MTL@TOR | 6.31 | 6 |
| 2026-11-07 | UTA@OTT | 6.40 | 6 |
| 2026-11-07 | NJD@NYI | 5.68 | 9 |
| 2026-11-07 | CHI@CAR | 5.98 | 11 |
| 2026-11-07 | SJS@DAL | 5.79 | 7 |
| 2026-11-07 | TBL@MIN | 6.03 | 7 |
| 2026-11-07 | DET@COL | 6.21 | 4 |
| 2026-11-07 | PIT@LAK | 6.16 | 7 |
| 2026-11-07 | VAN@EDM | 6.55 | 6 |
| 2026-11-08 | FLA@BOS | 6.02 | 5 |
| 2026-11-08 | VGK@BUF | 6.10 | 5 |
| 2026-11-08 | TBL@WPG | 6.16 | 7 |
| 2026-11-08 | NJD@TOR | 6.11 | 4 |
| 2026-11-08 | PHI@CGY | 5.23 | 7 |
| 2026-11-08 | PIT@ANA | 6.69 | 7 |
| 2026-11-09 | NYR@EDM | 6.39 | 4 |
| 2026-11-09 | PHI@VAN | 5.77 | 4 |
| 2026-11-09 | NYI@SJS | 5.84 | 5 |
| 2026-11-10 | COL@TOR | 6.50 | 9 |
| 2026-11-10 | MIN@MTL | 5.95 | 3 |
| 2026-11-10 | WSH@OTT | 6.30 | 5 |
| 2026-11-10 | NJD@WPG | 5.87 | 6 |
| 2026-11-10 | FLA@CBJ | 5.83 | 5 |
| 2026-11-10 | DET@STL | 5.75 | 5 |
| 2026-11-10 | NSH@LAK | 5.71 | 3 |
| 2026-11-11 | TBL@BUF | 6.32 | 11 |
| 2026-11-11 | NYR@CGY | 5.60 | 4 |
| 2026-11-11 | PHI@EDM | 6.03 | 5 |
| 2026-11-11 | UTA@VGK | 6.44 | 8 |
| 2026-11-11 | NSH@ANA | 6.22 | 6 |
| 2026-11-11 | PIT@SJS | 6.28 | 5 |
| 2026-11-12 | CAR@SEA | 6.36 | 5 |
| 2026-11-12 | MTL@BOS | 6.08 | 7 |
| 2026-11-12 | MIN@TOR | 6.01 | 7 |
| 2026-11-12 | COL@OTT | 6.44 | 7 |
| 2026-11-12 | WSH@NJD | 6.09 | 7 |
| 2026-11-12 | TBL@CBJ | 6.14 | 4 |
| 2026-11-12 | DET@FLA | 5.86 | 9 |
| 2026-11-12 | BUF@CHI | 6.09 | 5 |
| 2026-11-12 | WPG@DAL | 5.82 | 11 |
| 2026-11-12 | STL@UTA | 6.21 | 1 |
| 2026-11-12 | NYI@LAK | 5.66 | 7 |
| 2026-11-13 | NYR@VAN | 6.04 | 6 |
| 2026-11-13 | NSH@VGK | 5.90 | 5 |

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
- 2026-10-28: 124 skaters in the report, 0 not matched to a final box score
- 2026-10-29: 313 skaters in the report, 3 not matched to a final box score
- 2026-10-30: 98 skaters in the report, 2 not matched to a final box score
- 2026-10-31: 186 skaters in the report, 11 not matched to a final box score
- 2026-11-01: 158 skaters in the report, 5 not matched to a final box score
- 2026-11-02: 128 skaters in the report, 0 not matched to a final box score
- 2026-11-03: 297 skaters in the report, 4 not matched to a final box score
- 2026-11-04: 129 skaters in the report, 1 not matched to a final box score
- 2026-11-05: 333 skaters in the report, 4 not matched to a final box score
- 2026-11-06: 99 skaters in the report, 4 not matched to a final box score
- 2026-11-07: 102 skaters in the report, 1 not matched to a final box score
- 2026-11-08: 98 skaters in the report, 4 not matched to a final box score
- 2026-11-09: 99 skaters in the report, 2 not matched to a final box score
- 2026-11-10: 235 skaters in the report, 1 not matched to a final box score
- 2026-11-11: 204 skaters in the report, 3 not matched to a final box score
- 2026-11-12: 32 skaters in the report, 0 not matched to a final box score
- 2026-11-13: 67 skaters in the report, 1 not matched to a final box score
- 2026-11-14: report has no skater section; skipped
