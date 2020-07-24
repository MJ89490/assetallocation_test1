CREATE OR REPLACE FUNCTION select_fund(fund_name varchar, OUT fund_id int, OUT currency char)
LANGUAGE SQL
AS
$$
SELECT
  f.id,
  c.currency
FROM
  fund.fund f
  JOIN lookup.currency c
  ON f.currency_id = c.id
WHERE
  f.name = fund_name
$$;