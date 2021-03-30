DROP FUNCTION arp.select_times_assets(integer);
CREATE OR REPLACE FUNCTION arp.select_times_assets(
  strategy_version int
)
RETURNS TABLE(
    asset_subcategory text,
    future_ticker text,
    signal_ticker text,
    cost numeric(32, 16),
    s_leverage integer
  )
LANGUAGE plpgsql
AS
$$
BEGIN
  return query
    SELECT
      string_agg(ag.subcategory, '') FILTER (WHERE sa.name = 'future') as asset_subcategory,
      string_agg(a.ticker, '') FILTER (WHERE sa.name = 'future') as future_ticker,
      string_agg(a.ticker, '') FILTER (WHERE sa.name = 'signal') as signal_ticker,
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
  ;
END
$$;
