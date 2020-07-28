CREATE OR REPLACE FUNCTION insert_times(
  time_lag interval,
  leverage_type char,
  volatility_window int,
  short_signals numeric[],
  long_signals numeric[],
  frequency frequency,
  day_of_week int,
  execution_state_id int,
  strategy_id int,
  OUT t_version int
)
AS
$$
BEGIN
	INSERT INTO arp.times (
	  time_lag,
	  leverage_type,
	  volatility_window,
	  short_signals,
	  long_signals,
	  frequency,
	  day_of_week,
	  execution_state_id,
	  strategy_id
	)
	VALUES(
	  time_lag,
	  leverage_type,
	  volatility_window,
	  short_signals,
	  long_signals,
	  frequency,
	  day_of_week,
	  execution_state_id,
	  strategy_id
	)
	RETURNING arp.times.version into t_version;
	return;
END;
$$
LANGUAGE plpgsql;