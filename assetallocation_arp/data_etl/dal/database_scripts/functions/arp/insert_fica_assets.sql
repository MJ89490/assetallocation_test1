CREATE OR REPLACE FUNCTION arp.insert_fica_assets(
  fica_version int,
  asset_tickers varchar[],
  categories varchar[] ,
  curve_tenors varchar[]
)
RETURNS VOID
AS
$$
DECLARE
  execution_state_id int;
  strategy_name varchar;
  strategy_id int;
BEGIN
  strategy_name := 'fica';

  SELECT config.insert_execution_state('arp.insert_fica_assets') INTO execution_state_id;
  SELECT arp.select_strategy_id(strategy_name, fica_version) INTO strategy_id;
  PERFORM arp.delete_fica_assets_from_fica_asset(strategy_id);
  PERFORM arp.insert_fica_assets_into_fica_asset(strategy_id, execution_state_id, asset_tickers,
    categories, curve_tenors);
END;
$$
LANGUAGE plpgsql;