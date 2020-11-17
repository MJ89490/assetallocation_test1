CREATE OR REPLACE FUNCTION arp.select_effect_strategy(
  strategy_version int,
  OUT description varchar,
  OUT frequency varchar,
	OUT day_of_week integer,
	OUT trend_indicator varchar,
	OUT moving_average_short_term integer,
	OUT moving_average_long_term integer,
	OUT include_shorts boolean,
  OUT interest_rate_cut_off_short numeric(32,16),
  OUT interest_rate_cut_off_long numeric(32,16),
	OUT carry_type varchar,
	OUT inflation_lag interval,
	OUT is_realtime_inflation_forecast boolean,
	OUT closing_threshold numeric(32,16),
	OUT cost numeric(32,16)
)
AS
$$
DECLARE
  strategy_name varchar;
BEGIN
  strategy_name := 'effect';

	SELECT
	  s.description,
	  e.frequency,
	  e.day_of_week,
	  e.trend_indicator,
	  e.moving_average_short_term,
	  e.moving_average_long_term,
	  e.include_shorts,
    e.interest_rate_cut_off_short,
	  e.interest_rate_cut_off_long,
    e.carry_type,
    e.inflation_lag,
    e.is_realtime_inflation_forecast,
    e.closing_threshold,
    e.cost
  INTO
    description,
	  frequency,
	  day_of_week,
	  trend_indicator,
	  moving_average_short_term,
	  moving_average_long_term,
	  include_shorts,
    interest_rate_cut_off_short,
	  interest_rate_cut_off_long,
    carry_type,
    inflation_lag,
    is_realtime_inflation_forecast,
    closing_threshold,
    cost
	FROM
	  arp.strategy s
	  JOIN arp.effect e
	  ON s.id = e.strategy_id
	WHERE
	  s.name = strategy_name
	  AND e.version = strategy_version;
  return;
END;
$$
LANGUAGE plpgsql;