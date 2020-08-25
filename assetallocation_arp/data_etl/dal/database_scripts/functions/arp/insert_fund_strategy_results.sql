CREATE OR REPLACE FUNCTION arp.insert_fund_strategy_results(
  fund_name varchar,
  output_is_saved boolean,
  strategy_name varchar,
  strategy_version int,
  weight numeric,
  user_id varchar,
  python_code_version varchar,
  weights text[],
  analytics text[],
  OUT fund_strategy_id int
)
AS
$$
DECLARE
  execution_state_id int;
  fund_id int;
  strategy_id int;
  _weights arp.ticker_date_weight_weight[];
  _analytics arp.ticker_date_category_subcategory_value[];

BEGIN
  _weights := weights::arp.ticker_date_weight_weight[];
  _analytics := analytics::arp.ticker_date_category_subcategory_value[];

  select config.insert_execution_state('arp.insert_fund_strategy_results') into execution_state_id;
  select select_fund.fund_id from fund.select_fund(fund_name) into fund_id;
  select select_strategy_id.strategy_id from arp.select_strategy_id(strategy_name, strategy_version) into strategy_id;
  select arp.insert_fund_strategy(fund_id, output_is_saved, strategy_id, weight,
                                  user_id, python_code_version, execution_state_id) into fund_strategy_id;

  PERFORM arp.insert_fund_strategy_asset_weights(fund_strategy_id, _weights, execution_state_id);
  PERFORM arp.insert_fund_strategy_asset_analytics(fund_strategy_id, _analytics, execution_state_id);

  RETURN;
END
$$
LANGUAGE PLPGSQL;