CREATE OR REPLACE FUNCTION arp.select_times_assets(
  strategy_version int
)
RETURNS TABLE(
    future_name varchar,
    future_ticker varchar,
    signal_name varchar,
    signal_ticker varchar,
    cost numeric(32, 16),
    s_leverage integer
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
      ta.s_leverage
    FROM
      arp.times_asset ta
      JOIN asset.asset a1 on ta.future_asset_id = a1.id
      JOIN asset.asset a2 on ta.signal_asset_id = a2.id
      JOIN arp.times t on ta.strategy_id = t.strategy_id
      JOIN arp.strategy s on t.strategy_id = s.id
    WHERE
      s.name = strategy_name
      AND t.version = strategy_version
    GROUP BY a1.id, a2.id
  ;
END
$$;
