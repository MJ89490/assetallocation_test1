CREATE OR REPLACE FUNCTION arp.insert_fund_strategy(
  business_datetime timestamp with time zone,
  fund_id int,
  save_output_flag boolean,
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
    business_datetime,
    fund_id,
    save_output_flag,
    strategy_id,
    weight,
    app_user_id,
    python_code_version,
    execution_state_id
  )
  VALUES(
    business_datetime,
    fund_id,
    save_output_flag,
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