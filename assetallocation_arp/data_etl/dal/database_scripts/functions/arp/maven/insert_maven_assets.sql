CREATE OR REPLACE FUNCTION arp.insert_maven_assets(
  maven_version int,
  maven_assets text[]
)
RETURNS VOID
AS
$$
DECLARE
  execution_state_id int;
  strategy_name varchar := 'maven';
  strategy_id int;
  _maven_assets arp.ticker_ticker_ticker_currency_excess_weight_cost[];
BEGIN
  _maven_assets := maven_assets::arp.ticker_ticker_ticker_currency_excess_weight_cost[];

  SELECT config.insert_execution_state('arp.insert_maven_assets') INTO execution_state_id;
  SELECT arp.select_strategy_id(strategy_name, maven_version) INTO strategy_id;
  PERFORM arp.insert_maven_asset_groups(strategy_id, execution_state_id, _maven_assets);
END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION arp.insert_maven_asset_groups(
	strategy_id int,
  execution_state_id int,
  maven_assets arp.ticker_ticker_ticker_currency_excess_weight_cost[]
)
  RETURNS VOID
language plpgsql
as
$$
DECLARE
  _len_maven_assets int;
  _counter int := 1;
BEGIN
  _len_maven_assets = array_length(maven_assets, 1);

  loop
    exit when _counter > _len_maven_assets;
    PERFORM arp.insert_maven_asset_group(strategy_id, insert_maven_asset_groups.execution_state_id, maven_assets[_counter]);
    _counter := _counter + 1;
  end loop;
END
$$;


CREATE OR REPLACE FUNCTION arp.insert_maven_asset_group(
	strategy_id int,
  execution_state_id int,
  maven_asset arp.ticker_ticker_ticker_currency_excess_weight_cost
)
  RETURNS VOID
language plpgsql
as
$$
DECLARE
  strategy_asset_group_id int;
BEGIN
  SELECT arp.insert_strategy_asset_group(strategy_id, insert_maven_asset_group.execution_state_id) INTO strategy_asset_group_id;
  PERFORM arp.insert_maven_asset_group(
      strategy_asset_group_id,
      insert_maven_asset_group.execution_state_id,
      maven_asset.currency,
      maven_asset.is_excess,
      maven_asset.asset_weight,
      maven_asset.transaction_cost
  );
  PERFORM arp.insert_strategy_asset(strategy_asset_group_id, insert_maven_asset_group.execution_state_id, 'bbg_tr', maven_asset.bbg_tr_ticker);
  PERFORM arp.insert_strategy_asset(strategy_asset_group_id, insert_maven_asset_group.execution_state_id, 'bbg_er', maven_asset.bbg_er_ticker);
  PERFORM arp.insert_strategy_asset(strategy_asset_group_id, insert_maven_asset_group.execution_state_id, 'cash', maven_asset.cash_ticker);
END
$$;


CREATE OR REPLACE FUNCTION arp.insert_maven_asset_group(
  strategy_asset_group_id int,
	execution_state_id int,
  currency text,
  is_excess boolean,
  asset_weight numeric(32,16),
  transaction_cost numeric(32,16)
)
  RETURNS VOID
language plpgsql
as
$$
BEGIN
  INSERT INTO arp.maven_asset_group (
    strategy_asset_group_id,
    execution_state_id,
    currency_id,
    is_excess,
    asset_weight,
    transaction_cost
  )
  SELECT
    strategy_asset_group_id,
    insert_maven_asset_group.execution_state_id,
    c.id,
    is_excess,
    asset_weight,
    transaction_cost
  FROM
    lookup.currency c
  WHERE
    c.currency = insert_maven_asset_group.currency
  ;
  return;
END
$$
