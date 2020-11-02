CREATE OR REPLACE FUNCTION arp.insert_fica_strategy(
  description varchar,
  user_id varchar,
  coupon numeric,
  curve varchar,
  business_tstzrange tstzrange,
  strategy_weights numeric[],
  tenor int,
  trading_cost int,
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
  name := 'fica';
	SELECT config.insert_execution_state('insert_times_strategy') into execution_state_id;
  PERFORM arp.close_off_strategy(name);
	SELECT arp.insert_strategy(name, description, user_id, execution_state_id) into strategy_id;
  SELECT arp.insert_fica(coupon, curve, business_tstzrange, strategy_weights, tenor, trading_cost, execution_state_id,
                         strategy_id) into f_version;
	return;
END
$$;

CREATE OR REPLACE FUNCTION arp.insert_fica(
  coupon numeric,
  curve varchar,
  business_tstzrange tstzrange,
  strategy_weights numeric[],
  tenor int,
  trading_cost int,
  execution_state_id int,
  strategy_id int,
  OUT f_version int
)
AS
$$
BEGIN
	INSERT INTO arp.fica (
	  strategy_id,
    tenor,
    coupon,
    curve,
    trading_cost,
    business_tstzrange,
    strategy_weights,
    execution_state_id
  )
  VALUES(
    strategy_id,
    tenor,
    coupon,
    curve,
    trading_cost,
    business_tstzrange,
    strategy_weights,
    execution_state_id
    )
	RETURNING arp.fica.version into f_version;
	return;
END;
$$
LANGUAGE plpgsql;
