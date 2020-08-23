CREATE OR REPLACE FUNCTION arp.insert_times_assets_into_times_asset(
  strategy_id int,
  execution_state_id int,
  times_assets arp.ticker_ticker_cost_leverage[]
)
RETURNS void
AS
$$
BEGIN
  INSERT INTO arp.times_asset(
    strategy_id,
    signal_asset_id,
    future_asset_id,
    s_leverage,
    cost,
    execution_state_id
  )
  SELECT
    strategy_id,
    a1.id,
    a2.id,
    (ta).s_leverage,
    (ta).cost,
    insert_times_assets_into_times_asset.execution_state_id
  FROM
    unnest(times_assets) as ta
    JOIN asset.asset a1 ON (ta).signal_ticker = a1.ticker
    JOIN asset.asset a2 ON (ta).future_ticker = a2.ticker
;
END;
$$
LANGUAGE plpgsql;