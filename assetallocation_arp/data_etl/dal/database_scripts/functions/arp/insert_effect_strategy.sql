CREATE OR REPLACE FUNCTION arp.insert_effect_strategy(
  description varchar,
  user_id varchar,
  update_imf boolean,
	user_date date,
	signal_date date,
	position_size numeric,
	risk_weighting varchar,
	st_dev_window integer,
	bid_ask_spread integer,
	carry_type varchar,
	closing_threshold numeric,
	day_of_week integer,
	frequency frequency,
	include_shorts boolean,
	interest_rate_cut_off_long numeric,
	interest_rate_cut_off_short numeric,
	moving_average_long_term int,
	moving_average_short_term int,
	is_realtime_inflation_forecast boolean,
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

	SELECT config.insert_execution_state('insert_effect_strategy') into execution_state_id;
  PERFORM arp.close_off_strategy(name);
	SELECT arp.insert_strategy(name, description, user_id, execution_state_id) into strategy_id;
  INSERT INTO arp.effect (
    strategy_id,
    update_imf,
    user_date,
    signal_date,
    position_size,
    risk_weighting,
    st_dev_window,
    bid_ask_spread,
    carry_type,
    closing_threshold,
    day_of_week,
    frequency,
    include_shorts,
    interest_rate_cut_off_long,
    interest_rate_cut_off_short,
    moving_average_long_term,
    moving_average_short_term,
    is_realtime_inflation_forecast,
    trend_indicator,
    execution_state_id
  )
  VALUES(
    strategy_id,
    update_imf,
    user_date,
    signal_date,
    position_size,
    risk_weighting,
    st_dev_window,
    bid_ask_spread,
    carry_type,
    closing_threshold,
    day_of_week,
    frequency,
    include_shorts,
    interest_rate_cut_off_long,
    interest_rate_cut_off_short,
    moving_average_long_term,
    moving_average_short_term,
    is_realtime_inflation_forecast,
    trend_indicator,
    execution_state_id
  )
	RETURNING arp.effect.version into e_version;
	return;
END
$$;