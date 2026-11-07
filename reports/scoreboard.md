# Projection scoreboard

Updated 2026-11-07 00:32 ET. Uses the last slate report committed before first puck each day.
Brier and log-loss: lower is better. 'Naive' guesses the same average for everyone; the model should beat it.

## Skater chances, 1+ goal / point / assist

| Market | N | Avg predicted | Actual rate | Brier | Naive Brier | Log-loss | Naive log-loss |
|---|---|---|---|---|---|---|---|
| Goal | 4242 | 16.3% | 16.4% | 0.1289 | 0.1370 | 0.4172 | 0.4460 |
| Point | 4242 | 36.7% | 37.6% | 0.2096 | 0.2345 | 0.6082 | 0.6618 |
| Assist | 4242 | 25.4% | 26.4% | 0.1793 | 0.1942 | 0.5409 | 0.5770 |

### Calibration, Goal

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 2034 | 7.6% | 8.7% |
| 15-25% | 1351 | 19.2% | 18.7% |
| 25-35% | 595 | 28.7% | 27.2% |
| 35-45% | 240 | 39.8% | 38.8% |
| 45-55% | 22 | 47.1% | 50.0% |

### Calibration, Point

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 233 | 11.4% | 15.9% |
| 15-25% | 900 | 20.0% | 20.7% |
| 25-35% | 988 | 29.6% | 29.9% |
| 35-45% | 839 | 39.3% | 40.0% |
| 45-55% | 561 | 49.1% | 48.3% |
| 55-65% | 485 | 59.4% | 63.7% |
| 65-75% | 206 | 68.5% | 65.0% |
| 75-100% | 30 | 78.8% | 83.3% |

### Calibration, Assist

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 777 | 10.7% | 14.8% |
| 15-25% | 1525 | 19.3% | 19.4% |
| 25-35% | 1036 | 29.1% | 26.5% |
| 35-45% | 535 | 39.0% | 45.6% |
| 45-55% | 261 | 48.7% | 48.3% |
| 55-65% | 100 | 58.0% | 55.0% |
| 65-75% | 8 | 66.3% | 100.0% |

### Point chance by role

| Role | N | Avg predicted | Actual |
|---|---|---|---|
| PP1 | 1289 | 53.9% | 59.5% |
| PP2 | 1219 | 36.7% | 35.5% |
| no PP | 1734 | 23.8% | 22.7% |

## Does recent form add anything? (predicted vs actual by last-3 and last-10 hits)


### Point, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 1035 | 26.2% | 26.6% |
| 1/3 | 1257 | 35.0% | 34.0% |
| 2/3 | 838 | 45.5% | 49.0% |
| 3/3 | 307 | 54.9% | 59.0% |

### Goal, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 2088 | 12.7% | 12.9% |
| 1/3 | 1028 | 20.2% | 21.1% |
| 2/3 | 293 | 26.4% | 26.6% |
| 3/3 | 28 | 34.0% | 32.1% |

### Assist, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 1507 | 19.7% | 20.0% |
| 1/3 | 1289 | 26.5% | 29.4% |
| 2/3 | 535 | 35.0% | 34.6% |
| 3/3 | 106 | 44.7% | 48.1% |

### Point, by hits in the last 10 games

| Last 10 | N | Avg predicted | Actual |
|---|---|---|---|
| 0-2/10 | 1465 | 23.9% | 24.5% |
| 3-4/10 | 1343 | 34.6% | 33.4% |
| 5-6/10 | 943 | 47.6% | 50.5% |
| 7-8/10 | 430 | 58.2% | 62.1% |
| 9-10/10 | 61 | 67.9% | 68.9% |

### Point and goal, by the game's projected total

| Projected total | Market | N | Avg predicted | Actual |
|---|---|---|---|---|
| 0-5.9 | Point | 1245 | 35.8% | 38.2% |
| 0-5.9 | Goal | 1245 | 15.9% | 16.8% |
| 5.9-6.2 | Point | 1671 | 36.6% | 37.8% |
| 5.9-6.2 | Goal | 1671 | 16.3% | 16.0% |
| 6.2-6.4 | Point | 873 | 37.3% | 34.4% |
| 6.2-6.4 | Goal | 873 | 16.5% | 15.5% |
| 6.4-9 | Point | 453 | 38.1% | 41.1% |
| 6.4-9 | Goal | 453 | 17.0% | 18.3% |

## Game totals

Games: 157. Average projected total 6.07, actual 6.48 (actual minus projected: +0.41).
Mean absolute error 1.85 goals, against 1.86 for a flat guess at the average.

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
