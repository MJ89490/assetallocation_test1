CREATE OR REPLACE FUNCTION config.insert_model_instance(
	model_name text,
  business_tstzrange tstzrange,
  python_code_version text,
  execution_state_id int,
  out model_instance_id int
)
language plpgsql
as
$$
declare
	model_id int;
begin
	select id into model_id from config.model m where  m.name = model_name;
	insert into config.model_instance (business_tstzrange, model_id, python_code_version, execution_state_id)
	values (business_tstzrange, model_id, python_code_version, execution_state_id)
	RETURNING model_instance.id into model_instance_id;
	return;
END
$$