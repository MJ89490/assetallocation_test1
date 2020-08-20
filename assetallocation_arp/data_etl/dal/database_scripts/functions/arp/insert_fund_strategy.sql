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