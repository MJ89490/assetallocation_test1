CREATE OR REPLACE FUNCTION arp.insert_times_assets(
  times_version int,
  times_assets text[],
  OUT asset_ids int[]
)
AS
$$
DECLARE
  execution_state_id int;
  strategy_name varchar;
  strategy_id int;
  _times_assets asset.times_asset[];
BEGIN
  strategy_name := 'times';
  _times_assets := times_assets::asset.times_asset[];
  SELECT config.insert_execution_state('arp.insert_times_assets') INTO execution_state_id;
  SELECT arp.select_strategy_id(strategy_name, times_version) INTO strategy_id;
  SELECT array(select id from asset.insert_times_assets_into_asset(execution_state_id, _times_assets)) INTO asset_ids;
  PERFORM arp.delete_times_assets_from_times_asset(strategy_id);
  PERFORM arp.insert_times_assets_ids_into_times_asset(strategy_id, execution_state_id, asset_ids);
END;
$$
LANGUAGE plpgsql;