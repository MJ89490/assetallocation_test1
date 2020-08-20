CREATE OR REPLACE FUNCTION asset.insert_assets_into_asset(
  execution_state_id int,
  assets asset.generic_asset[]
)
  RETURNS TABLE (id int)
AS
$$
BEGIN
  RETURN QUERY
    INSERT INTO asset.asset (
      category,
      country_id,
      currency_id,
      description,
      name,
      ticker,
      is_tr,
      type,
      execution_state_id
    )
    SELECT
      (ga).category,
      co.id,
      cu.id,
      (ga).description,
      (ga).name,
      (ga).ticker,
      (ga).is_tr,
      (ga).type,
      insert_assets_into_asset.execution_state_id
    FROM
      unnest(insert_assets_into_asset.assets) as ga
      JOIN lookup.currency cu on (ga).currency = cu.currency
      JOIN lookup.country co on (ga).country = co.country
    ON CONFLICT (ticker) DO UPDATE
      SET
        category = EXCLUDED.category,
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
    RETURNING asset.asset.id
  ;
END;
$$
LANGUAGE plpgsql;