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
    WHEN strategy_name = 'fica' THEN (SELECT array_agg(f.version) from arp.fica f)
    WHEN strategy_name = 'fx' THEN (SELECT array_agg(fx.version) from arp.fx fx)
    WHEN strategy_name = 'maven' THEN (SELECT array_agg(m.version) from arp.maven m)
  END INTO strategy_versions
  ;
END;
$$
LANGUAGE plpgsql;