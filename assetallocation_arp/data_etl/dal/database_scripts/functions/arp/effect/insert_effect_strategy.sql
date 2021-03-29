CREATE OR REPLACE FUNCTION arp.insert_effect_strategy(
  business_date_from date,
  description varchar,
  user_id varchar,
  carry_type varchar,
  closing_threshold numeric,
  cost numeric,
  day_of_week int,
  frequency arp.frequency,
  include_shorts boolean,
  inflation_lag interval,
  interest_rate_cut_off_long numeric,
  interest_rate_cut_off_short numeric,
  moving_average_long_term int,
  moving_average_short_term int,
  realtime_inflation_forecast_flag boolean,
  trend_indicator varchar,
  OUT e_version int
)
LANGUAGE plpgsql
AS
$$
declare
  name varchar;
	execution_state_id int;
	strategy_id int;
BEGIN
  name := 'effect';
  
	SELECT config.insert_execution_state('insert_times_strategy') into execution_state_id;
  PERFORM arp.close_off_strategy(name);
	SELECT arp.insert_strategy(name, business_date_from, description, user_id, execution_state_id) into strategy_id;
INSERT INTO arp.effect (
  strategy_id,
  carry_type,
  closing_threshold,
  cost,
  day_of_week,
  frequency,
  include_shorts,
  inflation_lag,
  interest_rate_cut_off_long,
  interest_rate_cut_off_short,
  moving_average_long_term,
  moving_average_short_term,
  realtime_inflation_forecast_flag,
  trend_indicator,
  execution_state_id
)
VALUES(
  strategy_id,
  carry_type,
  closing_threshold,
  cost,
  day_of_week,
  frequency,
  include_shorts,
  inflation_lag,
  interest_rate_cut_off_long,
  interest_rate_cut_off_short,
  moving_average_long_term,
  moving_average_short_term,
  realtime_inflation_forecast_flag,
  trend_indicator,
  execution_state_id
	)
	RETURNING arp.effect.version into e_version;
	return;
END
$$;