CREATE OR REPLACE FUNCTION arp.select_fica_assets_with_analytics(
  strategy_version int,
  business_tstzrange tstzrange
)
  RETURNS TABLE(
    asset_subcategory varchar,
    fica_asset_name varchar,
    asset_ticker varchar,
    asset_analytics asset.category_datetime_value[]
  )
LANGUAGE plpgsql
AS
$$
BEGIN
  return query
    WITH fica_assets as (
      SELECT
        string_agg(ag.subcategory, '') FILTER (WHERE sa.name = concat('yr', f.tenor, '_', f.curve)) as asset_subcategory,
        sa.asset_id,
        sa.name as fica_asset_name
      FROM
        arp.fica f
        JOIN arp.strategy_asset_group sag ON f.strategy_id = sag.strategy_id
        JOIN arp.strategy_asset sa ON sag.id = sa.strategy_asset_group_id
        JOIN asset.asset a ON sa.asset_id = a.id
        JOIN asset.asset_group ag ON a.asset_group_id = ag.id
      WHERE
        f.version = strategy_version
      GROUP BY
        sa.strategy_asset_group_id,
        sa.asset_id,
        sa.name
    ),
    assets as (
      SELECT
        fa2.asset_id,
        a1.ticker as asset_ticker,
        array_agg((aa.category, aa.business_datetime, aa.value)::asset.category_datetime_value) as asset_analytics
      FROM
        fica_assets fa2
        JOIN asset.asset a1 on fa2.asset_id = a1.id
        JOIN asset.asset_analytic aa on a1.id = aa.asset_id
      WHERE
        aa.business_datetime <@ select_fica_assets_with_analytics.business_tstzrange
      GROUP BY
        fa2.asset_id,
        a1.name,
        a1.ticker
    )
    SELECT
      fa3.asset_subcategory,
      fa3.fica_asset_name,
      a2.asset_ticker,
      a2.asset_analytics
    FROM
      fica_assets fa3
      JOIN assets a2 on fa3.asset_id = a2.asset_id
  ;
END
$$;