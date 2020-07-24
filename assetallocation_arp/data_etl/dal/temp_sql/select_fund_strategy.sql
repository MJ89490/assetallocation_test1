CREATE OR REPLACE FUNCTION select_fund_strategy(
  fund_name varchar,
  strategy_name varchar,
  business_datetime timestamp with time zone,
  system_datetime timestamp with time zone,
  OUT s_user_email varchar,
  OUT s_user_id varchar,
  OUT s_user_name varchar,
  OUT s_name varchar,
  OUT description varchar,
  OUT fs_user_email varchar,
  OUT fs_user_id varchar,
  OUT fs_user_name varchar,
  OUT currency char,
  OUT f_name varchar,
  OUT save_output_flag boolean,
  OUT weight numeric
)
LANGUAGE SQL
AS
$$
SELECT
  su.email,
  su.id,
  su.name,
  s.name,
  s.description,
  fsu.email,
  fsu.id,
  fsu.name,
  c.currency,
  f.name,
  fs.save_output_flag,
  fs.weight
FROM
  fund.fund f
  JOIN lookup.currency c
  ON f.currency_id = c.id
  JOIN arp.fund_strategy fs
  ON f.id = fs.fund_id
  JOIN user.app_user fsu
  ON fs.user_id = fsu.id
  JOIN arp.strategy s
  ON fs.strategy_id = s.id
  JOIN user.app_user su
  ON s.user_id = su.id
WHERE
  f.name = select_fund_strategy.fund_name
  AND s.name = select_fund_strategy.strategy_name
  AND fs.business_datetime = select_fund_strategy.business_datetime
  AND fs.system_datetime = select_fund_strategy.system_datetime
$$;