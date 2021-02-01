CREATE OR REPLACE FUNCTION arp.insert_strategy_asset_group(
  strategy_id int,
	execution_state_id int,
	out strategy_asset_group_id int
)
language plpgsql
as
$$
BEGIN
INSERT INTO arp.strategy_asset_group (strategy_id, execution_state_id)
VALUES (
  strategy_id,
  execution_state_id
)
RETURNING arp.strategy_asset_group.id into strategy_asset_group_id;
return;
END
$$