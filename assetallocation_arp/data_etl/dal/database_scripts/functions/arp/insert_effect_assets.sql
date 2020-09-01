CREATE OR REPLACE FUNCTION arp.insert_effect_assets(
  effect_version int,
  effect_assets text[]
)
RETURNS VOID
AS
$$
DECLARE
  execution_state_id int;
  strategy_name varchar;
  strategy_id int;
  _effect_assets arp.ticker_code_code_size[];
BEGIN
  strategy_name := 'effect';
  _effect_assets := effect_assets::arp.ticker_code_code_size[];

  SELECT config.insert_execution_state('arp.insert_times_assets') INTO execution_state_id;
  SELECT arp.select_strategy_id(strategy_name, effect_version) INTO strategy_id;
  PERFORM arp.delete_effect_assets_from_effect_asset(strategy_id);
  PERFORM arp.insert_effect_assets_into_effect_asset(strategy_id, execution_state_id, _effect_assets);
END;
$$
LANGUAGE plpgsql;