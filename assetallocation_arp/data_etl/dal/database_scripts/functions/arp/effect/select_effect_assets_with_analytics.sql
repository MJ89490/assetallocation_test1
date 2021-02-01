CREATE OR REPLACE FUNCTION arp.select_effect_assets_with_analytics(
  strategy_version int,
  business_tstzrange tstzrange
)
  RETURNS TABLE(
    asset_ticker varchar,
    asset_analytics asset.category_datetime_value[],
    asset_subcategory varchar,
    ndf_code varchar,
    spot_code varchar,
    postition_size numeric(32, 16)
  )
LANGUAGE plpgsql
AS
$$
BEGIN
  return query
    SELECT
      eag.ndf_code,
      eag.spot_code,
      eag.position_size,
      a.ticker as asset_ticker,
      array_agg((aa.category, aa.business_datetime, aa.value)::asset.category_datetime_value) as asset_analytics,
      max(ag.subcategory) as asset_subcategory
    FROM
      arp.effect e
      JOIN arp.strategy_asset_group sag ON e.strategy_id = sag.strategy_id
      JOIN arp.effect_asset_group eag ON sag.id = eag.strategy_asset_group_id
      JOIN arp.strategy_asset sa ON sag.id = sa.strategy_asset_group_id
      JOIN asset.asset a ON sa.asset_id = a.id
      JOIN asset.asset_analytic aa ON a.id = aa.asset_id
      JOIN asset.asset_group ag ON a.asset_group_id = ag.id
    WHERE
      e.version = strategy_version
      AND aa.business_datetime <@ select_effect_assets_with_analytics.business_tstzrange
    GROUP BY
      eag.strategy_asset_group_id,
      eag.ndf_code,
      eag.spot_code,
      eag.position_size,
      a.ticker
  ;
END
$$;