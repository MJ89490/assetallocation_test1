DROP TYPE IF EXISTS  arp.ticker_date_frequency_weight_weight CASCADE;
CREATE TYPE arp.ticker_date_frequency_weight_weight AS (
  ticker varchar,
  date date,
  frequency frequency,
  strategy_weight numeric(32, 16),
  implemented_weight numeric(32, 16)
);