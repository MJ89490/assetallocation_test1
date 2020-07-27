CREATE OR REPLACE FUNCTION insert_strategy(
  name varchar,
  description varchar,
  user_id varchar,
	execution_state_id int,
	out strategy_id int
)
language sql
as
$$
INSERT INTO arp.strategy (name, description, user_id, execution_state_id)
SELECT
  name,
  description,
  user_id,
  inserted_es.id
FROM
  inserted_es
RETURNING arp.strategy.id
$$