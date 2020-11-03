CREATE OR REPLACE FUNCTION arp.insert_times_strategy(
  description varchar,
  user_id varchar,
  time_lag interval,
  leverage_type char,
  volatility_window int,
  short_signals numeric[],
  long_signals numeric[],
  frequency frequency,
  day_of_week int,
  OUT t_version int
)
LANGUAGE plpgsql
AS
$$
declare
  name varchar;
	execution_state_id int;
	strategy_id int;
BEGIN
  name := 'times';
	SELECT config.insert_execution_state('arp.insert_times_strategy') into execution_state_id;
  PERFORM arp.close_off_strategy(name);
	SELECT arp.insert_strategy(name, description, user_id, execution_state_id) into strategy_id;
	SELECT arp.insert_times(time_lag, leverage_type, volatility_window, short_signals, long_signals, frequency, day_of_week,
	  execution_state_id, strategy_id) into t_version;
	return;
END
$$;

CREATE OR REPLACE FUNCTION arp.insert_times(
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
