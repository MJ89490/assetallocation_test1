CREATE OR REPLACE FUNCTION arp.select_times_assets(
  strategy_version int
)
RETURNS TABLE(
    asset_subcategory varchar,
    future_ticker varchar,
    signal_ticker varchar,
    cost numeric(32, 16),
    s_leverage integer
  )
LANGUAGE plpgsql
AS
$$
BEGIN
  return query
    SELECT
      ta.asset_subcategory,
      a1.ticker as future_ticker,
      a2.ticker as signal_ticker,
      ta.cost,
      ta.s_leverage
    FROM
      arp.times_asset ta
      JOIN asset.asset a1 on ta.future_asset_id = a1.id
      JOIN asset.asset a2 on ta.signal_asset_id = a2.id
      JOIN arp.times t on ta.strategy_id = t.strategy_id
    WHERE
      t.version = strategy_version
    GROUP BY a1.id, a2.id
  ;
END
$$;
