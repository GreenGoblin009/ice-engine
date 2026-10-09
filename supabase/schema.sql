-- Ice Engine tables. Run in the Supabase SQL editor
-- (Dashboard -> SQL Editor -> New query -> paste -> Run). Safe to re-run:
-- it creates what's missing and upgrades tables made by an older version.

create table if not exists public.games (
  id                bigint primary key,        -- NHL gameId
  season            integer,                   -- e.g. 20262027
  game_date         date not null,             -- NHL calendar date (US Eastern)
  game_type         smallint,                  -- 2=regular, 3=playoffs
  game_state        text,                      -- FUT, LIVE, FINAL, OFF (OFF = official)
  away              text not null,
  home              text not null,
  start_time_utc    timestamptz,
  away_score        smallint,                  -- final score; null until the game is over
  home_score        smallint,
  last_period_type  text,                      -- REG, OT or SO (SO winner's score includes +1)
  updated_at        timestamptz not null default now()
);

create table if not exists public.players (
  id          bigint primary key,              -- NHL playerId
  name        text not null,
  team        text not null,                   -- current team abbreviation
  number      smallint,
  pos         text,                            -- C, L, R, D, G
  updated_at  timestamptz not null default now()
);

create table if not exists public.player_game_logs (
  player_id      bigint not null references public.players (id),
  game_id        bigint not null,
  season         integer not null,             -- e.g. 20262027
  game_type      smallint not null,
  game_date      date not null,
  team           text,                         -- team the player was on for this game
  opponent       text,
  home_road      text,                         -- H or R
  goals          smallint,
  assists        smallint,
  points         smallint,
  sog            smallint,                     -- skaters only
  shot_attempts  smallint,                     -- sog + missed + blocked; null until counted
  toi            text,                         -- "MM:SS"
  games_started  smallint,                     -- goalies only, from here down
  decision       text,
  shots_against  smallint,
  goals_against  smallint,
  save_pct       numeric,
  updated_at     timestamptz not null default now(),
  primary key (player_id, game_id)
);

-- Projected lineups scraped from NHL.com each afternoon (ice_engine_lineups.py).
-- One row per player named for a team that day, in the article's order.
create table if not exists public.daily_lineups (
  lineup_date        date not null,            -- NHL calendar date (US Eastern)
  team               text not null,
  list_order         smallint not null,        -- position in the team's list, 1 = first forward
  game_id            bigint,
  opponent           text,
  player_name        text not null,            -- as written in the article
  player_id          bigint references public.players (id),  -- null if no match by team + name
  slot               text check (slot in ('line', 'pair', 'goalie')),  -- null unless projected
  slot_number        smallint,                 -- line 1-4, pair 1-4, goalie 1 (listed first) or 2
  status             text not null check (status in ('projected', 'scratched', 'injured', 'suspended')),
  confirmed_starter  boolean not null default false,  -- status report says this goalie starts
  detail             text,                     -- injury, or the sentence naming the starter
  updated_at         timestamptz not null default now(),
  primary key (lineup_date, team, list_order)
);

-- Upgrade tables created before final scores and shot attempts were added.
alter table public.games add column if not exists season integer;
alter table public.games add column if not exists game_state text;
alter table public.games add column if not exists away_score smallint;
alter table public.games add column if not exists home_score smallint;
alter table public.games add column if not exists last_period_type text;
alter table public.player_game_logs add column if not exists shot_attempts smallint;

create index if not exists games_game_date_idx on public.games (game_date);
create index if not exists players_team_idx on public.players (team);
create index if not exists player_game_logs_player_date_idx
  on public.player_game_logs (player_id, game_date desc);
create index if not exists player_game_logs_opponent_idx
  on public.player_game_logs (player_id, opponent);
-- The daily job asks "which rows still need shot attempts?" on every run.
create index if not exists player_game_logs_missing_attempts_idx
  on public.player_game_logs (season) where shot_attempts is null;

create index if not exists daily_lineups_player_idx
  on public.daily_lineups (player_id, lineup_date desc);
create index if not exists daily_lineups_game_idx on public.daily_lineups (game_id);

-- Row-level security: the daily job writes with the service key, which
-- bypasses RLS. Everyone else (the Props Board, using the public anon key)
-- can only read.
alter table public.games enable row level security;
alter table public.players enable row level security;
alter table public.player_game_logs enable row level security;
alter table public.daily_lineups enable row level security;

drop policy if exists "public read" on public.games;
create policy "public read" on public.games for select using (true);
drop policy if exists "public read" on public.players;
create policy "public read" on public.players for select using (true);
drop policy if exists "public read" on public.player_game_logs;
create policy "public read" on public.player_game_logs for select using (true);
drop policy if exists "public read" on public.daily_lineups;
create policy "public read" on public.daily_lineups for select using (true);
