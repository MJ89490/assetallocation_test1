CREATE OR REPLACE FUNCTION arp.insert_fica_assets(
  fica_version int,
  asset_tickers varchar[],
  sovereign_tickers text[] ,
  swap_tickers text[],
  swap_cr_tickers text[]
)
RETURNS VOID
AS
$$
DECLARE
  execution_state_id int;
  strategy_name varchar;
  strategy_id int;
  _sovereign_tickers curve.ticker_months_years[];
  _swap_tickers curve.ticker_months_years[];
  _swap_cr_tickers curve.ticker_months_years[];
  _sovereign_ticker_ids int[];
  _swap_ticker_ids int[];
  _swap_cr_ticker_ids int[];
BEGIN
  strategy_name := 'fica';
  _sovereign_tickers := sovereign_tickers::curve.ticker_months_years[];
  _swap_tickers := swap_tickers::curve.ticker_months_years[];
  _swap_cr_tickers := swap_cr_tickers::curve.ticker_months_years[];

  SELECT config.insert_execution_state('arp.insert_fica_assets') INTO execution_state_id;
  SELECT arp.select_strategy_id(strategy_name, fica_version) INTO strategy_id;
  PERFORM arp.delete_fica_assets_from_fica_asset(strategy_id);
  SELECT curve.insert_tickers(execution_state_id, _sovereign_tickers) INTO _sovereign_ticker_ids;
  SELECT curve.insert_tickers(execution_state_id, _swap_tickers) INTO _swap_ticker_ids;
  SELECT curve.insert_tickers(execution_state_id, _swap_cr_tickers) INTO _swap_cr_ticker_ids;
  PERFORM arp.insert_fica_assets_into_fica_asset(strategy_id, execution_state_id, asset_tickers,
    _sovereign_ticker_ids, _swap_ticker_ids, _swap_cr_ticker_ids);
END;
$$
LANGUAGE plpgsql;