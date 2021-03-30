CREATE OR REPLACE FUNCTION config.insert_model(
	name text,
  description text default '',
	out model_id int
)
AS
$$
declare
	execution_state_id int;
BEGIN
	SELECT config.insert_execution_state('config.insert_model') into execution_state_id;

	INSERT INTO config.model (name, description, execution_state_id)
	VALUES (name, description, execution_state_id);
	return;
END
$$
LANGUAGE plpgsql;