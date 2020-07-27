CREATE OR REPLACE FUNCTION insert_times_strategy(
  name varchar,
  description varchar,
  user_id varchar,
  time_lag interval,
  leverage_type char,
  volatitity_window int,
  short_signals numeric[],
  long_signals numeric[],
  frequency frequency,
  day_of_week int,
  OUT version int
)
LANGUAGE SQL
AS
$$
with inserted_es (execution_state_id) as (
select insert_execution_state('insert_times_strategy')
),
inserted_s (strategy_id) AS (
select insert_strategy(name, description, user_id, execution_state_id)
),
INSERT INTO arp.times (
  time_lag,
  leverage_type,
  volatitity_window,
  short_signals,
  long_signals,
  frequency,
  day_of_week,
  execution_state_id,
  strategy_id
)
SELECT
  time_lag,
  leverage_type,
  volatitity_window,
  short_signals,
  long_signals,
  frequency,
  day_of_week,
  inserted_es.execution_state_id,
  inserted_s.strategy_id
FROM
  inserted_s
  CROSS JOIN inserted_es
RETURNING arp.times.version
$$;