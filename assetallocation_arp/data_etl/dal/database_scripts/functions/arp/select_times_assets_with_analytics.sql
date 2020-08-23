CREATE OR REPLACE FUNCTION arp.select_times_assets_with_analytics(
  strategy_version int,
  business_datetime timestamp with time zone
)
  RETURNS TABLE(
    future_name varchar,
    future_ticker varchar,
    signal_name varchar,
    signal_ticker varchar,
    cost numeric(32, 16),
    s_leverage integer,
    future_asset_analytics arp.category_datetime_value[],
    signal_asset_analytics arp.category_datetime_value[]
  )
LANGUAGE plpgsql
AS
$$
DECLARE
  strategy_name varchar;
BEGIN
  strategy_name := 'times';

  return query
    SELECT
      a1.name as future_name,
      a1.ticker as future_ticker,
      a2.name as signal_name,
      a2.ticker as signal_ticker,
      ta.cost,
      ta.s_leverage,
      array_agg((aa1.category, aa1.business_datetime, aa1.value)::arp.category_datetime_value) as future_asset_analytics,
      array_agg((aa2.category, aa2.business_datetime, aa2.value)::arp.category_datetime_value) as signal_asset_analytics
    FROM
      arp.times_asset ta
      JOIN asset.asset a1 on ta.future_asset_id = a1.id
      JOIN asset.asset a2 on ta.signal_asset_id = a2.id
      JOIN arp.times t on ta.strategy_id = t.strategy_id
      JOIN arp.strategy s on t.strategy_id = s.id
      JOIN asset.asset_analytic aa1 on a1.id = aa1.asset_id
      JOIN asset.asset_analytic aa2 on a2.id = aa2.asset_id
    WHERE
      s.name = strategy_name
      AND t.version = strategy_version
      AND aa1.business_datetime >= select_times_assets_with_analytics.business_datetime
      AND aa2.business_datetime >= select_times_assets_with_analytics.business_datetime
    GROUP BY a1.id, a2.id, ta.cost, ta.s_leverage
  ;
END
$$;