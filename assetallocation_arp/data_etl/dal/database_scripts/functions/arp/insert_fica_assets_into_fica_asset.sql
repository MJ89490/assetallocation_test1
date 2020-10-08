CREATE OR REPLACE FUNCTION arp.insert_fica_assets_into_fica_asset(
  strategy_id int,
  execution_state_id int,
  asset_tickers varchar[],
  sovereign_ticker_ids varchar[],
  swap_ticker_ids varchar[],
  swap_cr_ticker_ids varchar[]
)
RETURNS void
AS
$$
BEGIN
  INSERT INTO arp.fica_asset(
    strategy_id,
    execution_state_id,
    asset_id,
    sovereign_ticker_id,
    swap_ticker_id,
    swap_cr_ticker_id
  )
  SELECT
    insert_fica_assets_into_fica_asset.strategy_id,
    insert_fica_assets_into_fica_asset.execution_state_id,
    a.id as asset_id,
    unnest(insert_fica_assets_into_fica_asset.sovereign_ticker_ids),
    unnest(insert_fica_assets_into_fica_asset.swap_ticker_ids),
    unnest(insert_fica_assets_into_fica_asset.swap_cr_ticker_ids)
  FROM
    asset.asset a
  WHERE
    a.ticker = ANY(insert_fica_assets_into_fica_asset.asset_tickers)
;
END;
$$
LANGUAGE plpgsql;