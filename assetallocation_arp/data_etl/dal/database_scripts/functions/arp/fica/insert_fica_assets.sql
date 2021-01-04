CREATE OR REPLACE FUNCTION arp.insert_fica_assets(
  fica_version int,
  asset_tickers varchar[],
  names varchar[]
)
RETURNS VOID
AS
$$
DECLARE
  execution_state_id int;
  strategy_name varchar := 'fica';
  strategy_id int;
  strategy_asset_group_id int;
BEGIN
  SELECT config.insert_execution_state('arp.insert_fica_assets') INTO execution_state_id;
  SELECT arp.select_strategy_id(strategy_name, fica_version) INTO strategy_id;
  SELECT arp.insert_strategy_asset_group(strategy_id, insert_fica_assets.execution_state_id) INTO strategy_asset_group_id;
  PERFORM arp.insert_fica_assets_into_strategy_asset(execution_state_id, strategy_asset_group_id, asset_tickers, names);
END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION arp.insert_fica_assets_into_strategy_asset(
  execution_state_id int,
  strategy_asset_group_id int,
  asset_tickers varchar[],
  names varchar[]
)
RETURNS void
AS
$$
BEGIN
  WITH row_inputs as (
    SELECT
      unnest(insert_fica_assets_into_strategy_asset.asset_tickers) as asset_ticker,
      unnest(insert_fica_assets_into_strategy_asset.names) as name
  )
  INSERT INTO arp.strategy_asset(
    execution_state_id,
    strategy_asset_group_id,
    asset_id,
    name
  )
  SELECT
    insert_fica_assets_into_strategy_asset.execution_state_id,
    insert_fica_assets_into_strategy_asset.strategy_asset_group_id,
    a.id as asset_id,
    ri.name
  FROM
    asset.asset a
    JOIN row_inputs ri on ri.asset_ticker = a.ticker
;
END;
$$
LANGUAGE plpgsql;