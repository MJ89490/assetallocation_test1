DROP FUNCTION arp.insert_strategy_asset(integer,integer,character varying,character varying);
CREATE OR REPLACE FUNCTION arp.insert_strategy_asset(
  strategy_asset_group_id int,
  execution_state_id int,
  strategy_asset_name varchar,
  asset_ticker varchar
)
  RETURNS VOID
language plpgsql
as
$$
BEGIN
  INSERT INTO
    arp.strategy_asset (strategy_asset_group_id, execution_state_id, asset_id, name)
  SELECT
    strategy_asset_group_id,
    insert_strategy_asset.execution_state_id,
    a.id,
    strategy_asset_name
  FROM
    asset.asset a
  WHERE
    a.ticker = asset_ticker
  ;
END
$$