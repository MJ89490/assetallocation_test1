CREATE OR REPLACE FUNCTION arp.select_effect_assets_with_analytics(
  strategy_version int,
  business_tstzrange tstzrange
)
  RETURNS TABLE(
    asset_subcategory text,
    currency varchar,
    usd_weight numeric(32,16),
    base varchar,
    region varchar,
    ticker_3m text,
    asset_analytics_3m asset.category_datetime_value[],
    spot_ticker text,
    spot_asset_analytics asset.category_datetime_value[],
    carry_ticker text,
    carry_asset_analytics asset.category_datetime_value[]
  )
LANGUAGE plpgsql
AS
$$
BEGIN
  return query
    WITH effect_assets as (
    SELECT
      max(a.id) FILTER (WHERE sa.name = '3m') as asset_id_3m,
      max(a.id) FILTER (WHERE sa.name = 'spot') as spot_asset_id,
      max(a.id) FILTER (WHERE sa.name = 'carry') as carry_asset_id,
      string_agg(ag.subcategory, '') FILTER (WHERE sa.name = 'carry') as asset_subcategory,
      eag.currency,
      eag.usd_weight,
      eag.base,
      eag.region
    FROM
      arp.effect e
      JOIN arp.strategy_asset_group sag ON e.strategy_id = sag.strategy_id
      JOIN arp.effect_asset_group eag ON sag.id = eag.strategy_asset_group_id
      JOIN arp.strategy_asset sa ON sag.id = sa.strategy_asset_group_id
      JOIN asset.asset a ON sa.asset_id = a.id
      JOIN asset.asset_group ag ON a.asset_group_id = ag.id
    WHERE
      e.version = strategy_version
      AND sa.name in ('future', 'signal')
    GROUP BY
      eag.strategy_asset_group_id,
      eag.currency,
      eag.region,
      eag.base,
      eag.usd_weight
    ),
    spots as (
      SELECT
        ea2.spot_asset_id,
        a.ticker as spot_ticker,
        array_agg((aa.category, aa.business_datetime, aa.value)::asset.category_datetime_value) as spot_asset_analytics
      FROM
        effect_assets ea2
        JOIN asset.asset a on ea2.spot_asset_id = a.id
        JOIN asset.asset_analytic aa on a.id = aa.asset_id
      WHERE
        aa.business_datetime <@ select_effect_assets_with_analytics.business_tstzrange
        AND upper(aa.system_tstzrange) = 'infinity'
      GROUP BY
        ea2.spot_asset_id,
        a.ticker
    ),
    carries as (
      SELECT
        ea3.carry_asset_id,
        a.ticker as carry_ticker,
        array_agg((aa.category, aa.business_datetime, aa.value)::asset.category_datetime_value) as carry_asset_analytics
      FROM
        effect_assets ea3
        JOIN asset.asset a on ea3.carry_asset_id = a.id
        JOIN asset.asset_analytic aa on a.id = aa.asset_id
      WHERE
        aa.business_datetime <@ select_effect_assets_with_analytics.business_tstzrange
        AND upper(aa.system_tstzrange) = 'infinity'
      GROUP BY
        ea3.carry_asset_id,
        a.ticker
    ),
    tm as (
      SELECT
        ea4.asset_id_3m,
        a.ticker as ticker_3m,
        array_agg((aa.category, aa.business_datetime, aa.value)::asset.category_datetime_value) as asset_analytics_3m
      FROM
        effect_assets ea4
        JOIN asset.asset a on ea4.asset_id_3m = a.id
        JOIN asset.asset_analytic aa on a.id = aa.asset_id
      WHERE
        aa.business_datetime <@ select_effect_assets_with_analytics.business_tstzrange
        AND upper(aa.system_tstzrange) = 'infinity'
      GROUP BY
        ea4.asset_id_3m,
        a.ticker
    )
    SELECT
      ea5.asset_subcategory,
      ea5.currency,
      ea5.usd_weight,
      ea5.base,
      ea5.region,
      tm.ticker_3m::text,
      tm.asset_analytics_3m,
      s.spot_ticker::text,
      s.spot_asset_analytics,
      c.carry_ticker::text,
      c.carry_asset_analytics
    FROM
      effect_assets ea5
      JOIN carries c on ea5.carry_asset_id = c.carry_asset_id
      JOIN spots s on ea5.spot_asset_id = s.spot_asset_id
      JOIN tm on ea5.asset_id_3m = tm.asset_id_3m
  ;
END
$$;