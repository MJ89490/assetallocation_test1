CREATE OR REPLACE FUNCTION arp.select_fx_assets(
  strategy_version int
)
RETURNS TABLE(
    ppp_name varchar,
    ppp_ticker varchar,
    cash_rate_name varchar,
    cash_rate_ticker varchar,
    currency char(3)
  )
LANGUAGE plpgsql
AS
$$
BEGIN
  return query
    SELECT
      a1.name as ppp_name,
      a1.ticker as ppp_ticker,
      a2.name as cash_rate_name,
      a2.ticker as cash_rate_ticker,
      fa.currency
    FROM
      arp.fx_asset fa
      JOIN asset.asset a1 on fa.ppp_asset_id = a1.id
      JOIN asset.asset a2 on fa.cash_rate_asset_id = a2.id
      JOIN arp.fx f on fa.strategy_id = f.strategy_id
      JOIN arp.strategy s on f.strategy_id = s.id
    WHERE
      f.version = strategy_version
    GROUP BY a1.id, a2.id
  ;
END
$$;
