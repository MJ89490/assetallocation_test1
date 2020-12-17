CREATE OR REPLACE FUNCTION arp.insert_maven_strategy(
  description varchar,
  user_id varchar,
  er_tr varchar,
	frequency frequency,
	day_of_week integer,
	asset_count integer,
	long_cutoff integer,
	short_cutoff integer,
	val_period_months integer,
	val_period_base integer,
	momentum_weights numeric[],
	volatility_weights numeric[],
  OUT t_version int
)
LANGUAGE plpgsql
AS
$$
declare
  name varchar;
	execution_state_id int;
	strategy_id int;
BEGIN
  name := 'maven';
	SELECT config.insert_execution_state('arp.insert_maven_strategy') into execution_state_id;
  PERFORM arp.close_off_strategy(name);
	SELECT arp.insert_strategy(name, description, user_id, execution_state_id) into strategy_id;
	SELECT arp.insert_maven(
      er_tr, frequency, day_of_week, asset_count, long_cutoff, short_cutoff, val_period_months,
      val_period_base, momentum_weights, volatility_weights, execution_state_id, strategy_id
  ) into t_version;
	return;
END
$$;

CREATE OR REPLACE FUNCTION arp.insert_maven(
  er_tr varchar,
	frequency frequency,
	day_of_week integer,
	asset_count integer,
	long_cutoff integer,
	short_cutoff integer,
	val_period_months integer,
	val_period_base integer,
	momentum_weights numeric[],
	volatility_weights numeric[],
  execution_state_id int,
  strategy_id int,
  OUT t_version int
)
AS
$$
BEGIN
	INSERT INTO arp.maven (
	  er_tr,
    frequency,
    day_of_week,
    asset_count,
    long_cutoff,
    short_cutoff,
    val_period_months,
    val_period_base,
    momentum_weights,
    volatility_weights,
	  execution_state_id,
	  strategy_id
	)
	VALUES(
	  er_tr,
    frequency,
    day_of_week,
    asset_count,
    long_cutoff,
    short_cutoff,
    val_period_months,
    val_period_base,
    momentum_weights,
    volatility_weights,
	  execution_state_id,
	  strategy_id
	)
	RETURNING arp.maven.version into t_version;
	return;
END;
$$
LANGUAGE plpgsql;
