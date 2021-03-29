DROP FUNCTION arp.select_maven_strategy(integer);
CREATE OR REPLACE FUNCTION arp.select_maven_strategy(
  strategy_version int,
  OUT business_date_from date,
  OUT description varchar,
  OUT er_tr varchar,
  OUT frequency arp.frequency,
  OUT day_of_week integer,
  OUT asset_count integer,
  OUT long_cutoff integer,
  OUT short_cutoff integer,
  OUT val_period_months integer,
  OUT val_period_base integer,
  OUT momentum_weights numeric[],
  OUT volatility_weights numeric[]
)
AS
$$
BEGIN
	SELECT
    s.business_date_from,
	  s.description,
	  m.er_tr,
    m.frequency,
    m.day_of_week,
    m.asset_count,
    m.long_cutoff,
    m.short_cutoff,
    m.val_period_months,
    m.val_period_base,
    m.momentum_weights,
    m.volatility_weights
  INTO
    business_date_from,
    description,
	  er_tr,
    frequency,
    day_of_week,
    asset_count,
    long_cutoff,
    short_cutoff,
    val_period_months,
    val_period_base,
    momentum_weights,
    volatility_weights
	FROM
	  arp.strategy s
	  JOIN arp.maven m ON s.id = m.strategy_id
	WHERE
	  m.version = strategy_version;
  return;
END;
$$
LANGUAGE plpgsql;