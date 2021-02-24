/* Load asset data from staging.asset into asset.asset_group and asset.asset
asset.asset has fkey linked to asset.asset_group
Hence insertion order is required to be asset.asset_group then asset.asset
Delete any records from staging.asset that were inserted into asset.asset
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
  SELECT INTO _staging_asset_ids staging.load_assets_from_asset(_execution_state_id);
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
    __execution_state_id INT
)
  RETURNS VOID
LANGUAGE plpgsql
AS
$$
BEGIN
  INSERT INTO asset.asset_group (category, subcategory, execution_state_id)
  SELECT DISTINCT sa.asset_category, sa.asset_subcategory, __execution_state_id
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
  __execution_state_id INT,
  OUT staging_asset_ids INT[]
)
LANGUAGE plpgsql
AS
$$
BEGIN
  WITH ins_rows as (
    SELECT DISTINCT
    sa.name,
    sa.description,
    lcu.id as currency_id,
    lco.id as country_id,
    aag.id as asset_group_id,
    sa.ticker,
    sa.id as staging_asset_id
  FROM staging.asset sa
  JOIN lookup.currency lcu ON sa.currency = lcu.currency
  JOIN lookup.country lco ON sa.country = lco.country
  JOIN asset.asset_group aag ON sa.asset_category = aag.category
    AND sa.asset_subcategory = aag.subcategory
  ),
  ins as (
    INSERT INTO asset.asset (name, description, currency_id, country_id, execution_state_id, asset_group_id, ticker)
    SELECT DISTINCT
      ir.name,
      ir.description,
      ir.currency_id,
      ir.country_id,
      __execution_state_id,
      ir.asset_group_id,
      ir.ticker
    FROM ins_rows ir
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
    )
    SELECT array_agg(ir.staging_asset_id) FROM ins_rows ir INTO staging_asset_ids
  ;
END
$$;

