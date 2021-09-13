DROP FUNCTION IF EXISTS arp.insert_times_assets(integer,text[]);
CREATE OR REPLACE FUNCTION arp.insert_times_assets(
  times_version int,
  times_assets text[]
)
RETURNS VOID
AS
$$
DECLARE
  _execution_state_id int;
  strategy_name varchar := 'times';
  strategy_id int;
  _times_assets arp.ticker_ticker_cost_leverage[];
BEGIN
  _times_assets := times_assets::arp.ticker_ticker_cost_leverage[];

  SELECT config.insert_execution_state('arp.insert_times_assets') INTO _execution_state_id;
  SELECT arp.select_strategy_id(strategy_name, times_version) INTO strategy_id;
  PERFORM arp.insert_times_asset_groups(strategy_id, _execution_state_id, _times_assets);
END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION arp.insert_times_asset_groups(
	strategy_id int,
  execution_state_id int,
  times_assets arp.ticker_ticker_cost_leverage[]
)
  RETURNS VOID
language plpgsql
as
$$
DECLARE
  _len_times_assets int;
  _counter int := 1;
BEGIN
  _len_times_assets = array_length(times_assets, 1);

  loop
    exit when _counter > _len_times_assets;
    PERFORM arp.insert_times_asset_group(strategy_id, insert_times_asset_groups.execution_state_id, times_assets[_counter]);
    _counter := _counter + 1;
  end loop;
END
$$;


CREATE OR REPLACE FUNCTION arp.insert_times_asset_group(
	strategy_id int,
  execution_state_id int,
  times_asset arp.ticker_ticker_cost_leverage
)
  RETURNS VOID
language plpgsql
as
$$
DECLARE
  strategy_asset_group_id int;
BEGIN

  SELECT arp.insert_strategy_asset_group(strategy_id, insert_times_asset_group.execution_state_id) INTO strategy_asset_group_id;
  PERFORM arp.insert_times_asset_group(strategy_asset_group_id, insert_times_asset_group.execution_state_id, times_asset.cost, times_asset.s_leverage);
  PERFORM arp.insert_strategy_asset(strategy_asset_group_id, insert_times_asset_group.execution_state_id, 'signal', times_asset.signal_ticker);
  PERFORM arp.insert_strategy_asset(strategy_asset_group_id, insert_times_asset_group.execution_state_id, 'future', times_asset.future_ticker);
END
$$;


CREATE OR REPLACE FUNCTION arp.insert_times_asset_group(
  strategy_asset_group_id int,
	execution_state_id int,
  cost numeric,
  s_leverage int
)
  RETURNS VOID
language plpgsql
as
$$
BEGIN
  INSERT INTO arp.times_asset_group (strategy_asset_group_id, execution_state_id, cost, s_leverage)
  VALUES (
    strategy_asset_group_id,
    insert_times_asset_group.execution_state_id,
    cost,
    s_leverage
  );
  return;
END
$$