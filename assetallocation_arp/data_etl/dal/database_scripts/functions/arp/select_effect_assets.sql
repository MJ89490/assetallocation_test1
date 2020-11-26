CREATE OR REPLACE FUNCTION arp.select_effect_assets(
  strategy_version int
)
RETURNS TABLE(
  currency varchar,
  ticker_3m varchar,
  spot_ticker varchar,
  carry_ticker varchar,
  usd_weight numeric(32, 16),
  base varchar,
  region varchar
)
LANGUAGE plpgsql
AS
$$
BEGIN
  return query
    SELECT
      ea.currency,
      a_3m.ticker as ticker_3m,
      a_spot.ticker as spot_ticker,
      a_carry.ticker as carry_ticker,
      ea.usd_weight,
      ea.base,
      ea.region
    FROM
      arp.effect_asset ea
      JOIN asset.asset a_3m on ea.asset_3m_id = a_3m.id
      JOIN asset.asset a_spot on ea.spot_asset_id = a_spot.id
      JOIN asset.asset a_carry on ea.carry_asset_id = a_carry.id
      JOIN arp.effect e on ea.strategy_id = e.strategy_id
      JOIN arp.strategy s on e.strategy_id = s.id
    WHERE
      e.version = strategy_version
  ;
END
$$;
