CREATE OR REPLACE FUNCTION arp.select_times_assets_with_analytics(
  strategy_version int,
  business_tstzrange tstzrange
)
  RETURNS TABLE(
    asset_subcategory varchar,
    cost numeric(32, 16),
    s_leverage integer,
    future_ticker varchar,
    future_asset_analytics asset.category_datetime_value[],
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
      string_agg(a.id, '') FILTER (WHERE sa.name = 'future') as future_asset_id,
      string_agg(a.id, '') FILTER (WHERE sa.name = 'signal') as signal_asset_id,
      string_agg(ag.subcategory, '') FILTER (WHERE sa.name = 'future') as asset_subcategory,
      tag.cost,
      tag.s_leverage
    FROM
      arp.times t
      JOIN arp.strategy_asset_group sag ON t.strategy_id = sag.strategy_id
      JOIN arp.times_asset_group tag ON sag.id = tag.strategy_asset_group_id
      JOIN arp.strategy_asset sa ON sag.id = sa.strategy_asset_group_id
      JOIN asset.asset a ON sa.asset_id = a.id
      JOIN asset.asset_group ag ON a.asset_group_id = ag.id
    WHERE
      t.version = strategy_version
      AND sa.name in ('future', 'signal')
    GROUP BY
      tag.strategy_asset_group_id,
      tag.cost,
      tag.s_leverage
    ),
    signals as (
      SELECT
        ta2.signal_asset_id,
        a.ticker as signal_ticker,
        array_agg((aa.category, aa.business_datetime, aa.value)::asset.category_datetime_value) as signal_asset_analytics
      FROM
        times_assets ta2
        JOIN asset.asset a on ta2.signal_asset_id = a.id
        JOIN asset.asset_analytic aa on a.id = aa.asset_id
      WHERE
        aa.business_datetime <@ select_times_assets_with_analytics.business_tstzrange
      GROUP BY
        ta2.signal_asset_id,
        a.ticker
    ),
    futures as (
      SELECT
        ta3.future_asset_id,
        a.ticker as future_ticker,
        array_agg((aa.category, aa.business_datetime, aa.value)::asset.category_datetime_value) as future_asset_analytics
      FROM
        times_assets ta3
        JOIN asset.asset a on ta3.future_asset_id = a.id
        JOIN asset.asset_analytic aa on a.id = aa.asset_id
      WHERE
        aa.business_datetime <@ select_times_assets_with_analytics.business_tstzrange
      GROUP BY
        ta3.future_asset_id,
        a.ticker
    )
    SELECT
      ta4.asset_subcategory,
      ta4.cost,
      ta4.s_leverage,
      f.future_ticker,
      f.future_asset_analytics,
      s.signal_ticker,
      s.signal_asset_analytics
    FROM
      times_assets ta4
      JOIN futures f on ta4.future_asset_id = f.future_asset_id
      JOIN signals s on ta4.signal_asset_id = s.signal_asset_id
  ;
END
$$;