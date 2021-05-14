/* Load asset data from staging.asset_analytic into asset.asset_analytic
Delete any records from staging.asset that were inserted into asset.asset_analytic
*/
CREATE OR REPLACE FUNCTION staging.load_asset_analytics()
  RETURNS VOID
LANGUAGE plpgsql
AS
$$
DECLARE
  _execution_state_id INT;
  _staging_asset_analytic_ids INT[];
BEGIN
  SELECT INTO _execution_state_id config.insert_execution_state('staging.load_asset_analytics');
  SELECT INTO _staging_asset_analytic_ids staging.load_asset_analytics_from_asset_analytic(_execution_state_id);
  DELETE FROM staging.asset_analytic sas where sas.id = ANY (SELECT unnest(_staging_asset_analytic_ids));
END
$$;


/* Load asset data from staging.asset_analytic into asset.asset_analytic
trigger before_insert_close_off_old_record will fire on insertion of row

WHEN inserting a row from staging.asset_analytic
GIVEN there already exists a row where
  system_tstzrange  = 'infinity'
  asset_id, business_datetime, category, value equal to inserting row
THEN do not insert this row

Return ids from staging.asset_analytic of rows inserted
*/
CREATE OR REPLACE FUNCTION staging.load_asset_analytics_from_asset_analytic(
  _execution_state_id INT,
  OUT staging_asset_analytic_ids INT[]
)
LANGUAGE plpgsql
AS
$$
BEGIN
  with ins_rows as (
    SELECT
    saa.analytic_category,
    aa.id  as asset_id,
    saa.value,
    ls.id  as source_id,
    saa.business_datetime,
    load_asset_analytics_from_asset_analytic._execution_state_id,
    saa.id as staging_asset_analytic_id
    FROM staging.asset_analytic saa
    JOIN asset.asset aa on saa.ticker = aa.ticker
    JOIN lookup.source ls on saa.source = ls.source
  ),
  ins as (
    INSERT INTO asset.asset_analytic (category, asset_id, value, source_id, business_datetime, execution_state_id)
    SELECT DISTINCT
      ir.analytic_category,
      ir.asset_id,
      ir.value,
      ir.source_id,
      ir.business_datetime,
      load_asset_analytics_from_asset_analytic._execution_state_id
    FROM ins_rows ir
    ON CONFLICT (asset_id, business_datetime, category) WHERE upper(system_tstzrange) = 'infinity'
    DO NOTHING
  )
  SELECT array_agg(ir.staging_asset_analytic_id) FROM ins_rows ir INTO staging_asset_analytic_ids
  ;
END
$$;