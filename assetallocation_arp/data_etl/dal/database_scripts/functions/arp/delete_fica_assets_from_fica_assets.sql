CREATE OR REPLACE FUNCTION arp.delete_fica_assets_from_fica_asset(
  strategy_id int
)
  RETURNS VOID
AS
$$
BEGIN
  DELETE FROM arp.fica_asset fa WHERE fa.strategy_id = delete_fica_assets_from_fica_asset.strategy_id;
END;
$$
LANGUAGE plpgsql;


