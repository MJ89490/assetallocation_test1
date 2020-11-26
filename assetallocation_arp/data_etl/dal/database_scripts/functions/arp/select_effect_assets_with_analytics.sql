CREATE OR REPLACE FUNCTION arp.select_effect_assets_with_analytics(
  strategy_version int,
  business_datetime timestamp with time zone
)
  RETURNS TABLE(
    asset_subcategory varchar,
    ticker_3m varchar,
    asset_analytics_3m asset.category_datetime_value[],
    spot_ticker varchar,
    spot_asset_analytics asset.category_datetime_value[],
    carry_ticker varchar,
    carry_asset_analytics asset.category_datetime_value[],
    currency varchar,
    usd_weight numeric(32, 16),
    base varchar,
    region varchar
  )
LANGUAGE plpgsql
AS
$$
BEGIN
  return query
    WITH effect_assets as (
      SELECT
        ea.currency,
        ea.asset_3m_id,
        ea.spot_asset_id,
        ea.carry_asset_id,
        ea.usd_weight,
        ea.base,
        ea.region
      FROM
        arp.effect_asset ea
        JOIN arp.effect e on ea.strategy_id = e.strategy_id
        JOIN arp.strategy s on e.strategy_id = s.id
      WHERE
        e.version = strategy_version
    ),
    assets_3m as (
      SELECT
        ea2.asset_3m_id,
        a1.ticker as ticker_3m,
        array_agg((aa.category, aa.business_datetime, aa.value)::asset.category_datetime_value) as asset_analytics_3m
      FROM
        effect_assets ea2
        JOIN asset.asset a1 on ea2.asset_3m_id = a1.id
        JOIN asset.asset_analytic aa on a1.id = aa.asset_id
      WHERE
        aa.business_datetime >= select_effect_assets_with_analytics.business_datetime
      GROUP BY
        ea2.asset_3m_id,
        a1.ticker
    ),
    assets_spot as (
      SELECT
        ea2.spot_asset_id,
        a1.ticker as spot_ticker,
        array_agg((aa.category, aa.business_datetime, aa.value)::asset.category_datetime_value) as spot_asset_analytics
      FROM
        effect_assets ea2
        JOIN asset.asset a1 on ea2.spot_asset_id = a1.id
        JOIN asset.asset_analytic aa on a1.id = aa.asset_id
      WHERE
        aa.business_datetime >= select_effect_assets_with_analytics.business_datetime
      GROUP BY
        ea2.spot_asset_id,
        a1.ticker
    ),
    assets_carry as (
      SELECT
        ea2.carry_asset_id,
        a1.ticker as carry_ticker,
        a1.subcategory as asset_subcategory,
        array_agg((aa.category, aa.business_datetime, aa.value)::asset.category_datetime_value) as carry_asset_analytics
      FROM
        effect_assets ea2
        JOIN asset.asset a1 on ea2.carry_asset_id = a1.id
        JOIN asset.asset_analytic aa on a1.id = aa.asset_id
      WHERE
        aa.business_datetime >= select_effect_assets_with_analytics.business_datetime
      GROUP BY
        ea2.carry_asset_id,
        a1.ticker
    )
    SELECT
      assets_carry.asset_subcategory,
      assets_3m.ticker_3m,
      assets_3m.asset_analytics_3m,
      assets_spot.spot_ticker,
      assets_spot.spot_asset_analytics,
      assets_carry.carry_ticker,
      assets_carry.carry_asset_analytics,
      ea3.currency,
      ea3.usd_weight,
      ea3.base,
      ea3.region
    FROM
      effect_assets ea3
      JOIN assets_3m on ea3.asset_3m_id = assets_3m.asset_3m_id
      JOIN assets_spot on ea3.spot_asset_id = assets_spot.spot_asset_id
      JOIN assets_carry on ea3.carry_asset_id = assets_carry.carry_asset_id
  ;
END
$$;