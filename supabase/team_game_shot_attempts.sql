-- Shot attempts for and against, per team per game. Run once in the Supabase
-- SQL editor; safe to re-run. Read by backtest_team_totals.py.
--
-- Totals are sums over player_game_logs, which only holds players who are on
-- an NHL roster now. skaters_logged says how many skaters were found for that
-- team in that game (a full lineup is 18), so undercounted games are visible.

create or replace view public.team_game_shot_attempts
with (security_invoker = true) as  -- reads through the tables' own row-level security
with team_for as (
  select game_id, season, game_type, game_date, team, opponent, home_road,
         sum(shot_attempts)                     as attempts_for,
         sum(sog)                               as sog_for,
         count(*) filter (where sog is not null) as skaters_logged  -- goalies have no sog
  from public.player_game_logs
  where shot_attempts is not null
  group by game_id, season, game_type, game_date, team, opponent, home_road
)
select f.game_id, f.season, f.game_type, f.game_date, f.team, f.opponent, f.home_road,
       f.attempts_for,
       a.attempts_for   as attempts_against,
       f.sog_for,
       a.sog_for        as sog_against,
       f.skaters_logged,
       a.skaters_logged as opp_skaters_logged
from team_for f
left join team_for a on a.game_id = f.game_id and a.team = f.opponent;

grant select on public.team_game_shot_attempts to anon, authenticated;
