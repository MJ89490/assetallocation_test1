DROP FUNCTION arp.select_effect_assets(integer);
CREATE OR REPLACE FUNCTION arp.select_effect_assets(
  strategy_version int
)
RETURNS TABLE(
    asset_subcategory text,
    ticker_3m text,
    spot_ticker text,
    carry_ticker text,
    currency varchar,
    usd_weight numeric(32,16),
    base varchar,
    region varchar
  )
LANGUAGE plpgsql
AS
$$
BEGIN
  return query
    SELECT
      string_agg(ag.subcategory, '') FILTER (WHERE sa.name = 'future') as asset_subcategory,
      string_agg(a.ticker, '') FILTER (WHERE sa.name = '3m') as ticker_3m,
      string_agg(a.ticker, '') FILTER (WHERE sa.name = 'spot') as spot_ticker,
      string_agg(a.ticker, '') FILTER (WHERE sa.name = 'carry') as carry_ticker,
      eag.currency,
      eag.usd_weight,
      eag.base,
      eag.region
    FROM
      arp.effect e
      JOIN arp.strategy_asset_group sag ON e.strategy_id = sag.strategy_id
      JOIN arp.effect_asset_group eag ON sag.id = eag.strategy_asset_group_id
      JOIN arp.strategy_asset sa ON sag.id = sa.strategy_asset_group_id
      JOIN asset.asset a ON sa.asset_id = a.id
      JOIN asset.asset_group ag ON a.asset_group_id = ag.id
    WHERE
      e.version = strategy_version
    GROUP BY
      eag.currency,
      eag.usd_weight,
      eag.base,
      eag.region
  ;
END
$$;
