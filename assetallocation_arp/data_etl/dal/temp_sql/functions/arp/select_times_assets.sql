CREATE OR REPLACE FUNCTION arp.select_times_assets(
  strategy_name varchar,
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
    analytic_type varchar,
    value numeric(32, 16),
    source varchar
  )
LANGUAGE plpgsql
AS
$$
BEGIN
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
      aa.type as analytic_type,
      aa.value,
      s2.source
    INTO asset_row_set
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
      AND aa.business_tstzrange @> business_datetime;
END
$$;