CREATE OR REPLACE FUNCTION arp.insert_fund_strategy_results(
  fund_name varchar,
  strategy_name varchar,
  strategy_version int,
  business_tstzrange tstzrange,
  weight numeric,
  user_id varchar,
  python_code_version text,
  weights text[],
  strategy_analytics text[],
  strategy_asset_analytics text[],
  OUT fund_strategy_id int
)
AS
$$
DECLARE
  execution_state_id int;
  model_instance_id int;
  fund_id int;
  strategy_id int;
  fund_strategy_weight_id int;
  _weights arp.ticker_date_frequency_weight[];
  _strategy_analytics arp.date_category_subcategory_frequency_value_comp_name_comp_value[];
  _strategy_asset_analytics arp.ticker_date_category_subcategory_frequency_value[];
BEGIN
  _weights := weights::arp.ticker_date_frequency_weight[];
  _strategy_analytics := strategy_analytics::arp.date_category_subcategory_frequency_value_comp_name_comp_value[];
  _strategy_asset_analytics := strategy_asset_analytics::arp.ticker_date_category_subcategory_frequency_value[];

  select config.insert_execution_state('arp.insert_fund_strategy_results') into execution_state_id;
  SELECT
    config.insert_model_instance('ARP', business_tstzrange, python_code_version, execution_state_id)
  into
    model_instance_id;
  select select_fund.fund_id from fund.select_fund(fund_name) into fund_id;
  select arp.select_strategy_id(strategy_name, strategy_version) into strategy_id;
  select
    arp.select_current_fund_strategy_weight_id_for_weight(fund_id, strategy_id, weight)
  INTO
    fund_strategy_weight_id;

  if fund_strategy_weight_id IS NULL then
    PERFORM arp.close_off_fund_strategy_weight(fund_id, strategy_id);
    SELECT
      arp.insert_fund_strategy_weight(fund_id, strategy_id, weight, user_id, execution_state_id)
    INTO
      fund_strategy_weight_id;
  end if;

  PERFORM arp.insert_fund_strategy_asset_weights(
      fund_id, strategy_id, model_instance_id, user_id, _weights, execution_state_id
  );
  PERFORM arp.insert_strategy_analytics(strategy_id, model_instance_id, _strategy_analytics, execution_state_id);
  PERFORM arp.insert_strategy_asset_analytics(strategy_id, model_instance_id, _strategy_asset_analytics, execution_state_id);

  RETURN;
END
$$
LANGUAGE PLPGSQL;


CREATE OR REPLACE FUNCTION arp.select_current_fund_strategy_weight_id_for_weight(
  fund_id int,
  strategy_id int,
  weight numeric,
  out fund_strategy_weight_id int
)
AS
$$
BEGIN
  SELECT
    id
  INTO
    fund_strategy_weight_id
  from
    arp.fund_strategy_weight fsw
  where
    fsw.fund_id = select_current_fund_strategy_weight_id_for_weight.fund_id
    AND fsw.strategy_id = select_current_fund_strategy_weight_id_for_weight.strategy_id
    AND fsw.weight = select_current_fund_strategy_weight_id_for_weight.weight
    AND upper_inf(fsw.system_tstzrange)
  ;
END
$$
LANGUAGE PLPGSQL;


CREATE OR REPLACE FUNCTION arp.insert_fund_strategy_weight(
  fund_id int,
  strategy_id int,
  weight numeric,
  app_user_id varchar,
  execution_state_id int,
  OUT fund_strategy_id int
)
AS
$$
BEGIN
  INSERT INTO arp.fund_strategy_weight(
    fund_id,
    strategy_id,
    weight,
    set_by_id,
    execution_state_id
  )
  VALUES(
    fund_id,
    strategy_id,
    weight,
    app_user_id,
    execution_state_id
  )
  RETURNING arp.fund_strategy_weight.id into fund_strategy_id;
  RETURN;
END
$$
LANGUAGE PLPGSQL;


CREATE OR REPLACE FUNCTION arp.close_off_fund_strategy_weight(
  fund_id int,
  strategy_id int
)
  RETURNS VOID
AS
$$
BEGIN
  UPDATE arp.fund_strategy_weight
  SET system_tstzrange =  tstzrange(
        lower(system_tstzrange),
        now(),
        '[)'
    )
  WHERE
    arp.fund_strategy_weight.fund_id = close_off_fund_strategy_weight.fund_id
    AND arp.fund_strategy_weight.strategy_id = close_off_fund_strategy_weight.strategy_id
  ;
  RETURN;
END
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION arp.insert_fund_strategy_asset_weights(
  fund_id int,
  strategy_id int,
  model_instance_id int,
  set_by_id int,
  weights arp.ticker_date_frequency_weight[],
  execution_state_id int
)
RETURNS void
AS
$$
DECLARE
  id_weights arp.id_weight[];
BEGIN
  SELECT arp.insert_strategy_asset_weights(
      strategy_id, model_instance_id, weights, execution_state_id
  ) into id_weights;
  PERFORM arp.insert_fund_asset_weights(
      fund_id, set_by_id, id_weights, execution_state_id
  );
END
$$
LANGUAGE PLPGSQL;


CREATE OR REPLACE FUNCTION arp.insert_strategy_asset_weights(
    strategy_id int,
    model_instance_id int,
    weights arp.ticker_date_frequency_weight[],
    execution_state_id int,
    out id_weights arp.id_weight[]
)
AS
$$
BEGIN
  INSERT INTO arp.strategy_asset_weight(
    strategy_id,
    asset_id,
    model_instance_id,
    business_date,
    frequency,
    theoretical_weight,
    execution_state_id
  )
  SELECT
    insert_strategy_asset_weights.strategy_id,
    a.id,
    insert_strategy_asset_weights.model_instance_id,
    (aw).date,
    (aw).frequency,
    (aw).weight,
    insert_strategy_asset_weights.execution_state_id
  FROM
    unnest(weights) as aw
    JOIN asset.asset a ON a.ticker = (aw).ticker
  RETURNING array_agg(arp.strategy_asset_weight.id, arp.strategy_asset_weight.theoretical_weight::arp.id_weight) into id_weights;
  RETURN;
END
$$
LANGUAGE PLPGSQL;


CREATE OR REPLACE FUNCTION arp.insert_fund_asset_weights(
    fund_id int,
    id_weights arp.id_weight[],
    set_by_id int,
    execution_state_id int
)
  RETURNS VOID
AS
$$
DECLARE
  business_date_range daterange;
BEGIN
  -- per fund, per strategy, per asset_id per business datetime there should be one value
  SELECT
    daterange(min(saw.business_date), max(saw.business_date) + 1)
  INTO
    business_date_range
  FROM
    arp.strategy_asset_weight saw
    JOIN unnest(id_weights) as iw ON saw.id = (iw).id
  ;

  UPDATE arp.fund_strategy_asset_weight
  SET system_tstzrange =  tstzrange(
        lower(system_tstzrange),
        now(),
        '[)'
    )
  FROM
    arp.fund_strategy_asset_weight fsaw
    JOIN arp.strategy_asset_weight saw ON fsaw.strategy_asset_weight_id = saw.id
  WHERE
    saw.business_date <@ insert_fund_asset_weights.business_date_range
  ;

  INSERT INTO arp.fund_strategy_asset_weight(
    fund_id,
    strategy_asset_weight_id,
    set_by_id,
    implemented_weight,
    execution_state_id
  )
  SELECT
    insert_fund_asset_weights.fund_id,
    (iw).id as strategy_asset_weight_id,
    insert_fund_asset_weights.set_by_id,
    (iw).weight as implemented_weight,
    insert_fund_asset_weights.execution_state_id
  FROM
    unnest(id_weights) as iw
  ;
  RETURN;
END
$$
LANGUAGE PLPGSQL;


CREATE OR REPLACE FUNCTION arp.insert_strategy_analytics(
    strategy_id int,
    model_instance_id int,
    analytics arp.date_category_subcategory_frequency_value_comp_name_comp_value[],
    execution_state_id int
)
RETURNS void
AS
$$
BEGIN
  INSERT INTO arp.strategy_analytic(
    strategy_id,
    model_instance_id,
    business_date,
    category,
    subcategory,
    frequency,
    value,
    comparator_name,
    comparator_value,
    execution_state_id
  )
  SELECT
    insert_strategy_analytics.strategy_id,
    insert_strategy_analytics.model_instance_id,
    (a).business_date,
    (a).category,
    (a).subcategory,
    (a).frequency,
    (a).value,
    (a).comparator_name,
    (a).comparator_value,
    insert_strategy_analytics.execution_state_id
  FROM
    unnest(analytics) as a;
  RETURN;
END
$$
LANGUAGE PLPGSQL;


CREATE OR REPLACE FUNCTION arp.insert_strategy_asset_analytics(
    strategy_id int,
    model_instance_id int,
    analytics arp.ticker_date_category_subcategory_frequency_value[],
    execution_state_id int
)
RETURNS void
AS
$$
BEGIN
  INSERT INTO arp.strategy_asset_analytic(
    strategy_id,
    model_instance_id,
    asset_id,
    business_date,
    category,
    subcategory,
    frequency,
    value,
    execution_state_id
  )
  SELECT
    insert_strategy_asset_analytics.strategy_id,
    insert_strategy_asset_analytics.model_instance_id,
    aa.id,
    (a).business_date,
    (a).category,
    (a).subcategory,
    (a).frequency,
    (a).value,
    insert_strategy_asset_analytics.execution_state_id
  FROM
    unnest(analytics) as a
    JOIN asset.asset aa on (a).ticker = aa.ticker
  ;
  RETURN;
END
$$
LANGUAGE PLPGSQL;
