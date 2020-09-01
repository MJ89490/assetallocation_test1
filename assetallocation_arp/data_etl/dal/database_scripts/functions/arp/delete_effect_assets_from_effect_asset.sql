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


