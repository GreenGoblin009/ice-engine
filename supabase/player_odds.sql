-- Player-prop prices from The Odds API (ice_engine_odds.py). Run once in the
-- Supabase SQL editor; safe to re-run. One row per price: a player, a market,
-- a line, a side and a bookmaker on a given NHL date.

create table if not exists public.player_odds (
  game_date    date not null,                  -- NHL calendar date (US Eastern)
  event_id     text not null,                  -- The Odds API's id for the game
  home         text not null,                  -- team abbreviations, as in the other tables
  away         text not null,
  player_name  text not null,                  -- as the bookmaker feed spells it
  player_id    bigint references public.players (id),  -- null if no match by name + team
  market       text not null,                  -- e.g. player_points, player_assists
  line         numeric not null,               -- 0.5, 1.5, ...; 0.5 for yes/no markets
  side         text not null,                  -- Over, Under (or Yes)
  book         text not null,                  -- bookmaker, e.g. DraftKings
  price        integer not null,               -- American odds, e.g. -180 or +225
  updated_at   timestamptz not null default now(),
  primary key (game_date, player_name, market, line, side, book)
);

create index if not exists player_odds_player_idx on public.player_odds (player_id, game_date desc);
create index if not exists player_odds_event_idx on public.player_odds (event_id);

-- The job writes with the service key, which bypasses row-level security.
-- Everyone else (the Props Board, using the public key) can only read.
alter table public.player_odds enable row level security;
drop policy if exists "public read" on public.player_odds;
create policy "public read" on public.player_odds for select using (true);
