# Ice Engine pattern backtest (2026-10-27)
Regular season, every skater, last season + this season. Each game uses only games before it.
Baseline = last-60-game rate shrunk toward the league rate for F or D. Diff = actual minus baseline, in percentage points.
z: |2| or more is unlikely to be luck. Many buckets are tested, so a lone 2-3 can still be luck; trust an effect that shows in BOTH seasons.

## Points

### venue edge (same-venue last 20 vs last 20)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| same (within 5) | 14002 | 36.0 | 35.8 | +0.3 | +0.7 | +0.2 (+0.6), n=11459 | +0.3 (+0.3), n=2543 |
| worse here (-5 to -15) | 7145 | 37.0 | 37.5 | -0.6 | -1.0 | -0.6 (-1.0), n=5984 | -0.2 (-0.2), n=1161 |
| better here (+5 to +15) | 7294 | 37.0 | 37.3 | -0.3 | -0.6 | -0.2 (-0.3), n=6069 | -0.9 (-0.7), n=1225 |
| much better here (+15 or more) | 2981 | 38.7 | 39.1 | -0.4 | -0.5 | -0.3 (-0.4), n=2403 | -0.6 (-0.3), n=578 |
| much worse here (-15 pts or more) | 2984 | 40.0 | 39.3 | +0.7 | +0.8 | +1.6 (+1.7), n=2488 | -3.8 (-1.8), n=496 |

### steady (longest miss run in last 20)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| 4 or more | 25223 | 31.0 | 31.4 | -0.4 | -1.3 | -0.2 (-0.7), n=20949 | -1.2 (-1.8), n=4274 |
| 3 | 4676 | 48.1 | 47.3 | +0.8 | +1.1 | +0.4 (+0.5), n=3703 | +2.0 (+1.3), n=973 |
| 2 or less | 4613 | 58.5 | 57.9 | +0.6 | +0.9 | +0.7 (+0.9), n=3851 | +0.3 (+0.2), n=762 |

### blocks (every 5-game block has 2+ hits)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| no | 26519 | 31.3 | 31.8 | -0.5 | -1.7 | -0.4 (-1.3), n=21897 | -0.8 (-1.2), n=4622 |
| yes | 7993 | 55.6 | 54.5 | +1.1 | +2.1 | +1.3 (+2.1), n=6606 | +0.5 (+0.4), n=1387 |

### shots per game, last 10
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| under 1.5 | 16576 | 26.2 | 28.2 | -1.9 | -5.7 | -1.9 (-5.1), n=13434 | -2.0 (-2.6), n=3142 |
| 1.5-2.2 | 9600 | 40.0 | 39.8 | +0.2 | +0.4 | +0.1 (+0.2), n=8020 | +0.5 (+0.4), n=1580 |
| 2.2-3.0 | 5659 | 51.8 | 49.0 | +2.8 | +4.3 | +2.9 (+4.1), n=4782 | +2.2 (+1.3), n=877 |
| 3.0+ | 2677 | 61.3 | 57.0 | +4.3 | +4.6 | +4.7 (+4.7), n=2267 | +1.7 (+0.7), n=410 |

### hit each of last 3
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| no | 31720 | 35.6 | 35.6 | -0.0 | -0.1 | +0.1 (+0.3), n=26138 | -0.5 (-0.8), n=5582 |
| yes | 2792 | 52.4 | 53.3 | -0.9 | -1.0 | -1.0 (-1.0), n=2365 | -0.2 (-0.1), n=427 |

### all games (baseline check)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| all | 34512 | 37.0 | 37.1 | -0.1 | -0.4 | -0.0 (-0.0), n=28503 | -0.5 (-0.8), n=6009 |

### alternating (5+ flips in last 8)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| last game hit | 2283 | 45.6 | 43.2 | +2.5 | +2.5 | +2.5 (+2.2), n=1880 | +2.4 (+1.0), n=403 |
| last game MISS | 2482 | 38.9 | 41.3 | -2.4 | -2.5 | -2.4 (-2.3), n=2040 | -2.2 (-1.0), n=442 |

### steady players: straight misses right now
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| 2 | 569 | 54.0 | 52.7 | +1.3 | +0.6 | +2.4 (+1.1), n=486 | -5.4 (-1.0), n=83 |
| 0 | 2833 | 60.1 | 59.6 | +0.6 | +0.6 | +1.0 (+1.0), n=2373 | -1.6 (-0.7), n=460 |
| 1 | 1211 | 56.7 | 56.3 | +0.5 | +0.3 | -0.9 (-0.6), n=992 | +6.5 (+2.0), n=219 |

## Assists

### venue edge (same-venue last 20 vs last 20)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| same (within 5) | 15068 | 25.1 | 24.8 | +0.3 | +0.9 | +0.4 (+1.0), n=12461 | +0.0 (+0.0), n=2607 |
| worse here (-5 to -15) | 7195 | 25.4 | 25.5 | -0.1 | -0.2 | -0.1 (-0.1), n=5951 | -0.3 (-0.3), n=1244 |
| better here (+5 to +15) | 7232 | 24.9 | 25.3 | -0.4 | -0.8 | -0.6 (-1.1), n=5995 | +0.6 (+0.5), n=1237 |
| much better here (+15 or more) | 2450 | 28.4 | 29.7 | -1.2 | -1.4 | -1.2 (-1.2), n=1971 | -1.3 (-0.7), n=479 |
| much worse here (-15 pts or more) | 2461 | 30.9 | 29.8 | +1.0 | +1.2 | +1.7 (+1.7), n=2025 | -1.9 (-0.9), n=436 |

### steady (longest miss run in last 20)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| 4 or more | 30659 | 23.6 | 23.7 | -0.1 | -0.3 | -0.0 (-0.1), n=25332 | -0.2 (-0.4), n=5327 |
| 3 | 2511 | 40.2 | 40.0 | +0.3 | +0.3 | -0.0 (-0.0), n=2075 | +1.6 (+0.7), n=436 |
| 2 or less | 1342 | 47.8 | 47.3 | +0.6 | +0.4 | +1.2 (+0.8), n=1096 | -2.5 (-0.8), n=246 |

### blocks (every 5-game block has 2+ hits)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| no | 31742 | 24.0 | 24.1 | -0.0 | -0.1 | +0.0 (+0.1), n=26203 | -0.2 (-0.4), n=5539 |
| yes | 2770 | 45.3 | 45.2 | +0.1 | +0.1 | +0.0 (+0.0), n=2300 | +0.1 (+0.1), n=470 |

### shots per game, last 10
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| under 1.5 | 16576 | 18.4 | 20.0 | -1.6 | -5.3 | -1.7 (-5.0), n=13434 | -1.3 (-1.9), n=3142 |
| 1.5-2.2 | 9600 | 27.4 | 27.5 | -0.1 | -0.2 | -0.1 (-0.2), n=8020 | -0.3 (-0.2), n=1580 |
| 2.2-3.0 | 5659 | 36.5 | 33.6 | +3.0 | +4.8 | +3.2 (+4.8), n=4782 | +1.6 (+1.0), n=877 |
| 3.0+ | 2677 | 42.6 | 38.7 | +3.9 | +4.2 | +3.7 (+3.7), n=2267 | +4.9 (+2.1), n=410 |

### hit each of last 3
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| no | 33493 | 25.4 | 25.3 | +0.1 | +0.3 | +0.1 (+0.6), n=27649 | -0.3 (-0.5), n=5844 |
| yes | 1019 | 38.0 | 40.8 | -2.8 | -1.9 | -4.1 (-2.5), n=854 | +3.5 (+0.9), n=165 |

### all games (baseline check)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| all | 34512 | 25.7 | 25.8 | -0.0 | -0.1 | +0.0 (+0.1), n=28503 | -0.2 (-0.3), n=6009 |

### alternating (5+ flips in last 8)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| last game hit | 1565 | 35.1 | 34.9 | +0.2 | +0.2 | +0.5 (+0.4), n=1324 | -1.4 (-0.5), n=241 |
| last game MISS | 1895 | 32.7 | 33.7 | -1.0 | -0.9 | -0.9 (-0.8), n=1582 | -1.3 (-0.5), n=313 |

### steady players: straight misses right now
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| 0 | 697 | 48.8 | 49.2 | -0.4 | -0.2 | -0.3 (-0.1), n=577 | -0.7 (-0.2), n=120 |
| 1 | 405 | 47.4 | 46.4 | +1.0 | +0.4 | +3.4 (+1.2), n=331 | -9.4 (-1.6), n=74 |
| 2 | 240 | 45.8 | 43.4 | +2.4 | +0.8 | +2.2 (+0.6), n=188 | +3.3 (+0.5), n=52 |

## Goals

### venue edge (same-venue last 20 vs last 20)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| better here (+5 to +15) | 7256 | 16.3 | 15.9 | +0.3 | +0.8 | +0.4 (+0.9), n=5913 | -0.0 (-0.0), n=1343 |
| worse here (-5 to -15) | 7474 | 16.5 | 16.0 | +0.5 | +1.2 | +0.5 (+1.0), n=6196 | +0.8 (+0.8), n=1278 |
| same (within 5) | 16489 | 15.5 | 15.3 | +0.2 | +0.9 | +0.4 (+1.3), n=13732 | -0.6 (-0.9), n=2757 |
| much better here (+15 or more) | 1588 | 21.0 | 23.1 | -2.1 | -2.0 | -1.5 (-1.3), n=1240 | -4.1 (-1.9), n=348 |
| much worse here (-15 pts or more) | 1599 | 21.7 | 23.4 | -1.7 | -1.6 | -1.4 (-1.2), n=1322 | -3.1 (-1.2), n=277 |

### steady (longest miss run in last 20)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| 4 or more | 33214 | 15.8 | 15.6 | +0.2 | +1.2 | +0.4 (+1.7), n=27454 | -0.4 (-0.8), n=5760 |
| 3 | 1065 | 31.1 | 34.2 | -3.1 | -2.2 | -3.5 (-2.1), n=851 | -1.8 (-0.6), n=214 |
| 2 or less | 233 | 35.2 | 39.0 | -3.8 | -1.2 | -2.6 (-0.8), n=198 | -10.3 (-1.3), n=35 |

### blocks (every 5-game block has 1+ hits)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| no | 28477 | 14.1 | 13.6 | +0.4 | +2.3 | +0.6 (+2.7), n=23476 | -0.2 (-0.4), n=5001 |
| yes | 6035 | 27.3 | 28.9 | -1.5 | -2.7 | -1.4 (-2.3), n=5027 | -2.1 (-1.5), n=1008 |

### shots per game, last 10
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| under 1.5 | 16576 | 10.1 | 10.7 | -0.7 | -2.8 | -0.6 (-2.2), n=13434 | -1.1 (-2.0), n=3142 |
| 1.5-2.2 | 9600 | 18.0 | 17.4 | +0.6 | +1.5 | +0.6 (+1.5), n=8020 | +0.3 (+0.4), n=1580 |
| 2.2-3.0 | 5659 | 24.5 | 23.8 | +0.7 | +1.2 | +0.8 (+1.4), n=4782 | -0.1 (-0.0), n=877 |
| 3.0+ | 2677 | 33.0 | 31.1 | +1.9 | +2.1 | +2.3 (+2.4), n=2267 | -0.3 (-0.1), n=410 |

### goal heat (3+ goals in last 10, 3+ shots, last 5 above season rate)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| no | 33194 | 15.7 | 15.6 | +0.0 | +0.2 | +0.2 (+0.9), n=27364 | -0.7 (-1.4), n=5830 |
| yes | 1318 | 34.1 | 32.7 | +1.5 | +1.1 | +0.9 (+0.7), n=1139 | +4.9 (+1.4), n=179 |

### hit each of last 3
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| no | 34182 | 16.3 | 16.1 | +0.1 | +0.8 | +0.3 (+1.4), n=28218 | -0.5 (-1.1), n=5964 |
| yes | 330 | 27.0 | 31.9 | -4.9 | -2.0 | -6.0 (-2.2), n=285 | +1.6 (+0.2), n=45 |

### all games (baseline check)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| all | 34512 | 16.4 | 16.3 | +0.1 | +0.5 | +0.2 (+1.1), n=28503 | -0.5 (-1.1), n=6009 |

### alternating (5+ flips in last 8)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| last game hit | 772 | 26.4 | 28.1 | -1.7 | -1.0 | -2.3 (-1.3), n=652 | +1.7 (+0.4), n=120 |
| last game MISS | 1030 | 24.3 | 26.8 | -2.6 | -1.9 | -2.7 (-1.9), n=869 | -1.7 (-0.5), n=161 |

### steady players: straight misses right now
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| 2 | 60 | 36.7 | 36.9 | -0.3 | -0.0 | -1.3 (-0.2), n=50 | +5.0 (+0.3), n=10 |
| 1 | 73 | 32.9 | 38.9 | -6.0 | -1.1 | -5.3 (-0.9), n=60 | -9.3 (-0.7), n=13 |
| 0 | 100 | 36.0 | 40.2 | -4.2 | -0.9 | -1.5 (-0.3), n=88 | -24.2 (-1.7), n=12 |

