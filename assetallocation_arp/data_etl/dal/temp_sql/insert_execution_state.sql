CREATE OR REPLACE FUNCTION insert_execution_state(
	execution_name varchar,
	out execution_state_id int
)
language sql
as
$$
with iese as (
	select id
	from config.execution e
	where e.name = execution_name
	and in_use = 't'
)
insert into config.execution_state (system_datetime, execution_id)
select
	now(),
	iese.id
from
	iese
RETURNING execution_state.id
$$