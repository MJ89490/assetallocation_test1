CREATE OR REPLACE FUNCTION insert_effect_strategy(
  name varchar,
  description varchar,
  user_id varchar,
  carry_type varchar,
  closing_threshold numeric,
  cost numeric,
  day_of_week int,
  frequency frequency,
  include_shorts_flag boolean,
  inflation_lag interval,
  interest_rate_cut_off_long numeric,
  interest_rate_cut_off_short numeric,
  moving_average_long_term int,
  moving_average_short_term int,
  realtime_inflation_forecast_flag boolean,
  trend_indicator varchar,
  OUT version int
)
LANGUAGE SQL
AS
$$
with inserted_es (execution_state_id) as (
select insert_execution_state('insert_effect_strategy')
),
inserted_s (strategy_id) AS (
select insert_strategy(name, description, user_id, execution_state_id)
)
INSERT INTO arp.effect (
  strategy_id,
  carry_type,
  closing_threshold,
  cost,
  day_of_week,
  frequency,
  include_shorts_flag,
  inflation_lag,
  interest_rate_cut_off_long,
  interest_rate_cut_off_short,
  moving_average_long_term,
  moving_average_short_term,
  realtime_inflation_forecast_flag,
  trend_indicator,
  execution_state_id
)
SELECT
  inserted_s.strategy_id,
  carry_type,
  closing_threshold,
  cost,
  day_of_week,
  frequency,
  include_shorts_flag,
  inflation_lag,
  interest_rate_cut_off_long,
  interest_rate_cut_off_short,
  moving_average_long_term,
  moving_average_short_term,
  realtime_inflation_forecast_flag,
  trend_indicator,
  inserted_es.execution_state_id
FROM
  inserted_s
  CROSS JOIN inserted_es
RETURNING arp.effect.version
$$;