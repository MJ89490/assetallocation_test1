DROP FUNCTION IF EXISTS arp.select_times_strategy(integer);
CREATE OR REPLACE FUNCTION arp.select_times_strategy(
  strategy_version int,
  OUT business_date_from date,
  OUT description varchar,
  OUT time_lag varchar,
  OUT leverage_type varchar,
  OUT volatility_window int,
  OUT short_signals numeric[],
  OUT long_signals numeric[],
  OUT frequency arp.frequency,
  OUT day_of_week int
)
AS
$$
BEGIN
	SELECT
    s.business_date_from,
	  s.description,
	  t.time_lag,
	  t.leverage_type,
	  t.volatility_window,
	  t.short_signals,
	  t.long_signals,
	  t.frequency,
	  t.day_of_week
  INTO
    business_date_from,
    description,
    time_lag,
    leverage_type,
    volatility_window,
    short_signals,
    long_signals,
    frequency,
    day_of_week
	FROM
	  arp.strategy s
	  JOIN arp.times t ON s.id = t.strategy_id
	WHERE
	  t.version = strategy_version;
  return;
END;
$$
LANGUAGE plpgsql;