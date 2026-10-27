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

### shot attempts per game, last 10
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| D: 3-4 | 2709 | 29.8 | 30.4 | -0.6 | -0.7 | -0.6 (-0.7), n=2270 | -0.7 (-0.3), n=439 |
| D: 4-5 | 1655 | 39.8 | 37.6 | +2.3 | +1.9 | +2.3 (+1.8), n=1418 | +2.0 (+0.6), n=237 |
| D: 5+ | 1397 | 50.3 | 46.1 | +4.2 | +3.2 | +4.4 (+3.1), n=1182 | +2.9 (+0.9), n=215 |
| F: 4-5 | 3750 | 50.7 | 49.0 | +1.7 | +2.2 | +2.0 (+2.3), n=3204 | +0.1 (+0.0), n=546 |
| F: 3-4 | 5177 | 41.9 | 41.6 | +0.3 | +0.4 | +0.1 (+0.2), n=4252 | +1.1 (+0.7), n=925 |
| F: under 3 | 9688 | 28.9 | 31.2 | -2.3 | -4.9 | -2.4 (-4.6), n=7818 | -1.9 (-1.8), n=1870 |
| F: 6+ | 1905 | 63.0 | 58.9 | +4.2 | +3.8 | +4.2 (+3.4), n=1593 | +4.3 (+1.6), n=312 |
| F: 5-6 | 2193 | 56.8 | 53.9 | +3.0 | +2.8 | +3.0 (+2.6), n=1855 | +2.7 (+1.0), n=338 |
| D: 2-3 | 3894 | 22.7 | 24.2 | -1.5 | -2.2 | -1.2 (-1.7), n=3197 | -2.7 (-1.7), n=697 |
| D: under 2 | 2144 | 18.1 | 20.7 | -2.6 | -3.0 | -2.3 (-2.4), n=1714 | -3.6 (-1.9), n=430 |

### hit each of last 3
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| no | 31720 | 35.6 | 35.6 | -0.0 | -0.1 | +0.1 (+0.3), n=26138 | -0.5 (-0.8), n=5582 |
| yes | 2792 | 52.4 | 53.3 | -0.9 | -1.0 | -1.0 (-1.0), n=2365 | -0.2 (-0.1), n=427 |

### recency: last-20 rate minus 60-game baseline
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| L20 above (+3 to +8) | 6208 | 42.1 | 41.6 | +0.5 | +0.9 | +0.7 (+1.0), n=5251 | -0.1 (-0.1), n=957 |
| L20 well above baseline (+8 or more) | 5773 | 47.2 | 46.5 | +0.7 | +1.2 | +1.1 (+1.6), n=4767 | -1.0 (-0.6), n=1006 |
| L20 near baseline | 9928 | 35.2 | 35.9 | -0.6 | -1.3 | -0.5 (-1.1), n=8261 | -1.0 (-0.9), n=1667 |
| L20 below (-3 to -8) | 7203 | 30.8 | 31.2 | -0.4 | -0.7 | -0.6 (-1.0), n=5898 | +0.6 (+0.5), n=1305 |
| L20 well below (-8 or less) | 5400 | 31.5 | 31.8 | -0.4 | -0.6 | -0.2 (-0.4), n=4326 | -1.0 (-0.7), n=1074 |

### recency: last-10 rate minus 60-game baseline
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| L10 well above baseline (+15 or more) | 4577 | 44.7 | 43.9 | +0.7 | +1.0 | +0.7 (+0.9), n=3812 | +0.8 (+0.5), n=765 |
| L10 above (+5 to +15) | 7040 | 40.1 | 40.0 | +0.1 | +0.2 | -0.2 (-0.4), n=5897 | +1.7 (+1.3), n=1143 |
| L10 near baseline | 10009 | 35.9 | 36.2 | -0.3 | -0.7 | +0.2 (+0.3), n=8263 | -2.6 (-2.4), n=1746 |
| L10 below (-5 to -15) | 8597 | 33.1 | 33.1 | -0.0 | -0.1 | +0.0 (+0.1), n=7025 | -0.4 (-0.3), n=1572 |
| L10 well below (-15 or less) | 4289 | 33.8 | 34.7 | -0.8 | -1.2 | -0.9 (-1.2), n=3506 | -0.6 (-0.3), n=783 |

### USER METHOD: L10 form at the bar but same-venue L10 below the bar
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| venue form weak | 2494 | 47.2 | 47.7 | -0.5 | -0.5 | -0.0 (-0.0), n=2099 | -3.1 (-1.3), n=395 |

### current hit run (games in a row with a hit)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| 0 | 21783 | 32.6 | 33.1 | -0.5 | -1.8 | -0.5 (-1.4), n=17908 | -0.9 (-1.3), n=3875 |
| 1 | 7083 | 40.4 | 39.5 | +0.9 | +1.7 | +1.0 (+1.6), n=5864 | +0.8 (+0.6), n=1219 |
| 2 | 2854 | 46.8 | 45.2 | +1.6 | +1.8 | +2.1 (+2.1), n=2366 | -0.5 (-0.2), n=488 |
| 3 | 1330 | 50.6 | 49.8 | +0.8 | +0.6 | +0.5 (+0.3), n=1111 | +2.2 (+0.7), n=219 |
| 4+ | 1462 | 54.0 | 56.4 | -2.4 | -1.9 | -2.4 (-1.7), n=1254 | -2.6 (-0.8), n=208 |

### all games (baseline check)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| all | 34512 | 37.0 | 37.1 | -0.1 | -0.4 | -0.0 (-0.0), n=28503 | -0.5 (-0.8), n=6009 |

### alternating (5+ flips in last 8)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| last game hit | 2283 | 45.6 | 43.2 | +2.5 | +2.5 | +2.5 (+2.2), n=1880 | +2.4 (+1.0), n=403 |
| last game MISS | 2482 | 38.9 | 41.3 | -2.4 | -2.5 | -2.4 (-2.3), n=2040 | -2.2 (-1.0), n=442 |

### USER METHOD: L10 form and same-venue L10 form both at the bar (points 6+, assists 4+, goals 3+)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| both at the bar, hit last game | 3537 | 59.3 | 58.2 | +1.1 | +1.4 | +1.1 (+1.2), n=2975 | +1.3 (+0.6), n=562 |
| both at the bar, missed last game (off night) | 1422 | 58.4 | 56.6 | +1.8 | +1.4 | +2.1 (+1.4), n=1184 | +0.6 (+0.2), n=238 |

### PATTERN: 3 straight misses after a pattern that never missed more than 2
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| no, had longer miss runs before | 2508 | 28.5 | 30.9 | -2.4 | -2.7 | -2.4 (-2.5), n=2051 | -2.3 (-1.1), n=457 |
| yes | 280 | 47.9 | 48.9 | -1.0 | -0.4 | -2.5 (-0.8), n=229 | +5.8 (+0.8), n=51 |

### USER METHOD: L10 below the bar but same-venue L10 at the bar
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| venue form strong only | 2424 | 47.8 | 47.8 | -0.1 | -0.1 | +0.7 (+0.6), n=1930 | -3.0 (-1.4), n=494 |

### USER METHOD: both at the bar and 1-2 straight misses (off night or two)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| yes | 1363 | 58.5 | 56.6 | +1.8 | +1.4 | +2.0 (+1.4), n=1134 | +0.9 (+0.3), n=229 |

### PATTERN: 2 misses right after a 2-hit run (MM after HH)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| any history | 1269 | 36.2 | 37.8 | -1.6 | -1.2 | -1.2 (-0.8), n=1043 | -3.8 (-1.2), n=226 |
| history never missed more than 2 | 315 | 54.6 | 54.8 | -0.2 | -0.1 | +1.7 (+0.6), n=270 | -11.9 (-1.6), n=45 |

### long-history venue edge (all prior same-venue games, 30+ there, vs all prior games)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| venue same (within 4) | 5977 | 38.9 | 38.5 | +0.4 | +0.6 | +0.9 (+1.1), n=3326 | -0.2 (-0.3), n=2651 |
| venue a bit better (+4 to +10) | 2198 | 38.4 | 38.8 | -0.4 | -0.4 | +0.2 (+0.2), n=1249 | -1.1 (-0.8), n=949 |
| venue a bit worse (-4 to -10) | 2192 | 38.0 | 39.2 | -1.1 | -1.1 | -2.1 (-1.6), n=1251 | +0.1 (+0.1), n=941 |
| venue much worse (-10 or more) | 359 | 47.6 | 43.2 | +4.5 | +1.8 | +6.7 (+2.1), n=233 | +0.4 (+0.1), n=126 |
| venue much better (+10 or more) | 339 | 43.4 | 42.9 | +0.5 | +0.2 | -2.3 (-0.7), n=201 | +4.5 (+1.1), n=138 |

### forwards: games with 4+ attempts, last 10
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| 5-6 of 10 | 4411 | 46.3 | 45.4 | +0.9 | +1.3 | +1.5 (+1.9), n=3708 | -2.3 (-1.2), n=703 |
| 0-4 of 10 | 12573 | 31.6 | 33.4 | -1.8 | -4.4 | -2.0 (-4.3), n=10201 | -1.0 (-1.1), n=2372 |
| 9-10 of 10 games with 4+ attempts | 2015 | 61.8 | 57.4 | +4.4 | +4.1 | +4.5 (+3.8), n=1703 | +4.1 (+1.5), n=312 |
| 7-8 of 10 | 3714 | 55.3 | 52.6 | +2.7 | +3.4 | +2.5 (+2.8), n=3110 | +4.0 (+2.0), n=604 |

### forwards: games with 5+ attempts, last 10
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| 0-4 of 10 | 16688 | 35.4 | 36.4 | -1.0 | -2.9 | -1.1 (-2.6), n=13647 | -0.9 (-1.1), n=3041 |
| 5-7 of 10 | 4474 | 54.7 | 52.1 | +2.7 | +3.6 | +2.8 (+3.5), n=3791 | +1.8 (+1.0), n=683 |
| 8-10 of 10 games with 5+ attempts | 1551 | 62.5 | 58.8 | +3.8 | +3.1 | +3.5 (+2.6), n=1284 | +5.1 (+1.7), n=267 |

### mid volume by goals in last 10
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| mid volume, 0-1 goals in last 10 | 1391 | 45.5 | 42.2 | +3.3 | +2.5 | +2.6 (+1.8), n=1191 | +7.7 (+2.2), n=200 |
| mid volume, 2+ goals in last 10 | 4392 | 49.7 | 48.6 | +1.1 | +1.5 | +1.6 (+2.1), n=3716 | -1.9 (-1.0), n=676 |

### PATTERN: 4 straight misses after a pattern that never missed more than 2
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| yes | 157 | 49.0 | 46.1 | +3.0 | +0.8 | +1.9 (+0.4), n=135 | +9.9 (+0.9), n=22 |

### high volume (5+ attempts or 3+ shots a game) by goals in last 10
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| high volume, 3+ goals in last 10 (hot) | 3043 | 61.5 | 57.9 | +3.6 | +4.1 | +3.4 (+3.5), n=2567 | +4.6 (+2.1), n=476 |
| high volume, 2 goals in last 10 | 771 | 55.0 | 52.1 | +2.9 | +1.6 | +3.5 (+1.8), n=659 | -0.6 (-0.1), n=112 |
| high volume, 0-1 goals in last 10 (sleeper) | 401 | 54.6 | 49.6 | +5.1 | +2.1 | +6.0 (+2.2), n=312 | +1.6 (+0.3), n=89 |

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

### shot attempts per game, last 10
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| D: 3-4 | 2709 | 24.4 | 24.9 | -0.5 | -0.6 | -0.5 (-0.5), n=2270 | -0.3 (-0.1), n=439 |
| D: 4-5 | 1655 | 31.6 | 30.1 | +1.5 | +1.4 | +1.7 (+1.5), n=1418 | +0.3 (+0.1), n=237 |
| D: 5+ | 1397 | 40.5 | 37.4 | +3.1 | +2.5 | +2.5 (+1.8), n=1182 | +6.2 (+1.9), n=215 |
| F: 4-5 | 3750 | 34.1 | 32.3 | +1.8 | +2.4 | +2.0 (+2.5), n=3204 | +0.5 (+0.3), n=546 |
| F: 3-4 | 5177 | 26.8 | 26.9 | -0.1 | -0.1 | +0.1 (+0.1), n=4252 | -0.7 (-0.5), n=925 |
| F: under 3 | 9688 | 18.4 | 20.0 | -1.6 | -4.0 | -1.8 (-4.1), n=7818 | -0.7 (-0.8), n=1870 |
| F: 6+ | 1905 | 42.6 | 39.4 | +3.3 | +3.0 | +2.7 (+2.2), n=1593 | +6.3 (+2.3), n=312 |
| F: 5-6 | 2193 | 38.4 | 35.5 | +2.9 | +2.9 | +3.2 (+3.0), n=1855 | +1.3 (+0.5), n=338 |
| D: 2-3 | 3894 | 18.5 | 19.6 | -1.2 | -1.9 | -1.0 (-1.4), n=3197 | -2.0 (-1.3), n=697 |
| D: under 2 | 2144 | 14.6 | 17.1 | -2.5 | -3.1 | -2.1 (-2.3), n=1714 | -3.9 (-2.2), n=430 |

### hit each of last 3
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| no | 33493 | 25.4 | 25.3 | +0.1 | +0.3 | +0.1 (+0.6), n=27649 | -0.3 (-0.5), n=5844 |
| yes | 1019 | 38.0 | 40.8 | -2.8 | -1.9 | -4.1 (-2.5), n=854 | +3.5 (+0.9), n=165 |

### recency: last-20 rate minus 60-game baseline
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| L20 above (+3 to +8) | 6043 | 29.4 | 28.7 | +0.7 | +1.2 | +0.7 (+1.1), n=4985 | +0.6 (+0.4), n=1058 |
| L20 well above baseline (+8 or more) | 5089 | 35.0 | 34.7 | +0.3 | +0.5 | +0.5 (+0.6), n=4192 | -0.4 (-0.3), n=897 |
| L20 near baseline | 10893 | 23.3 | 23.9 | -0.6 | -1.5 | -0.6 (-1.3), n=9168 | -0.8 (-0.8), n=1725 |
| L20 below (-3 to -8) | 7973 | 22.0 | 21.6 | +0.4 | +0.9 | +0.4 (+0.9), n=6625 | +0.4 (+0.3), n=1348 |
| L20 well below (-8 or less) | 4514 | 23.0 | 23.6 | -0.7 | -1.1 | -0.7 (-1.0), n=3533 | -0.4 (-0.3), n=981 |

### recency: last-10 rate minus 60-game baseline
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| L10 above (+5 to +15) | 6894 | 28.1 | 27.9 | +0.2 | +0.4 | +0.5 (+0.8), n=5747 | -1.1 (-0.9), n=1147 |
| L10 near baseline | 10843 | 24.0 | 24.3 | -0.3 | -0.8 | -0.3 (-0.7), n=8988 | -0.6 (-0.6), n=1855 |
| L10 below (-5 to -15) | 9446 | 22.9 | 22.6 | +0.3 | +0.6 | +0.4 (+0.9), n=7681 | -0.5 (-0.5), n=1765 |
| L10 well below (-15 or less) | 3275 | 26.0 | 26.7 | -0.6 | -0.9 | -1.5 (-1.8), n=2729 | +3.5 (+1.9), n=546 |
| L10 well above baseline (+15 or more) | 4054 | 32.9 | 32.6 | +0.3 | +0.4 | +0.4 (+0.4), n=3358 | +0.2 (+0.1), n=696 |

### USER METHOD: L10 form and same-venue L10 form both at the bar (points 6+, assists 4+, goals 3+)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| both at the bar, missed last game (off night) | 3007 | 39.4 | 38.8 | +0.5 | +0.6 | +0.6 (+0.6), n=2487 | +0.3 (+0.1), n=520 |
| both at the bar, hit last game | 3364 | 40.8 | 41.0 | -0.2 | -0.2 | -0.2 (-0.2), n=2795 | -0.1 (-0.0), n=569 |

### USER METHOD: both at the bar and 1-2 straight misses (off night or two)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| yes | 2427 | 40.4 | 39.4 | +1.0 | +1.0 | +1.4 (+1.3), n=2010 | -0.8 (-0.4), n=417 |

### current hit run (games in a row with a hit)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| 0 | 25649 | 23.8 | 23.8 | -0.0 | -0.1 | +0.0 (+0.0), n=21123 | -0.2 (-0.3), n=4526 |
| 1 | 6061 | 29.3 | 29.1 | +0.2 | +0.3 | +0.4 (+0.6), n=5029 | -1.0 (-0.7), n=1032 |
| 2 | 1783 | 35.3 | 34.2 | +1.2 | +1.1 | +1.3 (+1.1), n=1497 | +0.4 (+0.1), n=286 |
| 3 | 630 | 33.8 | 38.2 | -4.4 | -2.3 | -6.3 (-3.1), n=534 | +5.9 (+1.3), n=96 |
| 4+ | 389 | 44.7 | 45.0 | -0.3 | -0.1 | -0.4 (-0.1), n=320 | +0.0 (+0.0), n=69 |

### all games (baseline check)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| all | 34512 | 25.7 | 25.8 | -0.0 | -0.1 | +0.0 (+0.1), n=28503 | -0.2 (-0.3), n=6009 |

### PATTERN: 2 misses right after a 2-hit run (MM after HH)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| any history | 1063 | 29.6 | 30.3 | -0.6 | -0.5 | -0.3 (-0.2), n=874 | -2.3 (-0.7), n=189 |
| history never missed more than 2 | 110 | 49.1 | 46.0 | +3.0 | +0.6 | +4.0 (+0.8), n=90 | -1.2 (-0.1), n=20 |

### PATTERN: 3 straight misses after a pattern that never missed more than 2
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| no, had longer miss runs before | 2992 | 22.8 | 24.3 | -1.5 | -2.0 | -1.5 (-1.8), n=2448 | -1.4 (-0.8), n=544 |
| yes | 147 | 37.4 | 41.8 | -4.3 | -1.1 | -8.5 (-1.9), n=115 | +10.7 (+1.3), n=32 |

### USER METHOD: L10 form at the bar but same-venue L10 below the bar
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| venue form weak | 3212 | 29.9 | 30.5 | -0.6 | -0.8 | -0.2 (-0.2), n=2648 | -2.7 (-1.4), n=564 |

### USER METHOD: L10 below the bar but same-venue L10 at the bar
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| venue form strong only | 3189 | 30.3 | 30.4 | -0.1 | -0.1 | -0.1 (-0.1), n=2599 | +0.1 (+0.0), n=590 |

### long-history venue edge (all prior same-venue games, 30+ there, vs all prior games)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| venue same (within 4) | 6685 | 25.8 | 25.6 | +0.2 | +0.4 | +0.0 (+0.0), n=3651 | +0.5 (+0.6), n=3034 |
| venue a bit better (+4 to +10) | 1994 | 27.7 | 29.0 | -1.3 | -1.3 | -1.0 (-0.8), n=1168 | -1.6 (-1.1), n=826 |
| venue a bit worse (-4 to -10) | 1981 | 30.4 | 29.4 | +0.9 | +0.9 | +1.3 (+1.0), n=1167 | +0.4 (+0.3), n=814 |
| venue much better (+10 or more) | 190 | 32.6 | 33.6 | -0.9 | -0.3 | -2.3 (-0.6), n=127 | +1.9 (+0.3), n=63 |
| venue much worse (-10 or more) | 215 | 38.1 | 33.9 | +4.3 | +1.3 | +5.0 (+1.3), n=147 | +2.6 (+0.5), n=68 |

### alternating (5+ flips in last 8)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| last game hit | 1565 | 35.1 | 34.9 | +0.2 | +0.2 | +0.5 (+0.4), n=1324 | -1.4 (-0.5), n=241 |
| last game MISS | 1895 | 32.7 | 33.7 | -1.0 | -0.9 | -0.9 (-0.8), n=1582 | -1.3 (-0.5), n=313 |

### forwards: games with 4+ attempts, last 10
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| 5-6 of 10 | 4411 | 30.4 | 29.6 | +0.9 | +1.3 | +1.5 (+2.0), n=3708 | -2.3 (-1.3), n=703 |
| 0-4 of 10 | 12573 | 20.2 | 21.4 | -1.3 | -3.6 | -1.5 (-3.8), n=10201 | -0.4 (-0.5), n=2372 |
| 9-10 of 10 games with 4+ attempts | 2015 | 43.0 | 38.6 | +4.4 | +4.2 | +4.0 (+3.4), n=1703 | +7.0 (+2.6), n=312 |
| 7-8 of 10 | 3714 | 36.6 | 34.8 | +1.9 | +2.5 | +1.9 (+2.3), n=3110 | +1.6 (+0.9), n=604 |

### forwards: games with 5+ attempts, last 10
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| 0-4 of 10 | 16688 | 22.8 | 23.5 | -0.7 | -2.1 | -0.7 (-1.9), n=13647 | -0.6 (-0.8), n=3041 |
| 5-7 of 10 | 4474 | 36.5 | 34.2 | +2.3 | +3.3 | +2.4 (+3.1), n=3791 | +1.8 (+1.0), n=683 |
| 8-10 of 10 games with 5+ attempts | 1551 | 42.6 | 39.7 | +2.9 | +2.4 | +2.4 (+1.8), n=1284 | +5.2 (+1.8), n=267 |

### mid volume by goals in last 10
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| mid volume, 0-1 goals in last 10 | 1391 | 30.8 | 28.6 | +2.2 | +1.9 | +1.7 (+1.3), n=1191 | +5.4 (+1.7), n=200 |
| mid volume, 2+ goals in last 10 | 4392 | 33.4 | 31.5 | +1.9 | +2.8 | +2.5 (+3.4), n=3716 | -1.2 (-0.7), n=676 |

### high volume (5+ attempts or 3+ shots a game) by goals in last 10
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| high volume, 3+ goals in last 10 (hot) | 3043 | 42.0 | 38.1 | +3.9 | +4.6 | +3.6 (+3.8), n=2567 | +5.6 (+2.6), n=476 |
| high volume, 2 goals in last 10 | 771 | 36.6 | 35.3 | +1.3 | +0.8 | +1.4 (+0.8), n=659 | +0.6 (+0.1), n=112 |
| high volume, 0-1 goals in last 10 (sleeper) | 401 | 34.4 | 33.7 | +0.7 | +0.3 | +1.5 (+0.6), n=312 | -2.1 (-0.4), n=89 |

### PATTERN: 4 straight misses after a pattern that never missed more than 2
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| yes | 99 | 40.4 | 39.4 | +1.0 | +0.2 | +1.5 (+0.3), n=83 | -1.3 (-0.1), n=16 |

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

### shot attempts per game, last 10
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| D: 3-4 | 2709 | 7.6 | 7.7 | -0.0 | -0.1 | -0.1 (-0.1), n=2270 | +0.1 (+0.1), n=439 |
| D: 4-5 | 1655 | 11.7 | 10.7 | +1.0 | +1.3 | +0.9 (+1.1), n=1418 | +1.4 (+0.7), n=237 |
| D: 5+ | 1397 | 16.7 | 14.7 | +2.0 | +2.2 | +3.2 (+3.1), n=1182 | -4.2 (-1.7), n=215 |
| F: 4-5 | 3750 | 25.7 | 25.0 | +0.7 | +1.0 | +0.9 (+1.2), n=3204 | -0.5 (-0.3), n=546 |
| F: 3-4 | 5177 | 21.1 | 20.5 | +0.6 | +1.1 | +0.5 (+0.8), n=4252 | +1.0 (+0.8), n=925 |
| F: under 3 | 9688 | 13.6 | 14.7 | -1.1 | -3.1 | -1.0 (-2.5), n=7818 | -1.6 (-2.0), n=1870 |
| F: 6+ | 1905 | 36.2 | 33.8 | +2.4 | +2.2 | +2.6 (+2.2), n=1593 | +1.2 (+0.4), n=312 |
| F: 5-6 | 2193 | 30.3 | 29.0 | +1.3 | +1.4 | +1.4 (+1.3), n=1855 | +0.9 (+0.3), n=338 |
| D: 2-3 | 3894 | 5.4 | 5.9 | -0.5 | -1.4 | -0.4 (-0.9), n=3197 | -1.1 (-1.2), n=697 |
| D: under 2 | 2144 | 4.0 | 4.6 | -0.5 | -1.2 | -0.6 (-1.3), n=1714 | -0.2 (-0.2), n=430 |

### hit each of last 3
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| no | 34182 | 16.3 | 16.1 | +0.1 | +0.8 | +0.3 (+1.4), n=28218 | -0.5 (-1.1), n=5964 |
| yes | 330 | 27.0 | 31.9 | -4.9 | -2.0 | -6.0 (-2.2), n=285 | +1.6 (+0.2), n=45 |

### recency: last-20 rate minus 60-game baseline
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| L20 near baseline | 14880 | 13.8 | 13.7 | +0.2 | +0.6 | +0.2 (+0.6), n=12497 | +0.0 (+0.0), n=2383 |
| L20 above (+3 to +8) | 6028 | 18.7 | 19.4 | -0.6 | -1.3 | -0.5 (-0.9), n=5041 | -1.4 (-1.2), n=987 |
| L20 well above baseline (+8 or more) | 3475 | 24.6 | 25.0 | -0.4 | -0.6 | -0.4 (-0.5), n=2864 | -0.6 (-0.4), n=611 |
| L20 below (-3 to -8) | 7774 | 14.9 | 14.2 | +0.8 | +2.0 | +0.9 (+2.2), n=6368 | +0.1 (+0.1), n=1406 |
| L20 well below (-8 or less) | 2355 | 19.5 | 19.2 | +0.2 | +0.3 | +1.1 (+1.2), n=1733 | -2.1 (-1.3), n=622 |

### recency: last-10 rate minus 60-game baseline
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| L10 near baseline | 14220 | 14.1 | 13.7 | +0.4 | +1.5 | +0.5 (+1.7), n=11745 | -0.1 (-0.1), n=2475 |
| L10 above (+5 to +15) | 6603 | 18.4 | 18.4 | -0.0 | -0.1 | -0.0 (-0.0), n=5605 | -0.2 (-0.1), n=998 |
| L10 well above baseline (+15 or more) | 2761 | 22.8 | 24.0 | -1.2 | -1.5 | -1.1 (-1.3), n=2302 | -1.7 (-0.9), n=459 |
| L10 below (-5 to -15) | 9381 | 15.3 | 15.3 | +0.0 | +0.1 | +0.3 (+0.9), n=7605 | -1.3 (-1.6), n=1776 |
| L10 well below (-15 or less) | 1547 | 24.1 | 23.5 | +0.6 | +0.5 | +0.4 (+0.3), n=1246 | +1.4 (+0.6), n=301 |

### current hit run (games in a row with a hit)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| 0 | 28870 | 15.2 | 15.0 | +0.3 | +1.3 | +0.4 (+1.7), n=23788 | -0.2 (-0.5), n=5082 |
| 1 | 4383 | 21.3 | 21.7 | -0.3 | -0.6 | -0.1 (-0.2), n=3649 | -1.5 (-1.0), n=734 |
| 2 | 929 | 25.9 | 27.1 | -1.2 | -0.8 | -0.4 (-0.3), n=781 | -5.2 (-1.5), n=148 |
| 3 | 240 | 25.8 | 31.1 | -5.3 | -1.8 | -6.0 (-1.9), n=207 | -1.0 (-0.1), n=33 |
| 4+ | 90 | 30.0 | 34.0 | -4.0 | -0.8 | -6.0 (-1.1), n=78 | +9.0 (+0.7), n=12 |

### all games (baseline check)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| all | 34512 | 16.4 | 16.3 | +0.1 | +0.5 | +0.2 (+1.1), n=28503 | -0.5 (-1.1), n=6009 |

### PATTERN: 3 straight misses after a pattern that never missed more than 2
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| no, had longer miss runs before | 2735 | 17.7 | 18.7 | -1.0 | -1.4 | -1.2 (-1.5), n=2258 | -0.3 (-0.2), n=477 |
| yes | 46 | 47.8 | 35.0 | +12.8 | +1.8 | +11.7 (+1.5), n=38 | +17.9 (+1.1), n=8 |

### USER METHOD: L10 form and same-venue L10 form both at the bar (points 6+, assists 4+, goals 3+)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| both at the bar, hit last game | 2347 | 28.6 | 30.4 | -1.8 | -1.9 | -1.9 (-1.8), n=1983 | -1.4 (-0.6), n=364 |
| both at the bar, missed last game (off night) | 3394 | 27.8 | 29.0 | -1.2 | -1.6 | -1.9 (-2.3), n=2846 | +2.5 (+1.3), n=548 |

### USER METHOD: L10 form at the bar but same-venue L10 below the bar
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| venue form weak | 2987 | 21.8 | 21.6 | +0.1 | +0.2 | +0.7 (+0.9), n=2509 | -2.9 (-1.6), n=478 |

### USER METHOD: L10 below the bar but same-venue L10 at the bar
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| venue form strong only | 3075 | 21.8 | 22.0 | -0.3 | -0.3 | +0.7 (+0.9), n=2488 | -4.4 (-2.6), n=587 |

### PATTERN: 2 misses right after a 2-hit run (MM after HH)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| any history | 679 | 22.2 | 25.0 | -2.8 | -1.7 | -3.1 (-1.8), n=566 | -1.1 (-0.3), n=113 |
| history never missed more than 2 | 27 | 37.0 | 39.6 | -2.5 | -0.3 | -8.1 (-0.8), n=22 | +22.0 (+1.0), n=5 |

### long-history venue edge (all prior same-venue games, 30+ there, vs all prior games)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| venue same (within 4) | 7292 | 15.9 | 15.6 | +0.3 | +0.8 | +0.7 (+1.4), n=4021 | -0.2 (-0.3), n=3271 |
| venue a bit better (+4 to +10) | 1753 | 20.8 | 20.6 | +0.2 | +0.2 | +0.2 (+0.2), n=1014 | +0.2 (+0.2), n=739 |
| venue a bit worse (-4 to -10) | 1748 | 19.0 | 20.9 | -1.9 | -2.0 | -1.2 (-0.9), n=1047 | -2.9 (-1.9), n=701 |
| venue much better (+10 or more) | 137 | 24.8 | 23.6 | +1.2 | +0.3 | +0.7 (+0.2), n=87 | +2.2 (+0.4), n=50 |
| venue much worse (-10 or more) | 135 | 31.9 | 24.0 | +7.8 | +2.2 | +7.4 (+1.7), n=91 | +8.6 (+1.4), n=44 |

### forwards: games with 4+ attempts, last 10
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| 5-6 of 10 | 4411 | 23.5 | 23.1 | +0.4 | +0.6 | +0.5 (+0.8), n=3708 | -0.3 (-0.2), n=703 |
| 0-4 of 10 | 12573 | 15.1 | 16.0 | -0.8 | -2.5 | -0.7 (-2.0), n=10201 | -1.2 (-1.6), n=2372 |
| 9-10 of 10 games with 4+ attempts | 2015 | 33.2 | 32.2 | +1.0 | +1.0 | +1.2 (+1.1), n=1703 | -0.1 (-0.0), n=312 |
| 7-8 of 10 | 3714 | 30.2 | 27.9 | +2.3 | +3.2 | +2.3 (+2.9), n=3110 | +2.4 (+1.3), n=604 |

### forwards: games with 5+ attempts, last 10
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| 0-4 of 10 | 16688 | 17.2 | 17.7 | -0.5 | -1.7 | -0.4 (-1.3), n=13647 | -0.8 (-1.1), n=3041 |
| 5-7 of 10 | 4474 | 29.2 | 27.7 | +1.5 | +2.3 | +1.8 (+2.5), n=3791 | +0.1 (+0.0), n=683 |
| 8-10 of 10 games with 5+ attempts | 1551 | 35.6 | 33.4 | +2.1 | +1.8 | +2.1 (+1.6), n=1284 | +2.4 (+0.8), n=267 |

### mid volume by goals in last 10
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| mid volume, 0-1 goals in last 10 | 1391 | 21.4 | 19.1 | +2.3 | +2.2 | +2.1 (+1.9), n=1191 | +3.4 (+1.2), n=200 |
| mid volume, 2+ goals in last 10 | 4392 | 25.0 | 25.3 | -0.3 | -0.4 | +0.1 (+0.1), n=3716 | -2.2 (-1.3), n=676 |

### alternating (5+ flips in last 8)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| last game hit | 772 | 26.4 | 28.1 | -1.7 | -1.0 | -2.3 (-1.3), n=652 | +1.7 (+0.4), n=120 |
| last game MISS | 1030 | 24.3 | 26.8 | -2.6 | -1.9 | -2.7 (-1.9), n=869 | -1.7 (-0.5), n=161 |

### USER METHOD: both at the bar and 1-2 straight misses (off night or two)
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| yes | 2339 | 28.2 | 29.5 | -1.3 | -1.4 | -1.9 (-1.9), n=1954 | +1.7 (+0.7), n=385 |

### high volume (5+ attempts or 3+ shots a game) by goals in last 10
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| high volume, 3+ goals in last 10 (hot) | 3043 | 34.3 | 33.2 | +1.0 | +1.2 | +1.0 (+1.1), n=2567 | +1.2 (+0.6), n=476 |
| high volume, 2 goals in last 10 | 771 | 29.3 | 26.5 | +2.8 | +1.8 | +4.2 (+2.5), n=659 | -5.8 (-1.4), n=112 |
| high volume, 0-1 goals in last 10 (sleeper) | 401 | 30.4 | 24.1 | +6.3 | +3.0 | +5.4 (+2.3), n=312 | +9.5 (+2.0), n=89 |

### steady players: straight misses right now
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| 2 | 60 | 36.7 | 36.9 | -0.3 | -0.0 | -1.3 (-0.2), n=50 | +5.0 (+0.3), n=10 |
| 1 | 73 | 32.9 | 38.9 | -6.0 | -1.1 | -5.3 (-0.9), n=60 | -9.3 (-0.7), n=13 |
| 0 | 100 | 36.0 | 40.2 | -4.2 | -0.9 | -1.5 (-0.3), n=88 | -24.2 (-1.7), n=12 |

### PATTERN: 4 straight misses after a pattern that never missed more than 2
| bucket | n | actual % | baseline % | diff | z | last season diff (z) | this season diff (z) |
|---|---|---|---|---|---|---|---|
| yes | 32 | 37.5 | 33.7 | +3.8 | +0.5 | -1.8 (-0.2), n=28 | +42.8 (+1.8), n=4 |

