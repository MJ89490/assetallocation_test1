CREATE OR REPLACE FUNCTION arp.select_fica_strategy(
  strategy_version int,
  OUT description varchar,
  OUT coupon numeric,
  OUT curve varchar,
  OUT business_tstzrange tstzrange,
  OUT strategy_weights numeric[],
  OUT tenor int,
  OUT trading_cost int
)
AS
$$
DECLARE
  strategy_name varchar;
BEGIN
  strategy_name := 'fica';
  
	SELECT
	  s.description,
	  f.coupon,
	  f.curve,
	  f.business_tstzrange,
	  f.strategy_weights,
	  f.tenor,
	  f.trading_cost
  INTO
    description,
    coupon,
    curve,
    business_tstzrange,
    strategy_weights,
    tenor,
    trading_cost
	FROM
	  arp.strategy s
	  JOIN arp.fica f
	  ON s.id = f.strategy_id
	WHERE
	  s.name = strategy_name
	  AND f.version = strategy_version;
  return;
END;
$$
LANGUAGE plpgsql;