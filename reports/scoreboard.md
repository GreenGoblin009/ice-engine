# Projection scoreboard

Updated 2026-11-19 14:05 ET. Uses the last slate report committed before first puck each day.
Brier and log-loss: lower is better. 'Naive' guesses the same average for everyone; the model should beat it.

## Skater chances, 1+ goal / point / assist

| Market | N | Avg predicted | Actual rate | Brier | Naive Brier | Log-loss | Naive log-loss |
|---|---|---|---|---|---|---|---|
| Goal | 5814 | 16.2% | 16.0% | 0.1257 | 0.1341 | 0.4088 | 0.4390 |
| Point | 5814 | 36.6% | 36.8% | 0.2071 | 0.2325 | 0.6024 | 0.6576 |
| Assist | 5814 | 25.4% | 25.9% | 0.1768 | 0.1917 | 0.5346 | 0.5715 |

### Calibration, Goal

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 2781 | 7.5% | 8.2% |
| 15-25% | 1867 | 19.1% | 18.3% |
| 25-35% | 816 | 28.6% | 26.5% |
| 35-45% | 321 | 39.8% | 39.9% |
| 45-55% | 29 | 47.0% | 51.7% |

### Calibration, Point

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 327 | 11.4% | 15.0% |
| 15-25% | 1229 | 19.9% | 20.3% |
| 25-35% | 1362 | 29.5% | 27.6% |
| 35-45% | 1161 | 39.3% | 40.1% |
| 45-55% | 750 | 49.0% | 49.5% |
| 55-65% | 666 | 59.4% | 61.6% |
| 65-75% | 277 | 68.5% | 65.0% |
| 75-100% | 42 | 79.1% | 85.7% |

### Calibration, Assist

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 1068 | 10.7% | 13.6% |
| 15-25% | 2116 | 19.3% | 19.0% |
| 25-35% | 1396 | 29.1% | 27.2% |
| 35-45% | 725 | 39.0% | 44.0% |
| 45-55% | 362 | 48.7% | 46.7% |
| 55-65% | 135 | 58.0% | 57.0% |
| 65-75% | 12 | 66.8% | 91.7% |

### Point chance by role

| Role | N | Avg predicted | Actual |
|---|---|---|---|
| PP1 | 1761 | 53.9% | 58.0% |
| PP2 | 1670 | 36.7% | 35.7% |
| no PP | 2383 | 23.7% | 21.8% |

## Does recent form add anything? (predicted vs actual by last-3 and last-10 hits)


### Point, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 1529 | 26.3% | 26.2% |
| 1/3 | 1838 | 35.0% | 34.1% |
| 2/3 | 1209 | 45.3% | 46.3% |
| 3/3 | 433 | 55.3% | 58.2% |

### Goal, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 3068 | 12.7% | 12.9% |
| 1/3 | 1497 | 20.2% | 19.8% |
| 2/3 | 401 | 26.1% | 24.4% |
| 3/3 | 43 | 34.2% | 32.6% |

### Assist, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 2245 | 19.8% | 19.2% |
| 1/3 | 1821 | 26.5% | 28.7% |
| 2/3 | 788 | 34.9% | 34.6% |
| 3/3 | 155 | 44.6% | 46.5% |

### Point, by hits in the last 10 games

| Last 10 | N | Avg predicted | Actual |
|---|---|---|---|
| 0-2/10 | 2014 | 23.9% | 24.3% |
| 3-4/10 | 1838 | 34.3% | 32.4% |
| 5-6/10 | 1259 | 47.5% | 48.9% |
| 7-8/10 | 602 | 58.0% | 60.8% |
| 9-10/10 | 101 | 67.1% | 70.3% |

### Point and goal, by the game's projected total

| Projected total | Market | N | Avg predicted | Actual |
|---|---|---|---|---|
| 0-5.9 | Point | 1771 | 35.6% | 36.6% |
| 0-5.9 | Goal | 1771 | 15.7% | 16.0% |
| 5.9-6.2 | Point | 2262 | 36.7% | 36.6% |
| 5.9-6.2 | Goal | 2262 | 16.2% | 15.4% |
| 6.2-6.4 | Point | 1167 | 37.3% | 35.2% |
| 6.2-6.4 | Goal | 1167 | 16.5% | 15.7% |
| 6.4-9 | Point | 614 | 37.9% | 40.9% |
| 6.4-9 | Goal | 614 | 16.8% | 18.4% |

## Game totals

Games: 239. Average projected total 6.07, actual 6.37 (actual minus projected: +0.30).
Mean absolute error 1.86 goals, against 1.86 for a flat guess at the average.

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
| 2026-11-14 | SEA@CAR | 6.34 | 6 |
| 2026-11-14 | WPG@CHI | 5.86 | 9 |
| 2026-11-14 | MIN@BOS | 5.88 | 8 |
| 2026-11-14 | EDM@TOR | 6.56 | 1 |
| 2026-11-14 | COL@MTL | 6.40 | 5 |
| 2026-11-14 | DET@TBL | 6.21 | 2 |
| 2026-11-14 | OTT@PIT | 6.35 | 5 |
| 2026-11-14 | NJD@WSH | 6.15 | 11 |
| 2026-11-14 | PHI@CBJ | 5.53 | 7 |
| 2026-11-14 | FLA@STL | 5.85 | 5 |
| 2026-11-14 | BUF@DAL | 6.13 | 2 |
| 2026-11-14 | SJS@UTA | 6.31 | 11 |
| 2026-11-14 | NYI@ANA | 6.28 | 8 |
| 2026-11-14 | CGY@LAK | 5.50 | 5 |
| 2026-11-15 | EDM@PHI | 5.86 | 7 |
| 2026-11-15 | FLA@DAL | 5.89 | 3 |
| 2026-11-15 | CGY@ANA | 6.04 | 7 |
| 2026-11-15 | VAN@VGK | 6.24 | 9 |
| 2026-11-15 | NSH@SJS | 5.78 | 6 |
| 2026-11-16 | MTL@NYR | 6.02 | 4 |
| 2026-11-16 | VAN@UTA | 6.44 | 5 |
| 2026-11-17 | LAK@BOS | 6.03 | 3 |
| 2026-11-17 | EDM@FLA | 6.01 | 7 |
| 2026-11-17 | CBJ@NYI | 5.78 | 6 |
| 2026-11-17 | BUF@PHI | 5.85 | 7 |
| 2026-11-17 | OTT@WPG | 6.09 | 3 |
| 2026-11-17 | WSH@TBL | 6.53 | 7 |
| 2026-11-17 | TOR@CHI | 6.10 | 9 |
| 2026-11-17 | ANA@STL | 6.26 | 14 |
| 2026-11-17 | NSH@MIN | 5.67 | 10 |
| 2026-11-17 | DAL@VGK | 5.97 | 7 |
| 2026-11-17 | CGY@SJS | 5.78 | 7 |
| 2026-11-18 | BOS@DET | 5.98 | 5 |
| 2026-11-18 | MTL@NJD | 6.10 | 5 |
| 2026-11-18 | COL@UTA | 6.64 | 5 |

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
- 2026-11-14: 64 skaters in the report, 1 not matched to a final box score
- 2026-11-15: 169 skaters in the report, 4 not matched to a final box score
- 2026-11-16: 62 skaters in the report, 1 not matched to a final box score
- 2026-11-17: 363 skaters in the report, 5 not matched to a final box score
- 2026-11-18: 100 skaters in the report, 0 not matched to a final box score
- 2026-11-19: report has no skater section; skipped
