CREATE OR REPLACE FUNCTION arp.insert_fica_assets(
  fica_version int,
  fica_assets text[]
)
RETURNS VOID
AS
$$
DECLARE
  execution_state_id int;
  strategy_name varchar;
  strategy_id int;
  _fica_assets arp.ticker_curves[];
  _sovereign_ticker_ids int[];
  _swap_ticker_ids int[];
  _swap_cr_ticker_ids int[];
BEGIN
  strategy_name := 'fica';
  _fica_assets := fica_assets::arp.ticker_curves[];

  SELECT config.insert_execution_state('arp.insert_fica_assets') INTO execution_state_id;
  SELECT arp.select_strategy_id(strategy_name, fica_version) INTO strategy_id;
  PERFORM arp.delete_fica_assets_from_fica_asset(strategy_id);
  SELECT curve.insert_tickers(execution_state_id, (Select (fa).sovereign_ticker from unnest(_fica_assets))) INTO _sovereign_ticker_ids;
  SELECT curve.insert_tickers(execution_state_id, (Select (fa).swap_ticker from unnest(_fica_assets))) INTO _swap_ticker_ids;
  SELECT curve.insert_tickers(execution_state_id, (Select (fa).swap_cr_ticker from unnest(_fica_assets))) INTO _swap_cr_ticker_ids;
  PERFORM arp.insert_fica_assets_into_fica_asset(strategy_id, execution_state_id,
                                                 (Select (fa).asset_ticker from unnest(_fica_assets)),
    _sovereign_ticker_ids, _swap_ticker_ids, _swap_cr_ticker_ids);
END;
$$
LANGUAGE plpgsql;