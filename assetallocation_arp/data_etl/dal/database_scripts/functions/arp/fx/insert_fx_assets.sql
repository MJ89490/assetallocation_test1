CREATE OR REPLACE FUNCTION arp.insert_fx_assets(
  fx_version int,
  fx_assets text[]
)
RETURNS VOID
AS
$$
DECLARE
  execution_state_id int;
  strategy_name varchar;
  strategy_id int;
  _fx_assets arp.ticker_ticker_currency[];
BEGIN
  strategy_name := 'fx';
  _fx_assets := fx_assets::arp.ticker_ticker_currency[];

  SELECT config.insert_execution_state('arp.insert_fx_assets') INTO execution_state_id;
  SELECT arp.select_strategy_id(strategy_name, fx_version) INTO strategy_id;
  PERFORM arp.delete_fx_assets_from_fx_asset(strategy_id);
  PERFORM arp.insert_fx_assets_into_fx_asset(strategy_id, execution_state_id, _fx_assets);
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION arp.delete_fx_assets_from_fx_asset(
  strategy_id int
)
  RETURNS VOID
AS
$$
BEGIN
  DELETE FROM arp.fx_asset ta WHERE ta.strategy_id = delete_fx_assets_from_fx_asset.strategy_id;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION arp.insert_fx_assets_into_fx_asset(
  strategy_id int,
  execution_state_id int,
  fx_assets arp.ticker_ticker_currency[]
)
RETURNS void
AS
$$
BEGIN
  INSERT INTO arp.fx_asset(
    strategy_id,
    ppp_asset_id,
    cash_rate_asset_id,
    currency,
    execution_state_id
  )
  SELECT
    strategy_id,
    a1.id,
    a2.id,
    (fa).currency,
    insert_fx_assets_into_fx_asset.execution_state_id
  FROM
    unnest(fx_assets) as fa
    JOIN asset.asset a1 ON (fa).ppp_ticker = a1.ticker
    JOIN asset.asset a2 ON (fa).cash_rate_ticker = a2.ticker
;
END;
$$
LANGUAGE plpgsql;
