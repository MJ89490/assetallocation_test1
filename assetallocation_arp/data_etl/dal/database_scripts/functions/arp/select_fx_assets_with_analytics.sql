CREATE OR REPLACE FUNCTION arp.select_fx_assets_with_analytics(
  strategy_version int
)
  RETURNS TABLE(
    currency numeric(32, 16),
    ppp_name varchar,
    ppp_ticker varchar,
    ppp_asset_analytics asset.category_datetime_value[],
    cash_rate_name varchar,
    cash_rate_ticker varchar,
    cash_rate_asset_analytics asset.category_datetime_value[]
  )
LANGUAGE plpgsql
AS
$$
BEGIN
  return query
    WITH fx_assets as (
      SELECT
        fa.ppp_asset_id,
        fa.cash_rate_asset_id,
        fa.currency,
        f.business_tstzrange
      FROM
        arp.fx_asset fa
        JOIN arp.fx f on fa.strategy_id = f.strategy_id
      WHERE
        f.version = strategy_version
    ),
    cash_rates as (
      SELECT
        fa2.cash_rate_asset_id,
        a.name as cash_rate_name,
        a.ticker as cash_rate_ticker,
        array_agg(
            (aa.category, aa.business_datetime, aa.value)::asset.category_datetime_value
        ) as cash_rate_asset_analytics
      FROM
        fx_assets fa2
        JOIN asset.asset a on fa2.cash_rate_asset_id = a.id
        JOIN asset.asset_analytic aa on a.id = aa.asset_id
      WHERE
        aa.business_datetime <@ fx_assets.business_tstzrange
      GROUP BY
        fa2.cash_rate_asset_id,
        a.name,
        a.ticker
    ),
    ppps as (
      SELECT
        ta3.ppp_asset_id,
        a.name as ppp_name,
        a.ticker as ppp_ticker,
        array_agg(
            (aa.category, aa.business_datetime, aa.value)::asset.category_datetime_value
        ) as ppp_asset_analytics
      FROM
        fx_assets ta3
        JOIN asset.asset a on ta3.ppp_asset_id = a.id
        JOIN asset.asset_analytic aa on a.id = aa.asset_id
      WHERE
        aa.business_datetime <@ fx_assets.business_tstzrange
      GROUP BY
        ta3.ppp_asset_id,
        a.name,
        a.ticker
    )
    SELECT
      fa4.currency,
      p.ppp_name,
      p.ppp_ticker,
      p.ppp_asset_analytics,
      c.cash_rate_name,
      c.cash_rate_ticker,
      c.cash_rate_asset_analytics
    FROM
      fx_assets fa4
      JOIN ppps p on fa4.ppp_asset_id = p.ppp_asset_id
      JOIN cash_rates c on fa4.cash_rate_asset_id = c.cash_rate_asset_id
  ;
END
$$;