CREATE OR REPLACE FUNCTION arp.select_times_assets_with_analytics(
  strategy_version int,
  business_datetime timestamp with time zone
)
  RETURNS TABLE(
    category varchar,
    cost numeric(32, 16),
    country char(2),
    currency char(3),
    description varchar,
    future_ticker varchar,
    name varchar,
    signal_ticker varchar,
    ticker varchar,
    is_tr boolean,
    asset_type varchar,
    s_leverage integer,
    asset_analytics arp.source_category_value[]
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
      a.category,
      a.cost,
      c2.country,
      c.currency,
      a.description,
      a.future_ticker,
      a.name,
      a.signal_ticker,
      a.ticker,
      a.is_tr,
      a.type as asset_type,
      a.s_leverage,
      array_agg((s2.source, aa.category, aa.value) :: arp.source_category_value) as asset_analytic
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