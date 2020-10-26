CREATE OR REPLACE FUNCTION arp.insert_fica_assets(
  fica_version int,
  asset_tickers varchar[],
  categories varchar[] ,
  curve_tenors varchar[]
)
RETURNS VOID
AS
$$
DECLARE
  execution_state_id int;
  strategy_name varchar;
  strategy_id int;
  fica_asset_group_id int;
BEGIN
  strategy_name := 'fica';

  SELECT config.insert_execution_state('arp.insert_fica_assets') INTO execution_state_id;
  SELECT arp.select_strategy_id(strategy_name, fica_version) INTO strategy_id;
  SELECT arp.insert_fica_asset_group(strategy_id, execution_state_id) INTO fica_asset_group_id;
  PERFORM arp.insert_fica_assets_into_fica_asset(execution_state_id, fica_asset_group_id, asset_tickers,
    categories, curve_tenors);
END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION arp.insert_fica_asset_group(
  strategy_id int,
  execution_state_id int,
  OUT fica_asset_group_id integer
)
AS
$$
BEGIN
  INSERT INTO arp.fica_asset_group(strategy_id, execution_state_id)
  VALUES (strategy_id, execution_state_id)
  RETURNING arp.fica_asset_group.id INTO fica_asset_group_id;
END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION arp.insert_fica_assets_into_fica_asset(
  execution_state_id int,
  fica_asset_group_id int,
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
    execution_state_id,
    fica_asset_group_id,
    asset_id,
    category,
    curve_tenor
  )
  SELECT
    insert_fica_assets_into_fica_asset.execution_state_id,
    insert_fica_assets_into_fica_asset.fica_asset_group_id,
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