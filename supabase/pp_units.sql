-- Power-play units. Paste into the Supabase SQL editor and run once
-- (safe to run again).

-- Seconds of power-play ice time in that game, from the NHL stats API's
-- skater "timeonice" report. Null = not filled yet (or a goalie).
alter table public.player_game_logs add column if not exists pp_toi integer;

-- 1 = first power-play unit, 2 = second; null = neither, or not known.
-- Worked out by ice_engine_lineups.py from recent pp_toi, not from the article.
alter table public.daily_lineups add column if not exists pp_unit smallint
  check (pp_unit in (1, 2));

-- The daily job asks "which regular-season rows still need pp_toi?" on every run.
create index if not exists player_game_logs_missing_pp_toi_idx
  on public.player_game_logs (season) where pp_toi is null;
