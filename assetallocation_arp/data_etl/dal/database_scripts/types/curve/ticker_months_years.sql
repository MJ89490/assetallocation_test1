DROP TYPE IF EXISTS  curve.ticker_months_years CASCADE;
CREATE TYPE curve.ticker_months_years AS (
  category varchar,
  mth3 varchar,
	yr1 varchar,
	yr2 varchar,
	yr3 varchar,
	yr4 varchar,
	yr5 varchar,
	yr6 varchar,
	yr7 varchar,
	yr8 varchar,
	yr9 varchar,
	yr10 varchar,
	yr15 varchar,
	yr20 varchar,
	yr30 varchar	
);