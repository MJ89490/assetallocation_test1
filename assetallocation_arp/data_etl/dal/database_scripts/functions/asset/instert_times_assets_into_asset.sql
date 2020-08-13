CREATE OR REPLACE FUNCTION arp.insert_times_assets_into_asset(
  execution_state_id int,
  times_assets [],
  OUT asset_ids SETOF int
)
AS
$$
BEGIN

  INSERT INTO asset.asset (
    category,
    country_id,
    currency_id,
    description,
    name,
    ticker,
    is_tr,
    type,
    signal_ticker,
    future_ticker,
    cost,
    s_leverage,
    execution_state_id
  )
  SELECT
    (ta).category,
    co.id,
    cu.id,
    (ta).description,
    (ta).name,
    (ta).ticker,
    (ta).is_tr,
    (ta).type,
    (ta).signal_ticker,
    (ta).future_ticker,
    (ta).cost,
    (ta).s_leverage,
    arp.insert_times_assets.execution_state_id
  FROM
    unnest(insert_times_asset.times_assets) as ta
    JOIN lookup.currency cu on (ta).currency = cu.currency
    JOIN lookup.country co on (ta).country = co.country
  ON CONFLICT (ticker) DO UPDATE
    SET
      category = excluded.category,
      country_id = EXCLUDED.country_id,
      currency_id = EXCLUDED.currency_id,
      description = EXCLUDED.description,
      name = EXCLUDED.name,
      is_tr = EXCLUDED.is_tr,
      type = EXCLUDED.type,
      signal_ticker = EXCLUDED.signal_ticker,
      future_ticker = EXCLUDED.future_ticker,
      cost = EXCLUDED.cost,
      s_leverage = EXCLUDED.s_leverage
  RETURNING (asset.asset.id)
  ;
END;
$$
LANGUAGE plpgsql;