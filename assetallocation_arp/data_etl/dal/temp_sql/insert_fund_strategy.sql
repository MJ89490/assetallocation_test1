CREATE [OR REPLACE] FUNCTION insert_fund_strategy(
  business_datetime timestamp with time zone,
  fund_name varchar,
  save_output_flag boolean,
  strategy_id int,
  weight numeric,
  user_id varchar,
  OUT fund_strategy_id int,
)
LANGUAGE SQL
AS
$$
WITH fund AS (
  SELECT f.id
  FROM fund.fund f
  WHERE f.name = fund_name
)
INSERT INTO arp.fund_strategy (business_datetime, fund_id, save_output_flag, strategy_id, user_id)
SELECT business_datetime, fund.fund_id, save_output_flag, strategy_id, user_id
from fund
RETURNING arp.fund_strategy.id
$$;