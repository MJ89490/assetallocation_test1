CREATE OR REPLACE FUNCTION arp.insert_fx_strategy(
  business_date_from date,
  description varchar,
  user_id varchar,
  model varchar,
  signal varchar,
  currency varchar,
  response_function  boolean,
  exposure numeric,
  momentum_weights numeric[],
  transaction_cost numeric,
  top_crosses integer,
  vol_window integer,
  value_window integer,
  sharpe_cutoff integer,
  mean_reversion integer,
  historical_base integer,
  defensive boolean,
  OUT f_version int
)
LANGUAGE plpgsql
AS
$$
declare
  name varchar;
	execution_state_id int;
	strategy_id int;
BEGIN
  name := 'fx';
	SELECT config.insert_execution_state('arp.insert_fx_strategy') into execution_state_id;
  PERFORM arp.close_off_strategy(name);
	SELECT arp.insert_strategy(name, business_date_from, description, user_id, execution_state_id) into strategy_id;
	SELECT arp.insert_fx(
    model,
    signal,
    currency,
    response_function ,
    exposure,
    momentum_weights,
    transaction_cost,
    top_crosses,
    vol_window,
    value_window,
    sharpe_cutoff,
    mean_reversion,
    historical_base,
    defensive,
    execution_state_id,
    strategy_id
  ) into f_version;
	return;
END
$$;

CREATE OR REPLACE FUNCTION arp.insert_fx(
  model varchar,
  signal varchar,
  currency varchar,
  response_function  boolean,
  exposure numeric,
  momentum_weights numeric[],
  transaction_cost numeric,
  top_crosses integer,
  vol_window integer,
  value_window integer,
  sharpe_cutoff integer,
  mean_reversion integer,
  historical_base integer,
  defensive boolean,
  strategy_id int,
  execution_state_id int,
  OUT f_version int
)
AS
$$
BEGIN
	INSERT INTO arp.fx (
	  model,
    signal,
    currency,
    response_function ,
    exposure,
    momentum_weights,
    transaction_cost,
    top_crosses,
    vol_window,
    value_window,
    sharpe_cutoff,
    mean_reversion,
    historical_base,
    defensive,
	  execution_state_id,
	  strategy_id
	)
	VALUES(
	  model,
    signal,
    currency,
    response_function ,
    exposure,
    momentum_weights,
    transaction_cost,
    top_crosses,
    vol_window,
    value_window,
    sharpe_cutoff,
    mean_reversion,
    historical_base,
    defensive,
	  execution_state_id,
	  strategy_id
	)
	RETURNING arp.fx.version into f_version;
	return;
END;
$$
LANGUAGE plpgsql;
