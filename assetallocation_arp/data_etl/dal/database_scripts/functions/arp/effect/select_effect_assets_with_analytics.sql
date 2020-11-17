CREATE OR REPLACE FUNCTION arp.select_effect_assets_with_analytics(
  strategy_version int,
  business_datetime timestamp with time zone
)
  RETURNS TABLE(
    ndf_code varchar,
    spot_code varchar,
    postition_size numeric(32, 16),
    asset_name varchar,
    asset_ticker varchar,
    asset_analytics asset.category_datetime_value[]
  )
LANGUAGE plpgsql
AS
$$
BEGIN
  return query
    WITH effect_assets as (
      SELECT
        ea.asset_id,
        ea.ndf_code,
        ea.spot_code,
        ea.position_size
      FROM
        arp.effect_asset ea
        JOIN arp.effect e on ea.strategy_id = e.strategy_id
      WHERE
        e.version = strategy_version
    ),
    assets as (
      SELECT
        ea2.asset_id,
        a1.name as asset_name,
        a1.ticker as asset_ticker,
        array_agg((aa.category, aa.business_datetime, aa.value)::asset.category_datetime_value) as asset_analytics
      FROM
        effect_assets ea2
        JOIN asset.asset a1 on ea2.asset_id = a1.id
        JOIN asset.asset_analytic aa on a1.id = aa.asset_id
      WHERE
        aa.business_datetime >= select_effect_assets_with_analytics.business_datetime
      GROUP BY
        ea2.asset_id,
        a1.name,
        a1.ticker
    )
    SELECT
      ea3.ndf_code,
      ea3.spot_code,
      ea3.position_size,
      a2.asset_name,
      a2.asset_ticker,
      a2.asset_analytics
    FROM
      effect_assets ea3
      JOIN assets a2 on ea3.asset_id = a2.asset_id
  ;
END
$$;