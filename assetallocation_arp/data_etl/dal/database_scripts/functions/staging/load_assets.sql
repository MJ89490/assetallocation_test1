/* Load asset data from staging.asset into asset.asset_group, asset.asset and asset.asset_analytic
asset.asset_analytic has fkey linked to asset.asset
asset.asset has fkey linked to asset.asset_group
Hence insertion order is required to be asset.asset_group then asset.asset then asset.asset_analytic
Delete any records from staging.asset that were inserted into asset.asset_analytic
*/
CREATE OR REPLACE FUNCTION staging.load_assets()
  RETURNS VOID
LANGUAGE plpgsql
AS
$$
DECLARE
  _execution_state_id INT;
  _staging_asset_ids INT[];
BEGIN
  SELECT INTO _execution_state_id config.insert_execution_state('staging.load_assets');
  PERFORM staging.load_asset_groups_from_asset(_execution_state_id);
  PERFORM staging.load_assets_from_asset(_execution_state_id);
  SELECT INTO _staging_asset_ids staging.load_asset_analytics_from_asset(_execution_state_id);
  DELETE FROM staging.asset sa where sa.id = ANY(SELECT unnest(_staging_asset_ids));
END
$$;


/* Load asset data from staging.asset into asset.group
WHEN inserting a row from staging.asset
GIVEN there already exists a row where
  category, subcategory equal to inserting row
THEN do not insert this row
*/
CREATE OR REPLACE FUNCTION staging.load_asset_groups_from_asset(
    _execution_state_id INT
)
  RETURNS VOID
LANGUAGE plpgsql
AS
$$
BEGIN
  INSERT INTO asset.asset_group (category, subcategory, execution_state_id)
  SELECT DISTINCT sa.asset_category, sa.asset_subcategory, _execution_state_id
  FROM staging.asset sa
  ON CONFLICT DO NOTHING
  ;
END
$$;


/* Load asset data from staging.asset into asset.asset
WHEN inserting a row from staging.asset
GIVEN there already exists a row where
  ticker equal to inserting row
  any of (name, description, currency_id, country_id, asset_group_id) not equal to inserting row
THEN update existing row
  set name, description, currency_id, country_id, asset_group_id, execution_state_id to inserting row values
*/
CREATE OR REPLACE FUNCTION staging.load_assets_from_asset(
  _execution_state_id INT
)
  RETURNS VOID
LANGUAGE plpgsql
AS
$$
BEGIN
  INSERT INTO asset.asset (name, description, currency_id, country_id, execution_state_id, asset_group_id, ticker)
  SELECT DISTINCT
    sa.name,
    sa.description,
    lcu.id as currency_id,
    lco.id as country_id,
    _execution_state_id,
    aag.id as asset_group_id,
    sa.ticker
  FROM staging.asset sa
  JOIN lookup.currency lcu ON sa.currency = lcu.currency
  JOIN lookup.country lco ON sa.country = lco.country
  JOIN asset.asset_group aag ON sa.asset_category = aag.category
    AND sa.asset_subcategory = aag.subcategory
  ON CONFLICT ON CONSTRAINT asset_ticker_key DO UPDATE
    SET
      name = EXCLUDED.name,
      description = EXCLUDED.description,
      currency_id = EXCLUDED.currency_id,
      country_id = EXCLUDED.country_id,
      execution_state_id = EXCLUDED.execution_state_id,
      asset_group_id = EXCLUDED.asset_group_id

    /* AVOID NET ZERO CHANGES */
    where exists
        (
        SELECT
          asset.asset.name,
          asset.asset.description,
          asset.asset.currency_id,
          asset.asset.country_id,
          asset.asset.asset_group_id
        EXCEPT
        SELECT
          EXCLUDED.name,
          EXCLUDED.description,
          EXCLUDED.currency_id,
          EXCLUDED.country_id,
          EXCLUDED.asset_group_id
        )
  ;
END
$$;

/* Load asset data from staging.asset into asset.asset_analytic
trigger before_insert_close_off_old_record will fire on insertion of row

WHEN inserting a row from staging.asset
GIVEN there already exists a row where
  system_tstzrange  = 'infinity'
  asset_id, business_datetime, category, value equal to inserting row
THEN do not insert this row

Return ids from staging.asset of rows inserted
*/
CREATE OR REPLACE FUNCTION staging.load_asset_analytics_from_asset(
  _execution_state_id INT,
  OUT staging_asset_ids INT[]
)
LANGUAGE plpgsql
AS
$$
BEGIN
  with ins_rows as (
    SELECT
    sa.analytic_category,
    aa.id as asset_id,
    sa.value,
    ls.id as source_id,
    sa.business_datetime,
    load_asset_analytics_from_asset._execution_state_id,
    sa.id as staging_asset_id
    FROM staging.asset sa
    JOIN asset.asset aa on sa.ticker = aa.ticker
    JOIN lookup.source ls on sa.source = ls.source
  ),
  ins as (
    INSERT INTO asset.asset_analytic (category, asset_id, value, source_id, business_datetime, execution_state_id)
    SELECT DISTINCT
      ir.analytic_category,
      ir.asset_id,
      ir.value,
      ir.source_id,
      ir.business_datetime,
      load_asset_analytics_from_asset._execution_state_id
    FROM ins_rows ir
    ON CONFLICT (asset_id, business_datetime, category) WHERE upper(system_tstzrange) = 'infinity'
    DO NOTHING
  )
  SELECT array_agg(ir.staging_asset_id) FROM ins_rows ir INTO staging_asset_ids
  ;
END
$$;
