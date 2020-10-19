CREATE OR REPLACE FUNCTION arp.select_fica_assets(
  strategy_version int
)
RETURNS TABLE(
    asset_ticker varchar,
    fica_asset_category varchar,
    curve_tenor varchar
  )
LANGUAGE plpgsql
AS
$$
DECLARE
  strategy_name varchar;
BEGIN
  strategy_name := 'fica';

  return query
    SELECT
      a.ticker as asset_ticker,
      fa.category as fica_asset_category,
      fa.curve_tenor
    FROM
      arp.fica_asset fa
      JOIN asset.asset a on fa.asset_id = a.id
      JOIN arp.fica f on fa.strategy_id = f.strategy_id
      JOIN arp.strategy s on f.strategy_id = s.id
    WHERE
      s.name = strategy_name
      AND f.version = strategy_version
  ;
END
$$;
