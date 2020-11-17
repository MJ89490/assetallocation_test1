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
  _times_assets arp.asset_ticker_ticker_cost_leverage[];
BEGIN
  strategy_name := 'times';
  _times_assets := times_assets::arp.asset_ticker_ticker_cost_leverage[];

  SELECT config.insert_execution_state('arp.insert_times_assets') INTO execution_state_id;
  SELECT arp.select_strategy_id(strategy_name, times_version) INTO strategy_id;
  PERFORM arp.delete_times_assets_from_times_asset(strategy_id);
  PERFORM arp.insert_times_assets_into_times_asset(strategy_id, execution_state_id, _times_assets);
END;
$$
LANGUAGE plpgsql;

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

CREATE OR REPLACE FUNCTION arp.insert_times_assets_into_times_asset(
  strategy_id int,
  execution_state_id int,
  times_assets arp.asset_ticker_ticker_cost_leverage[]
)
RETURNS void
AS
$$
BEGIN
  INSERT INTO arp.times_asset(
    strategy_id,
    signal_asset_id,
    future_asset_id,
    asset_subcategory,
    s_leverage,
    cost,
    execution_state_id
  )
  SELECT
    strategy_id,
    a1.id,
    a2.id,
    (ta).asset_subcategory,
    (ta).s_leverage,
    (ta).cost,
    insert_times_assets_into_times_asset.execution_state_id
  FROM
    unnest(times_assets) as ta
    JOIN asset.asset a1 ON (ta).signal_ticker = a1.ticker
    JOIN asset.asset a2 ON (ta).future_ticker = a2.ticker
;
END;
$$
LANGUAGE plpgsql;
