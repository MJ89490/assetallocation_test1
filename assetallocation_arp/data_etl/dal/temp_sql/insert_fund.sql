CREATE OR REPLACE FUNCTION insert_fund(
  name varchar,
  fund_currency char(2),
  OUT fund_id int
)
LANGUAGE plpgsql
AS
$$
declare
	execution_state_id int;
	currency_id int;
BEGIN
	SELECT insert_execution_state('insert_fund') into execution_state_id;
	SELECT id from lookup.currency where currency = fund_currency into currency_id;
	INSERT INTO fund.fund (name, currency_id, execution_state_id)
	VALUES (name, currency_id, execution_state_id)
  RETURNING fund.fund.id into fund_id;
	return;
END
$$;
