CREATE OR REPLACE FUNCTION arp.select_effect_assets(
  strategy_version int
)
RETURNS TABLE(
    asset_name varchar,
    asset_ticker varchar,
    ndf_code varchar,
    spot_code varchar,
    position_size numeric(32, 16)
  )
LANGUAGE plpgsql
AS
$$
DECLARE
  strategy_name varchar;
BEGIN
  strategy_name := 'effect';

  return query
    SELECT
      a.name as asset_name,
      a.ticker as asset_ticker,
      ea.ndf_code,
      ea.spot_code,
      ea.position_size
    FROM
      arp.effect_asset ea
      JOIN asset.asset a on ea.future_asset_id = a.id
      JOIN arp.effect e on ea.strategy_id = e.strategy_id
      JOIN arp.strategy s on e.strategy_id = s.id
    WHERE
      s.name = strategy_name
      AND e.version = strategy_version
    GROUP BY a.id
  ;
END
$$;
