CREATE OR REPLACE FUNCTION insert_fund_strategy(
  business_datetime timestamp with time zone,
  fund_name varchar,
  save_output_flag boolean,
  strategy_id int,
  weight numeric,
  user_id varchar,
  python_code_version varchar,
  OUT fund_strategy_id int
)
LANGUAGE SQL
AS
$$
with iese as (
	select id
	from config.execution e
	where e.name = 'insert_effect_strategy'
	and in_use = 't'
)
,
inserted_es (execution_state_id) as (
insert into confog.execution_state (system_datetime, execution_id)
select
	now(),
	iese.id
from
	iese
RETURNING execution_state.id
),
f(fund_id) AS (
  SELECT f.id
  FROM fund.fund f
  WHERE f.name = fund_name
)
INSERT INTO arp.fund_strategy (
  business_datetime,
  fund_id,
  save_output_flag,
  strategy_id,
  weight,
  user_id,
  python_code_version,
  execution_state_id
)
SELECT
  business_datetime,
  f.fund_id,
  save_output_flag,
  strategy_id,
  weight,
  user_id,
  python_code_version,
  inserted_es.execution_state_id
from
  f
  cross join inserted_es
RETURNING arp.fund_strategy.id
$$;