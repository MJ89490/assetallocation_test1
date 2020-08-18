CREATE OR REPLACE FUNCTION arp.close_off_strategy(name varchar)
  RETURNS VOID
AS
$$
BEGIN
  UPDATE arp.strategy
  SET system_tstzrange =  tstzrange(
        lower(system_tstzrange),
        now(),
        '[)'
    )
  WHERE arp.strategy.name = close_off_strategy.name;
  RETURN;
END
$$
LANGUAGE plpgsql;
