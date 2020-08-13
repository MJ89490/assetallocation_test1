CREATE OR REPLACE FUNCTION arp.insert_times_assets_ids_into_times_asset(
  strategy_id int,
  execution_state_id int,
  asset_ids int[]
)
RETURNS void
AS
$$
BEGIN
  INSERT INTO arp.times_asset (strategy_id, asset_id, execution_state_id)
  SELECT strategy_id, a.id, execution_state_id
  FROM unnest(asset_ids) as a(id);
END;
$$
LANGUAGE plpgsql;