CREATE OR REPLACE FUNCTION arp.insert_maven_assets(
  maven_version int,
  maven_assets text[]
)
RETURNS VOID
AS
$$
DECLARE
  execution_state_id int;
  strategy_name varchar;
  strategy_id int;
  _maven_assets arp.ticker_ticker_ticker_category_subcategory_currency_excess_weight_cost[];
BEGIN
  strategy_name := 'maven';
  _maven_assets := maven_assets::arp.ticker_ticker_ticker_category_subcategory_currency_excess_weight_cost[];

  SELECT config.insert_execution_state('arp.insert_maven_assets') INTO execution_state_id;
  SELECT arp.select_strategy_id(strategy_name, maven_version) INTO strategy_id;
  PERFORM arp.delete_maven_assets_from_maven_asset(strategy_id);
  PERFORM arp.insert_maven_assets_into_maven_asset(strategy_id, execution_state_id, _maven_assets);
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION arp.delete_maven_assets_from_maven_asset(
  strategy_id int
)
  RETURNS VOID
AS
$$
BEGIN
  DELETE FROM arp.maven_asset ta WHERE ta.strategy_id = delete_maven_assets_from_maven_asset.strategy_id;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION arp.insert_maven_assets_into_maven_asset(
  strategy_id int,
  execution_state_id int,
  maven_assets arp.asset_ticker_ticker_cost_leverage[]
)
RETURNS void
AS
$$
BEGIN
  INSERT INTO arp.maven_asset(
    strategy_id,
    bbg_tr_asset_id,
    bbg_er_asset_id,
    cash_asset_id,
    asset_category,
    asset_subcategory,
    currency,
    is_excess,
    asset_weight,
    transaction_cost,
    execution_state_id
  )
  SELECT
    strategy_id,
    a1.id,
    a2.id,
    a3.id,
    (ma).asset_category,
    (ma).asset_subcategory,
    (ma).currency,
    (ma).is_excess,
    (ma).asset_weight,
    (ma).transaction_cost,
    insert_maven_assets_into_maven_asset.execution_state_id
  FROM
    unnest(maven_assets) as ma
    JOIN asset.asset a1 ON (ma).bbg_tr_ticker = a1.ticker
    JOIN asset.asset a2 ON (ma).bbg_er_ticker = a2.ticker
    JOIN asset.asset a3 ON (ma).cash_ticker = a3.ticker
;
END;
$$
LANGUAGE plpgsql;
