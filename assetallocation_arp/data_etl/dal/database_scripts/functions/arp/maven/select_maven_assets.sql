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
      string_agg(ag.subcategory, '') FILTER (
        WHERE sa.name = (
          CASE
            WHEN m.er_tr = 'excess' THEN 'bbg_er'
            ELSE 'bbg_tr'
          END
        )
      ) as asset_subcategory,
      string_agg(a.ticker, '') FILTER (WHERE sa.name = 'bbg_tr') as bbg_tr_ticker,
      string_agg(a.ticker, '') FILTER (WHERE sa.name = 'bbg_er') as bbg_er_ticker,
      string_agg(a.ticker, '') FILTER (WHERE sa.name = 'cash') as cash_ticker,
      c.currency,
      mag.is_excess,
      mag.asset_weight,
      mag.transaction_cost
     FROM
      arp.maven m
      JOIN arp.strategy_asset_group sag ON m.strategy_id = sag.strategy_id
      JOIN arp.maven_asset_group mag ON sag.id = mag.strategy_asset_group_id
      JOIN lookup.currency c on mag.currency_id = c.id
      JOIN arp.strategy_asset sa ON sag.id = sa.strategy_asset_group_id
      JOIN asset.asset a ON sa.asset_id = a.id
      JOIN asset.asset_group ag ON a.asset_group_id = ag.id
    WHERE
      m.version = strategy_version
    GROUP BY
      mag.strategy_asset_group_id,
      c.currency,
      mag.is_excess,
      mag.asset_weight,
      mag.transaction_cost
  ;
END
$$;
