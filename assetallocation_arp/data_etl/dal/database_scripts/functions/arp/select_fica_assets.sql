CREATE OR REPLACE FUNCTION arp.select_fica_assets(
  strategy_version int
)
RETURNS TABLE(
    asset_subcategory varchar,
    asset_ticker varchar,
    fica_asset_category varchar,
    curve_tenor varchar
  )
LANGUAGE plpgsql
AS
$$
BEGIN
  return query
    SELECT
      fag.asset_subcategory,
      a.ticker as asset_ticker,
      fa.category as fica_asset_category,
      fa.curve_tenor
    FROM
      arp.fica_asset fa
      JOIN asset.asset a on fa.asset_id = a.id
      JOIN arp.fica_asset_group fag on fa.fica_asset_group_id = fag.id
      JOIN arp.fica f on fag.strategy_id = f.strategy_id
    WHERE
      f.version = strategy_version
  ;
END
$$;
