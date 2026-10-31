# Projection scoreboard

Updated 2026-10-31 16:58 ET. Uses the last slate report committed before first puck each day.
Brier and log-loss: lower is better. 'Naive' guesses the same average for everyone; the model should beat it.

## Skater chances, 1+ goal / point / assist

| Market | N | Avg predicted | Actual rate | Brier | Naive Brier | Log-loss | Naive log-loss |
|---|---|---|---|---|---|---|---|
| Goal | 3031 | 16.4% | 16.4% | 0.1289 | 0.1373 | 0.4170 | 0.4467 |
| Point | 3031 | 36.8% | 37.5% | 0.2104 | 0.2343 | 0.6096 | 0.6615 |
| Assist | 3031 | 25.4% | 26.0% | 0.1793 | 0.1922 | 0.5412 | 0.5727 |

### Calibration, Goal

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 1448 | 7.6% | 8.5% |
| 15-25% | 971 | 19.2% | 18.5% |
| 25-35% | 420 | 28.8% | 27.9% |
| 35-45% | 176 | 39.7% | 39.2% |
| 45-55% | 16 | 46.9% | 56.2% |

### Calibration, Point

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 158 | 11.4% | 15.2% |
| 15-25% | 635 | 19.9% | 21.4% |
| 25-35% | 726 | 29.6% | 29.2% |
| 35-45% | 587 | 39.2% | 39.0% |
| 45-55% | 407 | 49.1% | 50.6% |
| 55-65% | 345 | 59.4% | 62.6% |
| 65-75% | 153 | 68.5% | 62.7% |
| 75-100% | 20 | 78.8% | 85.0% |

### Calibration, Assist

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 555 | 10.8% | 14.6% |
| 15-25% | 1090 | 19.3% | 19.7% |
| 25-35% | 739 | 29.2% | 25.8% |
| 35-45% | 386 | 39.0% | 44.3% |
| 45-55% | 187 | 48.8% | 48.1% |
| 55-65% | 69 | 58.1% | 49.3% |
| 65-75% | 5 | 65.6% | 100.0% |

### Point chance by role

| Role | N | Avg predicted | Actual |
|---|---|---|---|
| PP1 | 919 | 53.9% | 59.1% |
| PP2 | 874 | 36.8% | 35.8% |
| no PP | 1238 | 24.0% | 22.6% |

## Does recent form add anything? (predicted vs actual by last-3 and last-10 hits)


### Point, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 691 | 26.2% | 27.5% |
| 1/3 | 823 | 35.9% | 34.9% |
| 2/3 | 540 | 46.3% | 50.0% |
| 3/3 | 172 | 53.9% | 52.9% |

### Goal, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 1368 | 12.9% | 13.2% |
| 1/3 | 667 | 20.5% | 22.3% |
| 2/3 | 171 | 26.2% | 24.0% |
| 3/3 | 20 | 34.4% | 30.0% |

### Assist, by hits in the last 3 games

| Last 3 | N | Avg predicted | Actual |
|---|---|---|---|
| 0/3 | 999 | 19.9% | 20.7% |
| 1/3 | 841 | 27.0% | 30.1% |
| 2/3 | 326 | 35.0% | 29.4% |
| 3/3 | 60 | 43.4% | 46.7% |

### Point, by hits in the last 10 games

| Last 10 | N | Avg predicted | Actual |
|---|---|---|---|
| 0-2/10 | 1039 | 23.8% | 25.1% |
| 3-4/10 | 994 | 35.1% | 32.9% |
| 5-6/10 | 688 | 48.0% | 51.6% |
| 7-8/10 | 273 | 59.3% | 61.9% |
| 9-10/10 | 37 | 68.5% | 64.9% |

### Point and goal, by the game's projected total

| Projected total | Market | N | Avg predicted | Actual |
|---|---|---|---|---|
| 0-5.9 | Point | 855 | 36.2% | 39.4% |
| 0-5.9 | Goal | 855 | 16.1% | 17.3% |
| 5.9-6.2 | Point | 1162 | 36.4% | 37.1% |
| 5.9-6.2 | Goal | 1162 | 16.2% | 15.7% |
| 6.2-6.4 | Point | 708 | 37.2% | 34.2% |
| 6.2-6.4 | Goal | 708 | 16.5% | 15.4% |
| 6.4-9 | Point | 306 | 38.8% | 41.2% |
| 6.4-9 | Goal | 306 | 17.3% | 19.0% |

## Game totals

Games: 113. Average projected total 6.07, actual 6.46 (actual minus projected: +0.39).
Mean absolute error 1.86 goals, against 1.87 for a flat guess at the average.

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
- 2026-10-31: 186 skaters in the report, 96 not matched to a final box score
