CREATE OR REPLACE FUNCTION arp.select_times_assets_with_analytics(
  strategy_version int,
  business_datetime timestamp with time zone
)
  RETURNS TABLE(
    cost numeric(32, 16),
    s_leverage integer,
    future_name varchar,
    future_ticker varchar,
    future_asset_analytics asset.category_datetime_value[],
    signal_name varchar,
    signal_ticker varchar,
    signal_asset_analytics asset.category_datetime_value[]
  )
LANGUAGE plpgsql
AS
$$
BEGIN
  return query
    WITH times_assets as (
      SELECT
        ta.future_asset_id,
        ta.signal_asset_id,
        ta.cost,
        ta.s_leverage
      FROM
        arp.times_asset ta
        JOIN arp.times t on ta.strategy_id = t.strategy_id
      WHERE
        t.version = strategy_version
    ),
    signals as (
      SELECT
        ta2.signal_asset_id,
        a.name as signal_name,
        a.ticker as signal_ticker,
        array_agg((aa.category, aa.business_datetime, aa.value)::asset.category_datetime_value) as signal_asset_analytics
      FROM
        times_assets ta2
        JOIN asset.asset a on ta2.signal_asset_id = a.id
        JOIN asset.asset_analytic aa on a.id = aa.asset_id
      WHERE
        aa.business_datetime >= select_times_assets_with_analytics.business_datetime
      GROUP BY
        ta2.signal_asset_id,
        a.name,
        a.ticker
    ),
    futures as (
      SELECT
        ta3.future_asset_id,
        a.name as future_name,
        a.ticker as future_ticker,
        array_agg((aa.category, aa.business_datetime, aa.value)::asset.category_datetime_value) as future_asset_analytics
      FROM
        times_assets ta3
        JOIN asset.asset a on ta3.future_asset_id = a.id
        JOIN asset.asset_analytic aa on a.id = aa.asset_id
      WHERE
        aa.business_datetime >= select_times_assets_with_analytics.business_datetime
      GROUP BY
        ta3.future_asset_id,
        a.name,
        a.ticker
    )
    SELECT
      ta4.cost,
      ta4.s_leverage,
      f.future_name,
      f.future_ticker,
      f.future_asset_analytics,
      s.signal_name,
      s.signal_ticker,
      s.signal_asset_analytics
    FROM
      times_assets ta4
      JOIN futures f on ta4.future_asset_id = f.future_asset_id
      JOIN signals s on ta4.signal_asset_id = s.signal_asset_id
  ;
END
$$;