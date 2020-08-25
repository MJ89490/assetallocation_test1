CREATE OR REPLACE FUNCTION arp.select_fund_strategy(
  fund_name varchar,
  strategy_name varchar,
  system_datetime timestamp with time zone,
  OUT fund_strategy_id int,
  OUT currency char,
  OUT output_is_saved boolean,
  OUT weight numeric
)
LANGUAGE SQL
AS
$$
SELECT
  fs.id,
  c.currency,
  fs.output_is_saved,
  fs.weight
FROM
  fund.fund f
  JOIN lookup.currency c
  ON f.currency_id = c.id
  JOIN arp.fund_strategy fs
  ON f.id = fs.fund_id
  JOIN arp.strategy s
  ON fs.strategy_id = s.id
WHERE
  f.name = select_fund_strategy.fund_name
  AND s.name = select_fund_strategy.strategy_name
  AND fs.system_datetime <= select_fund_strategy.system_datetime
ORDER BY
  fs.system_datetime desc
LIMIT 1
$$;