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
INSERT INTO arp.strategy(name, business_date_from, description, user_id, execution_state_id)
SELECT
  insert_strategy.name,
  insert_strategy.business_date_from,
  insert_strategy.description,
  au.id,
  insert_strategy.execution_state_id
FROM
  auth.user au
WHERE
  au.windows_username = app_user_id
  OR au.domino_username = app_user_id
RETURNING arp.strategy.id into strategy_id;
return;
END
$$