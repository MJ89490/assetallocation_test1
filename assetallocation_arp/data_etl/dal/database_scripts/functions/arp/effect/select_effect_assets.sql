CREATE OR REPLACE FUNCTION arp.select_effect_assets(
  strategy_version int
)
RETURNS TABLE(
    asset_ticker varchar,
    asset_subcategory varchar,
    ndf_code varchar,
    spot_code varchar,
    position_size numeric(32, 16)
  )
LANGUAGE plpgsql
AS
$$
BEGIN
  return query
    SELECT
      a.ticker as asset_ticker,
      ag.subcategory as asset_subcategory,
      eag.ndf_code,
      eag.spot_code,
      eag.position_size
    FROM
      arp.effect e
      JOIN arp.strategy_asset_group sag ON e.strategy_id = sag.strategy_id
      JOIN arp.effect_asset_group eag ON sag.id = eag.strategy_asset_group_id
      JOIN arp.strategy_asset sa ON sag.id = sa.strategy_asset_group_id
      JOIN asset.asset a ON sa.asset_id = a.id
      JOIN asset.asset_group ag ON a.asset_group_id = ag.id
    WHERE
      e.version = strategy_version
  ;
END
$$;
