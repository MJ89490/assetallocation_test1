CREATE OR REPLACE FUNCTION arp.select_maven_assets_with_analytics(
  strategy_version int
)
  RETURNS TABLE(
    bbg_tr_ticker varchar,
    bbg_tr_asset_analytics asset.category_datetime_value[],
    bbg_er_ticker varchar,
    bbg_er_asset_analytics asset.category_datetime_value[],
    cash_ticker varchar,
    cash_asset_analytics asset.category_datetime_value[],
    asset_category varchar,
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
    WITH maven_assets as (
      SELECT
        ma.bbg_tr_asset_id,
        ma.bbg_er_asset_id,
        ma.cash_asset_id,
        ma.asset_category,
        ma.asset_subcategory,
        ma.currency,
        ma.is_excess,
        ma.asset_weight,
        ma.transaction_cost,
        m.business_tstzrange
      FROM
        arp.maven_asset ma
        JOIN arp.maven m on ma.strategy_id = m.strategy_id
      WHERE
        m.version = strategy_version
    ),
    bbg_ers as (
      SELECT
        ta2.bbg_er_asset_id,
        a.ticker as bbg_er_ticker,
        array_agg((aa.category, aa.business_datetime, aa.value)::asset.category_datetime_value) as bbg_er_asset_analytics
      FROM
        maven_assets ta2
        JOIN asset.asset a on ta2.bbg_er_asset_id = a.id
        JOIN asset.asset_analytic aa on a.id = aa.asset_id
      WHERE
        aa.business_datetime <@ maven_assets.business_tstzrange
      GROUP BY
        ta2.bbg_er_asset_id,
        a.ticker
    ),
    bbg_trs as (
      SELECT
        ta3.bbg_tr_asset_id,
        a.ticker as bbg_tr_ticker,
        array_agg((aa.category, aa.business_datetime, aa.value)::asset.category_datetime_value) as bbg_tr_asset_analytics
      FROM
        maven_assets ta3
        JOIN asset.asset a on ta3.bbg_tr_asset_id = a.id
        JOIN asset.asset_analytic aa on a.id = aa.asset_id
      WHERE
        aa.business_datetime <@ maven_assets.business_tstzrange
      GROUP BY
        ta3.bbg_tr_asset_id,
        a.ticker
    ),
    cash as (
      SELECT
        ma4.cash_asset_id,
        a.ticker as cash_ticker,
        array_agg((aa.category, aa.business_datetime, aa.value)::asset.category_datetime_value) as cash_asset_analytics
      FROM
        maven_assets ma4
        JOIN asset.asset a on ma4.cash_asset_id = a.id
        JOIN asset.asset_analytic aa on a.id = aa.asset_id
      WHERE
        aa.business_datetime <@ maven_assets.business_tstzrange
      GROUP BY
        ma4.cash_asset_id,
        a.ticker
    )
    SELECT
      t.bbg_tr_ticker,
      t.bbg_tr_asset_analytics,
      e.bbg_er_ticker,
      e.bbg_er_asset_analytics,
      c.cash_ticker,
      c.cash_asset_analytics,
      ma5.asset_category,
      ma5.asset_subcategory,
      ma5.currency,
      ma5.is_excess,
      ma5.asset_weight,
      ma5.transaction_cost
    FROM
      maven_assets ma5
      JOIN bbg_trs t on ma5.bbg_tr_asset_id = t.bbg_tr_asset_id
      JOIN bbg_ers e on ma5.bbg_er_asset_id = e.bbg_er_asset_id
      JOIN cash c on ma5.cash_asset_id = c.cash_asset_id
  ;
END
$$;
