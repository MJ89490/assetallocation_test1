CREATE OR REPLACE FUNCTION arp.insert_fica_assets_into_fica_asset(
  strategy_id int,
  execution_state_id int,
  asset_tickers varchar[],
  categories varchar[],
  curve_tenors varchar[]
)
RETURNS void
AS
$$
BEGIN
  WITH row_inputs as (
    SELECT
      unnest(insert_fica_assets_into_fica_asset.asset_tickers) as asset_ticker,
      unnest(insert_fica_assets_into_fica_asset.categories) as category,
      unnest(insert_fica_assets_into_fica_asset.curve_tenors) as curve_tenor
  )
  INSERT INTO arp.fica_asset(
    strategy_id,
    execution_state_id,
    asset_id,
    category,
    curve_tenor
  )
  SELECT
    insert_fica_assets_into_fica_asset.strategy_id,
    insert_fica_assets_into_fica_asset.execution_state_id,
    a.id as asset_id,
    ri.category,
    ri.curve_tenor
  FROM
    asset.asset a
    JOIN row_inputs ri on ri.asset_ticker = a.ticker
;
END;
$$
LANGUAGE plpgsql;