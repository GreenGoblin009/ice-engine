-- Ice Engine tables. Run once in the Supabase SQL editor
-- (Dashboard -> SQL Editor -> New query -> paste -> Run). Safe to re-run.

create table if not exists public.games (
  id              bigint primary key,          -- NHL gameId
  game_date       date not null,               -- NHL calendar date (US Eastern)
  game_type       smallint,                    -- 1=preseason, 2=regular, 3=playoffs
  away            text not null,
  home            text not null,
  start_time_utc  timestamptz,
  updated_at      timestamptz not null default now()
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
  toi            text,                         -- "MM:SS"
  games_started  smallint,                     -- goalies only, from here down
  decision       text,
  shots_against  smallint,
  goals_against  smallint,
  save_pct       numeric,
  updated_at     timestamptz not null default now(),
  primary key (player_id, game_id)
);

create index if not exists games_game_date_idx on public.games (game_date);
create index if not exists players_team_idx on public.players (team);
create index if not exists player_game_logs_player_date_idx
  on public.player_game_logs (player_id, game_date desc);
create index if not exists player_game_logs_opponent_idx
  on public.player_game_logs (player_id, opponent);

-- Row-level security: the daily job writes with the service key, which
-- bypasses RLS. Everyone else (the Props Board, using the public anon key)
-- can only read.
alter table public.games enable row level security;
alter table public.players enable row level security;
alter table public.player_game_logs enable row level security;

drop policy if exists "public read" on public.games;
create policy "public read" on public.games for select using (true);
drop policy if exists "public read" on public.players;
create policy "public read" on public.players for select using (true);
drop policy if exists "public read" on public.player_game_logs;
create policy "public read" on public.player_game_logs for select using (true);
