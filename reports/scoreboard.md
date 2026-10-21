# Projection scoreboard

Updated 2026-10-21 06:49 ET. Uses the last slate report committed before first puck each day.
Brier and log-loss: lower is better. 'Naive' guesses the same average for everyone; the model should beat it.

## Skater chances, 1+ goal / point / assist

| Market | N | Avg predicted | Actual rate | Brier | Naive Brier | Log-loss | Naive log-loss |
|---|---|---|---|---|---|---|---|
| Goal | 1142 | 16.4% | 15.6% | 0.1234 | 0.1316 | 0.4054 | 0.4328 |
| Point | 1142 | 36.9% | 36.7% | 0.2088 | 0.2323 | 0.6056 | 0.6573 |
| Assist | 1142 | 25.6% | 25.0% | 0.1759 | 0.1877 | 0.5324 | 0.5628 |

### Calibration, Goal

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 548 | 7.6% | 7.3% |
| 15-25% | 363 | 19.3% | 19.0% |
| 25-35% | 157 | 29.0% | 23.6% |
| 35-45% | 68 | 39.8% | 41.2% |
| 45-55% | 6 | 47.0% | 66.7% |

### Calibration, Point

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 56 | 11.1% | 8.9% |
| 15-25% | 245 | 19.9% | 22.0% |
| 25-35% | 267 | 29.5% | 28.5% |
| 35-45% | 223 | 39.2% | 39.0% |
| 45-55% | 151 | 49.1% | 48.3% |
| 55-65% | 131 | 59.1% | 59.5% |
| 65-75% | 60 | 68.7% | 63.3% |
| 75-100% | 9 | 77.9% | 88.9% |

### Calibration, Assist

| Predicted | N | Avg predicted | Actual |
|---|---|---|---|
| 0-15% | 201 | 10.7% | 13.4% |
| 15-25% | 420 | 19.2% | 18.3% |
| 25-35% | 264 | 29.2% | 26.9% |
| 35-45% | 160 | 38.8% | 40.6% |
| 45-55% | 66 | 49.1% | 43.9% |
| 55-65% | 30 | 58.3% | 53.3% |
| 65-75% | 1 | 65.0% | 100.0% |

### Point chance by role

| Role | N | Avg predicted | Actual |
|---|---|---|---|
| PP1 | 342 | 54.3% | 56.7% |
| PP2 | 324 | 36.9% | 37.7% |
| no PP | 476 | 24.3% | 21.6% |

## Game totals

Games: 44. Average projected total 6.11, actual 6.20 (actual minus projected: +0.10).
Mean absolute error 1.59 goals, against 1.65 for a flat guess at the average.

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

## Data notes

- 2026-10-15: 359 skaters in the report, 9 not matched to a final box score
- 2026-10-16: 61 skaters in the report, 1 not matched to a final box score
- 2026-10-17: 226 skaters in the report, 4 not matched to a final box score
- 2026-10-18: 60 skaters in the report, 1 not matched to a final box score
- 2026-10-19: 119 skaters in the report, 5 not matched to a final box score
- 2026-10-20: 342 skaters in the report, 5 not matched to a final box score
