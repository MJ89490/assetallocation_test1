CREATE OR REPLACE FUNCTION select_times_strategy(
  strategy_name varchar,
  strategy_version int,
  OUT description varchar,
  OUT user_id varchar,
  OUT time_lag varchar,
  OUT leverage_type varchar,
  OUT volatility_window int,
  OUT short_signals numeric[],
  OUT long_signals numeric[],
  OUT frequency frequency,
  OUT day_of_week int
)
AS
$$
BEGIN
	SELECT
	  s.description,
	  s.user_id,
	  t.time_lag,
	  t.leverage_type,
	  t.volatility_window,
	  t.short_signals,
	  t.long_signals,
	  t.frequency,
	  t.day_of_week
  INTO
    description,
    user_id,
    time_lag,
    leverage_type,
    volatility_window,
    short_signals,
    long_signals,
    frequency,
    day_of_week
	FROM
	  arp.strategy s
	  JOIN arp.times t
	  ON s.id = t.strategy_id
	WHERE
	  s.name = strategy_name
	  AND t.version = strategy_version;
  return;
END;
$$
LANGUAGE plpgsql;