CREATE OR REPLACE FUNCTION arp.delete_times_assets_from_times_asset(
  strategy_id int
)
  RETURNS VOID
AS
$$
BEGIN
  DELETE FROM arp.times_asset ta WHERE ta.strategy_id = delete_times_assets_from_times_asset.strategy_id;
END;
$$
LANGUAGE plpgsql;


