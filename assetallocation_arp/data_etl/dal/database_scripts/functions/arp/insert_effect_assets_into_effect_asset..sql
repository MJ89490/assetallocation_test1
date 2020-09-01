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