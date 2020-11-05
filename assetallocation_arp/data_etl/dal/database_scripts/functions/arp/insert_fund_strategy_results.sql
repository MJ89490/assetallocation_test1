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
  _weights arp.asset_date_frequency_weight_weight[];
  _analytics arp.asset_date_aggregation_category_subcategory_frequency_value[];

BEGIN
  _weights := weights::arp.asset_date_frequency_weight_weight[];
  _analytics := analytics::arp.asset_date_aggregation_category_subcategory_frequency_value[];

  select config.insert_execution_state('arp.insert_fund_strategy_results') into execution_state_id;
  select select_fund.fund_id from fund.select_fund(fund_name) into fund_id;
  select select_strategy_id.strategy_id from arp.select_strategy_id(strategy_name, strategy_version) into strategy_id;
  select arp.insert_fund_strategy(fund_id, output_is_saved, strategy_id, weight,
                                  user_id, python_code_version, execution_state_id) into fund_strategy_id;

  PERFORM arp.insert_fund_strategy_asset_weights(fund_strategy_id, _weights, execution_state_id);
  PERFORM arp.insert_fund_strategy_analytics(fund_strategy_id, _analytics, execution_state_id);

  RETURN;
END
$$
LANGUAGE PLPGSQL;

CREATE OR REPLACE FUNCTION arp.insert_fund_strategy(
  fund_id int,
  output_is_saved boolean,
  strategy_id int,
  weight numeric,
  app_user_id varchar,
  python_code_version varchar,
  execution_state_id int,
  OUT fund_strategy_id int
)
AS
$$
BEGIN
  INSERT INTO arp.fund_strategy (
    fund_id,
    output_is_saved,
    strategy_id,
    weight,
    app_user_id,
    python_code_version,
    execution_state_id
  )
  VALUES(
    fund_id,
    output_is_saved,
    strategy_id,
    weight,
    app_user_id,
    python_code_version,
    execution_state_id
  )
  RETURNING arp.fund_strategy.id into fund_strategy_id;
  RETURN;
END
$$
LANGUAGE PLPGSQL;

CREATE OR REPLACE FUNCTION arp.insert_fund_strategy_asset_weights(
    fund_strategy_id int,
    weights arp.asset_date_frequency_weight_weight[],
    execution_state_id int
)
RETURNS void
AS
$$
BEGIN
  INSERT INTO arp.fund_strategy_asset_weight (
    fund_strategy_id,
    asset_subcategory,
    business_date,
    frequency,
    strategy_weight,
    implemented_weight,
    execution_state_id
  )
  SELECT
    insert_fund_strategy_asset_weights.fund_strategy_id,
    (aw).asset_subcategory,
    (aw).date,
    (aw).frequency,
    (aw).strategy_weight,
    (aw).implemented_weight,
    insert_fund_strategy_asset_weights.execution_state_id
  FROM
    unnest(weights) as aw;
  RETURN;
END
$$
LANGUAGE PLPGSQL;

CREATE OR REPLACE FUNCTION arp.insert_fund_strategy_analytics(
    fund_strategy_id int,
    analytics arp.asset_date_aggregation_category_subcategory_frequency_value[],
    execution_state_id int
)
RETURNS void
AS
$$
BEGIN
  INSERT INTO arp.fund_strategy_analytic (
    fund_strategy_id,
    asset_subcategory,
    aggregation_level,
    business_date,
    category,
    subcategory,
    frequency,
    value,
    execution_state_id
  )
  SELECT
    insert_fund_strategy_analytics.fund_strategy_id,
    (aa).asset_subcategory,
    (aa).aggregation_level,
    (aa).date,
    (aa).category,
    (aa).subcategory,
    (aa).frequency,
    (aa).value,
    insert_fund_strategy_analytics.execution_state_id
  FROM
    unnest(analytics) as aa;
  RETURN;
END
$$
LANGUAGE PLPGSQL;