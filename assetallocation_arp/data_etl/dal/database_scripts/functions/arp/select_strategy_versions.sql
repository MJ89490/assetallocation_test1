CREATE OR REPLACE FUNCTION arp.select_strategy_versions(
  strategy_name varchar,
  OUT strategy_versions integer[]
)
AS
$$
BEGIN
  SELECT
  CASE
    WHEN strategy_name = 'times' THEN (SELECT array_agg(t.version) from arp.times t)
    WHEN strategy_name = 'effect' THEN (SELECT array_agg(e.version) from arp.effect e)
  END INTO strategy_versions
  ;
END;
$$
LANGUAGE plpgsql;