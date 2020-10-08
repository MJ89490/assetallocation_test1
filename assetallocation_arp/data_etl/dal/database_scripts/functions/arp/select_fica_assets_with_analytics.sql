CREATE OR REPLACE FUNCTION arp.select_fica_assets_with_analytics(
  strategy_version int,
  business_datetime timestamp with time zone
)
  RETURNS TABLE(
    sovereign_ticker curve.ticker_months_years,
    swap_ticker curve.ticker_months_years,
    swap_cr_ticker curve.ticker_months_years,
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
        (t1.category, t1.mth3, t1.yr1, t1.yr2, t1.yr3, t1.yr4, t1.yr5, t1.yr6, t1.yr7, t1.yr8, t1.yr9, t1.yr10, t1.yr15, t1.yr20, t1.yr30):: curve.ticker_months_years as sovereign_ticker,
        (t2.category, t2.mth3, t2.yr1, t2.yr2, t2.yr3, t2.yr4, t2.yr5, t2.yr6, t2.yr7, t2.yr8, t2.yr9, t2.yr10, t2.yr15, t2.yr20, t2.yr30):: curve.ticker_months_years as swap_ticker,
        (t3.category, t3.mth3, t3.yr1, t3.yr2, t3.yr3, t3.yr4, t3.yr5, t3.yr6, t3.yr7, t3.yr8, t3.yr9, t3.yr10, t3.yr15, t3.yr20, t3.yr30):: curve.ticker_months_years as swap_cr_ticker
      FROM
        arp.fica_asset fa
        JOIN curve.ticker t1 on fa.sovereign_ticker_id = t1.id
        JOIN curve.ticker t2 on fa.swap_ticker_id = t2.id
        JOIN curve.ticker t3 on fa.swap_cr_ticker_id = t3.id
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
        aa.business_datetime >= select_fica_assets_with_analytics.business_datetime
      GROUP BY
        fa2.asset_id,
        a1.name,
        a1.ticker
    )
    SELECT
      fa3.sovereign_ticker,
      fa3.swap_ticker,
      fa3.swap_cr_ticker,
      a2.asset_name,
      a2.asset_ticker,
      a2.asset_analytics
    FROM
      fica_assets fa3
      JOIN assets a2 on fa3.asset_id = a2.asset_id
  ;
END
$$;