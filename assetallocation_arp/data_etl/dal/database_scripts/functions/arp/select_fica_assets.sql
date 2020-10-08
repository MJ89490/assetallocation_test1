CREATE OR REPLACE FUNCTION arp.select_fica_assets(
  strategy_version int
)
RETURNS TABLE(
    asset_ticker varchar,
    sovereign_ticker curve.ticker_months_years,
    swap_ticker curve.ticker_months_years,
    swap_cr_ticker curve.ticker_months_years
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
      (t1.category, t1.mth3, t1.yr1, t1.yr2, t1.yr3, t1.yr4, t1.yr5, t1.yr6, t1.yr7, t1.yr8, t1.yr9, t1.yr10, t1.yr15, t1.yr20, t1.yr30):: curve.ticker_months_years as sovereign_ticker,
      (t2.category, t2.mth3, t2.yr1, t2.yr2, t2.yr3, t2.yr4, t2.yr5, t2.yr6, t2.yr7, t2.yr8, t2.yr9, t2.yr10, t2.yr15, t2.yr20, t2.yr30):: curve.ticker_months_years as swap_ticker,
      (t3.category, t3.mth3, t3.yr1, t3.yr2, t3.yr3, t3.yr4, t3.yr5, t3.yr6, t3.yr7, t3.yr8, t3.yr9, t3.yr10, t3.yr15, t3.yr20, t3.yr30):: curve.ticker_months_years as swap_cr_ticker
    FROM
      arp.fica_asset fa
      JOIN asset.asset a on fa.asset_id = a.id
      JOIN curve.ticker t1 on fa.sovereign_ticker_id = t1.id
      JOIN curve.ticker t2 on fa.swap_ticker_id = t2.id
      JOIN curve.ticker t3 on fa.swap_cr_ticker_id = t3.id
      JOIN arp.fica f on fa.strategy_id = f.strategy_id
      JOIN arp.strategy s on f.strategy_id = s.id
    WHERE
      s.name = strategy_name
      AND f.version = strategy_version
  ;
END
$$;
