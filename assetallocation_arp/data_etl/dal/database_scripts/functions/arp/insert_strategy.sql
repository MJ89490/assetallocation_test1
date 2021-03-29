CREATE OR REPLACE FUNCTION arp.insert_strategy(
  name varchar,
  business_date_from date,
  description varchar,
  app_user_id varchar,
	execution_state_id int,
	out strategy_id int
)
language plpgsql
as
$$
BEGIN
INSERT INTO arp.strategy (name, business_date_from, description, app_user_id, execution_state_id)
VALUES (
  name,
  business_date_from,
  description,
  app_user_id,
  execution_state_id
)
RETURNING arp.strategy.id into strategy_id;
return;
END
$$