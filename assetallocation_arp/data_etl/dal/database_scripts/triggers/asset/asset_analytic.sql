CREATE OR REPLACE FUNCTION asset.close_off_asset_analytic()
  RETURNS TRIGGER
   LANGUAGE PLPGSQL
AS $$
BEGIN
  UPDATE asset.asset_analytic aa
  SET
    system_tstzrange =  tstzrange(
    lower(aa.system_tstzrange),
    now(),
    '[)')
  WHERE
    aa.asset_id = NEW.asset_id
    AND aa.business_datetime = NEW.business_datetime
    AND aa.category = NEW.category
    AND aa.value != NEW.value
    AND upper(aa.system_tstzrange) = 'infinity'
  ;
  RETURN NEW;
END;
$$;

DROP trigger if exists before_insert_close_off_old_record on asset.asset_analytic;
CREATE TRIGGER before_insert_close_off_old_record
  BEFORE INSERT
  ON asset.asset_analytic
  FOR EACH ROW
    EXECUTE PROCEDURE asset.close_off_asset_analytic();
