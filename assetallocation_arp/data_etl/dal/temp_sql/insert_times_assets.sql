CREATE OR REPLACE FUNCTION insert_times_asset(
  strategy_id int,
  asset_tickers varchar[],
  execution_state_id int
)
RETURNS void
AS
$$
BEGIN
  WITH a (asset_id) as (select id from asset.asset where ticker = ANY(asset_tickers))
  INSERT INTO arp.times_asset (strategy_id, asset_id, execution_state_id)
  SELECT strategy_id, a.asset_id, execution_state_id
  FROM a;
END;
$$
LANGUAGE plpgsql;