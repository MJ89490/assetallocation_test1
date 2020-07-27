CREATE OR REPLACE FUNCTION insert_strategy(
  name varchar,
  description varchar,
  user_id varchar,
	execution_state_id int,
	out strategy_id int
)
language plpgsql
as
$$
BEGIN
INSERT INTO arp.strategy (name, description, user_id, execution_state_id)
VALUES (
  name,
  description,
  user_id,
  execution_state_id
)
RETURNING arp.strategy.id into strategy_id;
return;
END
$$