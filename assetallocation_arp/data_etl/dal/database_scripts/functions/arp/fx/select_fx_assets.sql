CREATE OR REPLACE FUNCTION arp.select_fx_assets(
  strategy_version int
)
RETURNS TABLE(
  ppp_ticker text,
  cash_ticker text,
  currency text
  )
LANGUAGE plpgsql
AS
$$
BEGIN
  return query
    SELECT
      string_agg(a.ticker, '') FILTER (WHERE sa.name = 'ppp') as ppp_ticker,
      string_agg(a.ticker, '') FILTER (WHERE sa.name = 'cash') as cash_ticker,
      c.currency
     FROM
      arp.fx f
      JOIN arp.strategy_asset_group sag ON f.strategy_id = sag.strategy_id
      JOIN arp.fx_asset_group fag ON sag.id = fag.strategy_asset_group_id
      JOIN lookup.currency c on fag.currency_id = c.id
      JOIN arp.strategy_asset sa ON sag.id = sa.strategy_asset_group_id
      JOIN asset.asset a ON sa.asset_id = a.id
    WHERE
      f.version = strategy_version
    GROUP BY
      fag.strategy_asset_group_id,
      c.currency
  ;
END
$$;
