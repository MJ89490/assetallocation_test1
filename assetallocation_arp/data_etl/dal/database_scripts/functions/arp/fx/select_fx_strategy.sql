CREATE OR REPLACE FUNCTION arp.select_fx_strategy(
  strategy_version int,
  OUT description varchar(25),
  OUT model varchar(25),
	OUT business_tstzrange tstzrange,
	OUT signal varchar(25),
  OUT currency varchar(25),
	OUT response_function  boolean,
	OUT exposure numeric(32,16),
	OUT momentum_weights numeric(32,16)[],
	OUT transaction_cost numeric(32,16),
	OUT top_crosses integer,
	OUT vol_window integer,
	OUT value_window integer,
	OUT sharpe_cutoff integer,
	OUT mean_reversion integer,
	OUT historical_base integer,
	OUT defensive boolean
)
AS
$$
BEGIN
	SELECT
	  s.description,
	  f.model,
	  f.business_tstzrange,
	  f.signal,
	  f.currency,
	  f.response_function,
	  f.exposure,
	  f.momentum_weights,
    f.transaction_cost,
    f.top_crosses,
    f.vol_window,
    f.value_window,
    f.sharpe_cutoff,
    f.mean_reversion,
    f.historical_base,
		f.defensive
  INTO
    description,
	  model,
	  business_tstzrange,
	  signal,
	  currency,
	  response_function,
	  exposure,
	  momentum_weights,
    transaction_cost,
    top_crosses,
    vol_window,
    value_window,
    sharpe_cutoff,
    mean_reversion,
    historical_base,
		defensive
	FROM
	  arp.strategy s
	  JOIN arp.fx f
	  ON s.id = f.strategy_id
	WHERE
	  f.version = strategy_version;
  return;
END;
$$
LANGUAGE plpgsql;