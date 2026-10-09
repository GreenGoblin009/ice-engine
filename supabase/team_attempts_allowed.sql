-- What each team allows per game, per regular season: shot attempts and
-- goals. One row per team per season (32 x 2), so the website can read it in
-- a single small request. Run once in the Supabase SQL editor; safe to re-run.
--
-- attempts_allowed_per_game: the opponent's skaters' shot attempts, per game.
--   player_game_logs only has players on an NHL roster now, so each game is
--   scaled up to a full 18 skaters (x 18 / skaters found), the same way
--   backtest_player_props_v2.py does it. Games with fewer than 10 of the
--   opponent's skaters on file are left out of the average.
-- goals_allowed_per_game: from final scores, without the extra goal the NHL
--   credits to a shootout winner.

create or replace view public.team_attempts_allowed
with (security_invoker = true) as  -- reads through the tables' own row-level security
with per_game as (
  -- attempts by one team's skaters in a game = attempts their opponent allowed
  select season, game_id, opponent as team,
         sum(shot_attempts) * 18.0 / count(*) filter (where sog is not null) as attempts_allowed
  from public.player_game_logs
  where game_type = 2 and season in (20252026, 20262027) and shot_attempts is not null
  group by season, game_id, opponent
  having count(*) filter (where sog is not null) >= 10
),
attempts as (
  select season, team, avg(attempts_allowed) as attempts_allowed_per_game
  from per_game
  group by season, team
),
finals as (
  select season, home as team,
         away_score - (case when last_period_type = 'SO' and away_score > home_score then 1 else 0 end) as goals_allowed
  from public.games
  where game_type = 2 and season in (20252026, 20262027)
    and home_score is not null and away_score is not null and game_state in ('OFF', 'FINAL')
  union all
  select season, away as team,
         home_score - (case when last_period_type = 'SO' and home_score > away_score then 1 else 0 end) as goals_allowed
  from public.games
  where game_type = 2 and season in (20252026, 20262027)
    and home_score is not null and away_score is not null and game_state in ('OFF', 'FINAL')
),
goals as (
  select season, team, count(*) as games, avg(goals_allowed) as goals_allowed_per_game
  from finals
  group by season, team
)
select g.season,
       g.team,
       g.games,
       round(a.attempts_allowed_per_game, 2) as attempts_allowed_per_game,
       round(g.goals_allowed_per_game, 3)    as goals_allowed_per_game
from goals g
left join attempts a on a.season = g.season and a.team = g.team;

grant select on public.team_attempts_allowed to anon, authenticated;
