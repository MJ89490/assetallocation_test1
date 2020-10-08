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