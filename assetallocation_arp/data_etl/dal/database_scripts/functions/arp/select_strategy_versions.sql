DROP FUNCTION arp.select_strategy_versions(character varying);
CREATE OR REPLACE FUNCTION arp.select_strategy_versions(
  strategy_name varchar
)
  RETURNS TABLE(
  version int,
  description varchar
)
AS
$$
BEGIN
  RETURN QUERY
    SELECT
      COALESCE(t.version, e.version, fi.version, fx.version, m.version) as version,
      s.description
    FROM
      arp.strategy s
      LEFT JOIN arp.times t on t.strategy_id = s.id
      LEFT JOIN arp.effect e on e.strategy_id = s.id
      LEFT JOIN arp.fica fi on fi.strategy_id = s.id
      LEFT JOIN arp.fx fx on fx.strategy_id = s.id
      LEFT JOIN arp.maven m on m.strategy_id = s.id
    WHERE
      s.name = strategy_name
  ;
END;
$$
LANGUAGE plpgsql;