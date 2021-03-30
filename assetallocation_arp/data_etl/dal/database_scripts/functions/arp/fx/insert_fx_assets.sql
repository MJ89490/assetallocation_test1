CREATE OR REPLACE FUNCTION arp.insert_fx_assets(
  fx_version int,
  fx_assets text[]
)
RETURNS VOID
AS
$$
DECLARE
  execution_state_id int;
  strategy_name varchar := 'fx';
  strategy_id int;
  _fx_assets arp.ticker_ticker_currency[];
BEGIN
  _fx_assets := fx_assets::arp.ticker_ticker_currency[];

  SELECT config.insert_execution_state('arp.insert_fx_assets') INTO execution_state_id;
  SELECT arp.select_strategy_id(strategy_name, fx_version) INTO strategy_id;
  PERFORM arp.insert_fx_asset_groups(strategy_id, execution_state_id, _fx_assets);
END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION arp.insert_fx_asset_groups(
	strategy_id int,
  execution_state_id int,
  fx_assets arp.ticker_ticker_currency[]
)
  RETURNS VOID
language plpgsql
as
$$
DECLARE
  _len_fx_assets int;
  _counter int := 1;
BEGIN
  _len_fx_assets = array_length(fx_assets, 1);

  loop
    exit when _counter > _len_fx_assets;
    PERFORM arp.insert_fx_asset_group(strategy_id, insert_fx_asset_groups.execution_state_id, fx_assets[_counter]);
    _counter := _counter + 1;
  end loop;
END
$$;


CREATE OR REPLACE FUNCTION arp.insert_fx_asset_group(
	strategy_id int,
  execution_state_id int,
  fx_asset arp.ticker_ticker_currency
)
  RETURNS VOID
language plpgsql
as
$$
DECLARE
  strategy_asset_group_id int;
BEGIN
  SELECT arp.insert_strategy_asset_group(strategy_id, insert_fx_asset_group.execution_state_id) INTO strategy_asset_group_id;
  PERFORM arp.insert_fx_asset_group(
      strategy_asset_group_id,
      insert_fx_asset_group.execution_state_id,
      fx_asset.currency
  );
  PERFORM arp.insert_strategy_asset(strategy_asset_group_id, insert_fx_asset_group.execution_state_id, 'ppp', fx_asset.ppp_ticker);
  PERFORM arp.insert_strategy_asset(strategy_asset_group_id, insert_fx_asset_group.execution_state_id, 'cash', fx_asset.cash_ticker);
END
$$;


CREATE OR REPLACE FUNCTION arp.insert_fx_asset_group(
  strategy_asset_group_id int,
	execution_state_id int,
  currency text
)
  RETURNS VOID
language plpgsql
as
$$
BEGIN
  INSERT INTO arp.fx_asset_group (
    strategy_asset_group_id,
    execution_state_id,
    currency_id
  )
  SELECT
    strategy_asset_group_id,
    insert_fx_asset_group.execution_state_id,
    c.id
  FROM
    lookup.currency c
  WHERE
    c.currency = insert_fx_asset_group.currency
  ;
  return;
END
$$
;