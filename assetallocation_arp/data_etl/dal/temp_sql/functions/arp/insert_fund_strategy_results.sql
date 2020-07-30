CREATE OR REPLACE FUNCTION arp.insert_fund_strategy_results(
  business_datetime timestamp with time zone,
  fund_name varchar,
  save_output_flag boolean,
  strategy_id int, --TODO change this to name and version
  weight numeric,
  user_id varchar,
  python_code_version varchar,
  asset_weight_tickers varchar[],
  strategy_weights numeric[],
  implemented_weights numeric[],
  asset_analytic_tickers varchar[],
  analytic_types varchar[],
  analytic_subtypes varchar[],
  analytic_values numeric[],
  OUT fund_strategy_id int
)
AS
$$
DECLARE
  execution_state_id int;
  fund_id int;
BEGIN
  select config.insert_execution_state('insert_fund_strategy_results') into execution_state_id;
  select select_fund.fund_id from fund.select_fund(fund_name) into fund_id;
  select arp.insert_fund_strategy(business_datetime, fund_id, save_output_flag, strategy_id, weight, user_id,
    python_code_version, execution_state_id) into fund_strategy_id;

  PERFORM arp.insert_fund_strategy_asset_weights(fund_strategy_id, asset_weight_tickers, strategy_weights, implemented_weights, execution_state_id);
  PERFORM arp.insert_strategy_asset_analytics(fund_strategy_id, asset_analytic_tickers, analytic_types, analytic_subtypes, analytic_values, execution_state_id);

  RETURN;
END
$$
LANGUAGE PLPGSQL;