DROP FUNCTION arp.select_fica_assets(integer);
CREATE OR REPLACE FUNCTION arp.select_fica_assets(
  strategy_version int
)
RETURNS TABLE(
    asset_subcategory varchar,
    asset_ticker text,
    fica_asset_name text
  )
LANGUAGE plpgsql
AS
$$
BEGIN
  return query
  SELECT
    string_agg(ag.subcategory, '') FILTER (WHERE sa.name = concat('yr', f.tenor, '_', f.curve)) as asset_subcategory,
    a.ticker as asset_ticker,
    sa.name as fica_asset_name
  FROM
    arp.fica f
    JOIN arp.strategy_asset_group sag ON f.strategy_id = sag.strategy_id
    JOIN arp.strategy_asset sa ON sag.id = sa.strategy_asset_group_id
    JOIN asset.asset a ON sa.asset_id = a.id
    JOIN asset.asset_group ag ON a.asset_group_id = ag.id
  WHERE
    f.version = strategy_version
  GROUP BY
    sa.strategy_asset_group_id,
    a.ticker,
    sa.name
  ;
END
$$;


--Fica  – a bit more complicated: there are two inputs (tenor and curve that determines it)
-- so if tenor=10 and curve=swap, we would link to swap_ticker_10