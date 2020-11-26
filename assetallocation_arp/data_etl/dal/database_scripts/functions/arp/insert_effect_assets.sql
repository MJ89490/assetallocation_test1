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
  _effect_assets arp.currency_ticker_ticker_ticker_weight_base_region[];
BEGIN
  strategy_name := 'effect';
  _effect_assets := effect_assets::arp.currency_ticker_ticker_ticker_weight_base_region[];

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
  effect_assets arp.currency_ticker_ticker_ticker_weight_base_region[]
)
RETURNS void
AS
$$
BEGIN
  INSERT INTO arp.effect_asset(
    strategy_id,
    asset_3m_id,
    spot_asset_id,
    carry_asset_id,
    currency,
    usd_weight,
    base,
    region,
    execution_state_id
  )
  SELECT
    strategy_id,
    a_3m.id,
    a_spot.id,
    a_carry.id,
    (ea).currency,
    (ea).usd_weight,
    (ea).base,
    (ea).region,
    insert_effect_assets_into_effect_asset.execution_state_id
  FROM
    unnest(effect_assets) as ea
    JOIN asset.asset a_3m ON (ea).ticker_3m = a_3m.ticker
    JOIN asset.asset a_spot ON (ea).spot_ticker = a_spot.ticker
    JOIN asset.asset a_carry ON (ea).carry_ticker = a_carry.ticker
  ;
END;
$$
LANGUAGE plpgsql;
