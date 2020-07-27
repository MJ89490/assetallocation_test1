CREATE OR REPLACE FUNCTION insert_execution_state(
	execution_name varchar,
	out execution_state_id int
)
language plpgsql
as
$$
declare
	execution_id int;
begin
	select
	  id
	into
	  execution_id
	from
	  config.execution e
	where
	  e.name = execution_name
	  and in_use = 't';
	insert into config.execution_state (system_datetime, execution_id)
	values (now(), execution_id)
	RETURNING execution_state.id into execution_state_id
	return;
END
$$