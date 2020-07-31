CREATE OR REPLACE FUNCTION arp.select_times_assets(
  strategy_version int,
  business_datetime timestamp with time zone
)
  RETURNS TABLE(
    asset_class varchar,
    cost numeric(32, 16),
    country char(2),
    currency char(3),
    description varchar,
    future_ticker varchar,
    generic_yield_ticker varchar,
    name varchar,
    ndf_code varchar,
    s_leverage int,
    signal_ticker varchar,
    spot_code varchar,
    ticker varchar,
    tr_flag boolean,
    asset_type varchar,
    asset_analytic arp.source_type_value[]
  )
LANGUAGE plpgsql
AS
$$
DECLARE
  strategy_name varchar;
BEGIN
  strategy_name := 'times';

  return query
    SELECT
      a.asset_class,
      a.cost,
      c2.country,
      c.currency,
      a.description,
      a.future_ticker,
      a.generic_yield_ticker,
      a.name,
      a.ndf_code,
      a.s_leverage,
      a.signal_ticker,
      a.spot_code,
      a.ticker,
      a.tr_flag,
      a.type as asset_type,
      array_agg((s2.source, aa.type, aa.value) :: arp.source_type_value) as asset_analytic
    FROM
      asset.asset a
      JOIN arp.times_asset ta on a.id = ta.asset_id
      JOIN arp.times t on ta.strategy_id = t.strategy_id
      JOIN arp.strategy s on t.strategy_id = s.id
      JOIN lookup.currency c on a.currency_id = c.id
      JOIN lookup.country c2 on a.country_id = c2.id
      JOIN asset.asset_analytic aa on a.id = aa.asset_id
      JOIN lookup.source s2 on aa.source_id = s2.id
    WHERE
      s.name = strategy_name
      AND t.version = strategy_version
      AND aa.business_tstzrange @> business_datetime
    GROUP BY a.id, c.id, c2.id
  ;
END
$$;