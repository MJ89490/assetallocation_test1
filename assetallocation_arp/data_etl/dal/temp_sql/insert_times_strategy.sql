CREATE OR REPLACE FUNCTION insert_times_strategy(
  name varchar,
  description varchar,
  user_id varchar,
  time_lag interval,
  leverage_type char,
  volatility_window int,
  short_signals numeric[],
  long_signals numeric[],
  frequency frequency,
  day_of_week int,
  asset_tickers varchar[],
  OUT t_version int
)
LANGUAGE plpgsql
AS
$$
declare
	execution_state_id int;
	strategy_id int;
BEGIN
	SELECT insert_execution_state('insert_times_strategy') into execution_state_id;
	SELECT insert_strategy(name, description, user_id, execution_state_id) into strategy_id;
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
  WITH a (asset_id) as (select id from asset.asset where ticker = ANY(asset_tickers))
  INSERT INTO arp.times_asset (strategy_id, asset_id, execution_state_id)
  SELECT strategy_id, a.asset_id, execution_state_id
  FROM a;
	return;
END
$$;