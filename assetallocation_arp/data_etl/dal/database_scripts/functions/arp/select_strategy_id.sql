CREATE OR REPLACE FUNCTION arp.select_strategy_id(
  strategy_name varchar,
  strategy_version int,
  OUT strategy_id int
)
AS
$$
BEGIN
  EXECUTE format(
  'SELECT
    strategy_id
  FROM
  arp.%I
  WHERE
  version = %L;'
  , strategy_name, strategy_version)
  INTO strategy_id;

  RETURN;
END
$$
LANGUAGE PLPGSQL;