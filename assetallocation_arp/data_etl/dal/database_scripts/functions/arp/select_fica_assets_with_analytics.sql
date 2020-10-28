CREATE OR REPLACE FUNCTION arp.select_fica_assets_with_analytics(
  strategy_version int
)
  RETURNS TABLE(
    fica_asset_category varchar,
    curve_tenor varchar,
    asset_name varchar,
    asset_ticker varchar,
    asset_analytics arp.category_datetime_value[]
  )
LANGUAGE plpgsql
AS
$$
BEGIN
  return query
    WITH fica_assets as (
      SELECT
        fa.asset_id,
        fa.category as fica_asset_category,
        fa.curve_tenor,
        f.business_tstzrange
      FROM
        arp.fica_asset fa
        JOIN arp.fica f on fa.strategy_id = f.strategy_id
      WHERE
        f.version = strategy_version
    ),
    assets as (
      SELECT
        fa2.asset_id,
        a1.name as asset_name,
        a1.ticker as asset_ticker,
        array_agg((aa.category, aa.business_datetime, aa.value)::arp.category_datetime_value) as asset_analytics
      FROM
        fica_assets fa2
        JOIN asset.asset a1 on fa2.asset_id = a1.id
        JOIN asset.asset_analytic aa on a1.id = aa.asset_id
      WHERE
        aa.business_datetime <@ fica_assets.business_tstzrange
      GROUP BY
        fa2.asset_id,
        a1.name,
        a1.ticker
    )
    SELECT
      fa3.fica_asset_category,
      fa3.curve_tenor,
      a2.asset_name,
      a2.asset_ticker,
      a2.asset_analytics
    FROM
      fica_assets fa3
      JOIN assets a2 on fa3.asset_id = a2.asset_id
  ;
END
$$;