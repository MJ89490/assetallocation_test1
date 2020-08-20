CREATE OR REPLACE FUNCTION arp.insert_times_assets(
  times_version int,
  times_assets text[]
)
RETURNS VOID
AS
$$
DECLARE
  execution_state_id int;
  strategy_name varchar;
  strategy_id int;
  _times_assets arp.ticker_ticker_cost_leverage[];
BEGIN
  strategy_name := 'times';
  _times_assets := times_assets::arp.ticker_ticker_cost_leverage[];

  SELECT config.insert_execution_state('arp.insert_times_assets') INTO execution_state_id;
  SELECT arp.select_strategy_id(strategy_name, times_version) INTO strategy_id;
  PERFORM arp.delete_times_assets_from_times_asset(strategy_id);
  PERFORM arp.insert_times_assets_into_times_asset(strategy_id, execution_state_id, _times_assets);
END;
$$
LANGUAGE plpgsql;