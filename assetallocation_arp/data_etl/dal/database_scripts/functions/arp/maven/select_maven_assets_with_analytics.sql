CREATE OR REPLACE FUNCTION arp.select_maven_assets_with_analytics(
  strategy_version int,
  business_tstzrange tstzrange
)
  RETURNS TABLE(
    bbg_tr_ticker varchar,
    bbg_tr_asset_analytics asset.category_datetime_value[],
    bbg_er_ticker varchar,
    bbg_er_asset_analytics asset.category_datetime_value[],
    cash_ticker varchar,
    cash_asset_analytics asset.category_datetime_value[],
    asset_subcategory varchar,
    currency varchar,
    is_excess boolean,
    asset_weight numeric,
    transaction_cost numeric
  )
LANGUAGE plpgsql
AS
$$
BEGIN
  return query
    SELECT
      max(a.ticker) FILTER (WHERE sa.name = 'bbg_tr') as bbg_tr_ticker,
      array_agg((aa.category, aa.business_datetime, aa.value)::asset.category_datetime_value) FILTER (WHERE sa.name = 'bbg_tr') as bbg_tr_asset_analytics,
      max(a.ticker) FILTER (WHERE sa.name = 'bbg_er') as bbg_er_ticker,
      array_agg((aa.category, aa.business_datetime, aa.value)::asset.category_datetime_value) FILTER (WHERE sa.name = 'bbg_er') as bbg_er_asset_analytics,
      max(a.ticker) FILTER (WHERE sa.name = 'cash') as cash_ticker,
      array_agg((aa.category, aa.business_datetime, aa.value)::asset.category_datetime_value) FILTER (WHERE sa.name = 'cash') as cash_asset_analytics,
      string_agg(ag.subcategory, '') FILTER (
        WHERE sa.name = (
          CASE
            WHEN m.er_tr = 'excess' THEN 'bbg_er'
            ELSE 'bbg_tr'
          END
        )
      ) as asset_subcategory,
      c.currency,
      mag.is_excess,
      mag.asset_weight,
      mag.transaction_cost
    FROM
      arp.maven m
      JOIN arp.strategy_asset_group sag ON m.strategy_id = sag.strategy_id
      JOIN arp.maven_asset_group mag ON sag.id = mag.strategy_asset_group_id
      JOIN lookup.currency c on mag.currency_id = c.id
      JOIN arp.strategy_asset sa ON sag.id = sa.strategy_asset_group_id
      JOIN asset.asset a ON sa.asset_id = a.id
      JOIN asset.asset_analytic aa ON a.id = aa.asset_id
      JOIN asset.asset_group ag ON a.asset_group_id = ag.id
    WHERE
        m.version = strategy_version
        AND aa.business_datetime <@ select_maven_assets_with_analytics.business_tstzrange
      GROUP BY
        mag.strategy_asset_group_id,
        c.currency,
        mag.is_excess,
        mag.asset_weight,
        mag.transaction_cost
  ;
END
$$;
