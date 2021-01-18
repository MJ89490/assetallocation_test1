CREATE OR REPLACE FUNCTION arp.select_fx_assets_with_analytics(
  strategy_version int,
  business_tstzrange tstzrange
)
  RETURNS TABLE(
    ppp_ticker varchar,
    ppp_asset_analytics asset.category_datetime_value[],
    cash_ticker varchar,
    cash_asset_analytics asset.category_datetime_value[],
    currency numeric(32, 16)
  )
LANGUAGE plpgsql
AS
$$
BEGIN
  return query
    SELECT
      max(a.ticker) FILTER (WHERE sa.name = 'ppp') as ppp_ticker,
      array_agg((aa.category, aa.business_datetime, aa.value)::asset.category_datetime_value) FILTER (WHERE sa.name = 'ppp') as ppp_asset_analytics,
      max(a.ticker) FILTER (WHERE sa.name = 'cash') as cash_ticker,
      array_agg((aa.category, aa.business_datetime, aa.value)::asset.category_datetime_value) FILTER (WHERE sa.name = 'cash') as cash_asset_analytics,
      c.currency
    FROM
      arp.fx f
      JOIN arp.strategy_asset_group sag ON f.strategy_id = sag.strategy_id
      JOIN arp.fx_asset_group fag ON sag.id = fag.strategy_asset_group_id
      JOIN lookup.currency c on fag.currency_id = c.id
      JOIN arp.strategy_asset sa ON sag.id = sa.strategy_asset_group_id
      JOIN asset.asset a ON sa.asset_id = a.id
      JOIN asset.asset_analytic aa ON a.id = aa.asset_id
      JOIN asset.asset_group ag ON a.asset_group_id = ag.id
    WHERE
        f.version = strategy_version
        AND aa.business_datetime <@ select_fx_assets_with_analytics.business_tstzrange
      GROUP BY
        fag.strategy_asset_group_id,
        c.currency
  ;
END
$$;