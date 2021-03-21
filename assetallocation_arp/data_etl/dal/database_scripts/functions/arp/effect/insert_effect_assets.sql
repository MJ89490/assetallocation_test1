CREATE OR REPLACE FUNCTION arp.insert_effect_assets(
  effect_version int,
  effect_assets text[]
)
RETURNS VOID
AS
$$
DECLARE
  execution_state_id int;
  strategy_name varchar := 'effect';
  strategy_id int;
  _effect_assets arp.ticker_code_code_size[];
BEGIN
  _effect_assets := effect_assets::arp.ticker_code_code_size[];

  SELECT config.insert_execution_state('arp.insert_times_assets') INTO execution_state_id;
  SELECT arp.select_strategy_id(strategy_name, effect_version) INTO strategy_id;
  PERFORM arp.insert_effect_asset_groups(strategy_id, execution_state_id, _effect_assets);
END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION arp.insert_effect_asset_groups(
	strategy_id int,
  execution_state_id int,
  effect_assets arp.ticker_code_code_size[]
)
  RETURNS VOID
language plpgsql
as
$$
DECLARE
  _len_effect_assets int;
  _counter int := 1;
BEGIN
  _len_effect_assets = array_length(effect_assets, 1);

  loop
    exit when _counter > _len_effect_assets;
    PERFORM arp.insert_effect_asset_group(strategy_id, insert_effect_asset_groups.execution_state_id, effect_assets[_counter]);
    _counter := _counter + 1;
  end loop;
END
$$;


CREATE OR REPLACE FUNCTION arp.insert_effect_asset_group(
	strategy_id int,
  execution_state_id int,
  effect_asset arp.ticker_code_code_size
)
  RETURNS VOID
language plpgsql
as
$$
DECLARE
  strategy_asset_group_id int;
BEGIN
  SELECT arp.insert_strategy_asset_group(strategy_id, insert_effect_asset_group.execution_state_id) INTO strategy_asset_group_id;
  PERFORM arp.insert_effect_asset_group(
      strategy_asset_group_id,
      insert_effect_asset_group.execution_state_id,
      effect_asset.ndf_code,
      effect_asset.spot_code,
      effect_asset.position_size
  );
  PERFORM arp.insert_strategy_asset(strategy_asset_group_id, insert_effect_asset_group.execution_state_id, '', effect_asset.ticker);
END
$$;


CREATE OR REPLACE FUNCTION arp.insert_effect_asset_group(
  strategy_asset_group_id int,
	execution_state_id int,
  ndf_code text,
  spot_code text,
  position_size NUMERIC(32, 16)
)
  RETURNS VOID
language plpgsql
as
$$
BEGIN
  INSERT INTO arp.effect_asset_group (
    strategy_asset_group_id,
    execution_state_id,
    ndf_code,
    spot_code,
    position_size
  )
  VALUES (
    strategy_asset_group_id,
    insert_effect_asset_group.execution_state_id,
    ndf_code,
    spot_code,
    position_size
  )
  ;
  return;
END
$$;
