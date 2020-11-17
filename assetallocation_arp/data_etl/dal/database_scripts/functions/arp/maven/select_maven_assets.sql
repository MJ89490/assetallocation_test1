CREATE OR REPLACE FUNCTION arp.select_maven_assets(
  strategy_version int
)
RETURNS TABLE(
    bbg_tr_ticker integer,
    bbg_er_ticker integer,
    cash_ticker integer,
    asset_category varchar,
    asset_subcategory varchar,
    currency varchar,
    is_excess boolean,
    asset_weight numeric,
    transaction_cost numeric
)
LANGUAGE plpgsql
AS
$$
BEGIN
  return query
    SELECT
      ma.asset_subcategory,
      a1.ticker as bbg_tr_ticker,
      a2.ticker as bbg_er_ticker,
      a3.ticker as cash_ticker,
      asset_category,
      asset_subcategory,
      currency,
      is_excess,
      asset_weight,
      transaction_cost
    FROM
      arp.maven_asset ma
      JOIN asset.asset a1 on ma.bbg_tr_asset_id = a1.id
      JOIN asset.asset a2 on ma.bbg_er_asset_id = a2.id
      JOIN asset.asset a3 on ma.cash_asset_id = a3.id
      JOIN arp.maven m on ma.strategy_id = m.strategy_id
    WHERE
      m.version = strategy_version
    GROUP BY a1.id, a2.id, a3.id
  ;
END
$$;
