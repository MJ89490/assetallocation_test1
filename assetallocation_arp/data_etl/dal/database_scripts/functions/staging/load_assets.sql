CREATE OR REPLACE FUNCTION staging.load_assets()
  RETURNS VOID
LANGUAGE plpgsql
AS
$$
DECLARE
  _execution_state_id INT;
BEGIN
  SELECT INTO _execution_state_id config.insert_execution_state('staging.load_assets');
  PERFORM staging.load_asset_groups_from_asset(_execution_state_id);
  PERFORM staging.load_assets_from_asset(_execution_state_id);
  PERFORM staging.load_asset_analytics_from_asset(_execution_state_id);
END
$$;


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


CREATE OR REPLACE FUNCTION staging.load_assets_from_asset(
  _execution_state_id INT
)
  RETURNS VOID
LANGUAGE plpgsql
AS
$$
BEGIN
  INSERT INTO asset.asset (name, description, currency_id, country_id, execution_state_id, asset_group_id, is_tr, ticker)
  SELECT DISTINCT
    sa.name,
    sa.description,
    lcu.id as currency_id,
    lco.id as country_id,
    _execution_state_id,
    aag.id as asset_group_id,
    sa.is_tr,
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
      asset_group_id = EXCLUDED.asset_group_id,
      is_tr = EXCLUDED.is_tr

    /* AVOID NET ZERO CHANGES */
    where exists
        (
        SELECT
          asset.asset.name,
          asset.asset.description,
          asset.asset.currency_id,
          asset.asset.country_id,
          asset.asset.asset_group_id,
          asset.asset.is_tr
        EXCEPT
        SELECT
          EXCLUDED.name,
          EXCLUDED.description,
          EXCLUDED.currency_id,
          EXCLUDED.country_id,
          EXCLUDED.asset_group_id,
          EXCLUDED.is_tr
        )
  ;
END
$$;


CREATE OR REPLACE FUNCTION staging.load_asset_analytics_from_asset(
  _execution_state_id INT
)
  RETURNS VOID
LANGUAGE plpgsql
AS
$$
BEGIN
  INSERT INTO asset.asset_analytic (category, asset_id, value, source_id, business_datetime, execution_state_id)
  SELECT DISTINCT
    sa.analytic_category,
    aa.id,
    sa.value,
    ls.id,
    sa.business_datetime,
    _execution_state_id
  FROM staging.asset sa
  JOIN asset.asset aa on sa.ticker = aa.ticker
  JOIN lookup.source ls on sa.source = ls.source
  ON CONFLICT (asset_id, business_datetime, category) WHERE upper(system_tstzrange) = 'infinity'
  DO NOTHING
  ;
END
$$;
