DROP FUNCTION arp.select_effect_strategy(integer);
CREATE OR REPLACE FUNCTION arp.select_effect_strategy(
  strategy_version int,
  OUT business_date_from date,
  OUT description varchar,
  OUT update_imf boolean,
  OUT user_date date,
  OUT signal_date date,
  OUT position_size numeric,
  OUT risk_weighting varchar,
  OUT st_dev_window integer,
  OUT bid_ask_spread integer,
  OUT carry_type varchar,
  OUT closing_threshold numeric,
  OUT day_of_week integer,
  OUT frequency arp.frequency,
  OUT include_shorts boolean,
  OUT interest_rate_cut_off_long numeric,
  OUT interest_rate_cut_off_short numeric,
  OUT moving_average_long_term int,
  OUT moving_average_short_term int,
  OUT is_real_time_inflation_forecast boolean,
  OUT trend_indicator varchar
)
AS
$$
BEGIN
	SELECT
    s.business_date_from,
	  s.description,
	  e.update_imf,
    e.user_date,
    e.signal_date,
    e.position_size,
    e.risk_weighting,
    e.st_dev_window,
    e.bid_ask_spread,
    e.carry_type,
    e.closing_threshold,
    e.day_of_week,
    e.frequency,
    e.include_shorts,
    e.interest_rate_cut_off_long,
    e.interest_rate_cut_off_short,
    e.moving_average_long_term,
    e.moving_average_short_term,
    e.is_real_time_inflation_forecast,
    e.trend_indicator
  INTO
    business_date_from,
    description,
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
    is_real_time_inflation_forecast,
    trend_indicator
	FROM
	  arp.strategy s
	  JOIN arp.effect e
	  ON s.id = e.strategy_id
	WHERE
	  e.version = strategy_version;
  return;
END;
$$
LANGUAGE plpgsql;