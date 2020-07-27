CREATE OR REPLACE FUNCTION insert_fica_strategy(
  name varchar,
  description varchar,
  user_id varchar,
  tenor int,
  coupon numeric,
  curve varchar,
  trading_cost int,
  business_tstzrange tstzrange,
  strategy_weights numeric[],
  OUT f_version int
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
END
$$;