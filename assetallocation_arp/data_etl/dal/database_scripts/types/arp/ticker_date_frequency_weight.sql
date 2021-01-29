DROP TYPE IF EXISTS  arp.ticker_date_frequency_weight CASCADE;
CREATE TYPE arp.ticker_date_frequency_weight AS (
  ticker varchar,
  date date,
  frequency arp.frequency,
  weight numeric(32, 16)
);