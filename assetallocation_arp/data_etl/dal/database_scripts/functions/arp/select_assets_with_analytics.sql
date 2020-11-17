CREATE OR REPLACE FUNCTION asset.select_assets_with_analytics(
  tickers text[],
  business_tstzrange tstzrange
)
  RETURNS TABLE(
    name varchar,
    ticker varchar,
    analytics asset.category_datetime_value[]
  )
LANGUAGE plpgsql
AS
$$
BEGIN
  return query
    SELECT
      a.name,
      a.ticker,
      array_agg((aa.category, aa.business_datetime, aa.value)::asset.category_datetime_value) as analytics
    FROM
      asset.asset a
      JOIN asset.asset_analytic aa on a.id = aa.asset_id
    WHERE
      aa.business_datetime <@ select_assets_with_analytics.business_tstzrange
      AND a.ticker = ANY(select_assets_with_analytics.tickers)
    GROUP BY
      a.name,
      a.ticker
  ;
END
$$;