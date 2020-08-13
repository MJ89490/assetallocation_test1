CREATE OR REPLACE FUNCTION arp.insert_app_user(
  id varchar(7),
  name varchar,
  email varchar default null
)
RETURNS VOID
AS
$$
declare
	execution_state_id int;
BEGIN
	SELECT config.insert_execution_state('arp.insert_app_user') into execution_state_id;

	INSERT INTO arp.app_user (id, name, email, execution_state_id)
	VALUES (id, name, email, execution_state_id);
	return;
END
$$
LANGUAGE plpgsql;
