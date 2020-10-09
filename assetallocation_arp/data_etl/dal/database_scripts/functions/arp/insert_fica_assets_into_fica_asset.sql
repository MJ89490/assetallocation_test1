CREATE OR REPLACE FUNCTION arp.insert_fica_assets_into_fica_asset(
  strategy_id int,
  execution_state_id int,
  asset_tickers varchar[],
  sovereign_ticker_ids int[],
  swap_ticker_ids int[],
  swap_cr_ticker_ids int[]
)
RETURNS void
AS
$$
BEGIN
  WITH row_inputs as (
    SELECT
      unnest(insert_fica_assets_into_fica_asset.asset_tickers) as asset_ticker,
      unnest(insert_fica_assets_into_fica_asset.sovereign_ticker_ids) as sovereign_ticker_id,
      unnest(insert_fica_assets_into_fica_asset.swap_ticker_ids) as swap_ticker_id,
      unnest(insert_fica_assets_into_fica_asset.swap_cr_ticker_ids) as swap_cr_ticker_id
  )
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
    ri.sovereign_ticker_id,
    ri.swap_ticker_id,
    ri.swap_cr_ticker_id
  FROM
    asset.asset a
    JOIN row_inputs ri on ri.asset_ticker = a.ticker
;
END;
$$
LANGUAGE plpgsql;