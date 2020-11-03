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

CREATE OR REPLACE FUNCTION arp.delete_effect_assets_from_effect_asset(
  strategy_id int
)
  RETURNS VOID
AS
$$
BEGIN
  DELETE FROM arp.effect_asset ea WHERE ea.strategy_id = delete_effect_assets_from_effect_asset.strategy_id;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION arp.insert_effect_assets_into_effect_asset(
  strategy_id int,
  execution_state_id int,
  effect_assets arp.ticker_code_code_size[]
)
RETURNS void
AS
$$
BEGIN
  INSERT INTO arp.effect_asset(
    strategy_id,
    asset_id,
    ndf_code,
    position_size,
    spot_code,
    execution_state_id
  )
  SELECT
    strategy_id,
    a.id,
    (ea).ndf_code,
    (ea).position_size,
    (ea).spot_code,
    insert_effect_assets_into_effect_asset.execution_state_id
  FROM
    unnest(effect_assets) as ea
    JOIN asset.asset a ON (ea).ticker = a.ticker
;
END;
$$
LANGUAGE plpgsql;
