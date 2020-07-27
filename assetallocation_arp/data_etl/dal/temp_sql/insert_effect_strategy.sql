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
with iese as (
	select id
	from config.execution e
	where e.name = 'insert_effect_strategy'
	and in_use = 't'
)
,
inserted_es as (
insert into config.execution_state (system_datetime, execution_id)
select
	now(),
	iese.id
from
	iese
RETURNING execution_state.id
),
inserted_s (strategy_id, execution_state_id) AS (
INSERT INTO arp.strategy (name, description, user_id, execution_state_id)
SELECT
  name,
  description,
  user_id,
  inserted_es.id
FROM
  inserted_es
RETURNING arp.strategy.id, arp.strategy.execution_state_id
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
  inserted_s.execution_state_id
FROM
  inserted_s
RETURNING arp.effect.version
$$;