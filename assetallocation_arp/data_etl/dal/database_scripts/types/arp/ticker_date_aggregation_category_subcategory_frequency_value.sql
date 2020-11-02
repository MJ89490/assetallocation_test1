DROP TYPE IF EXISTS  arp.ticker_date_aggregation_category_subcategory_frequency_value CASCADE;
CREATE TYPE arp.ticker_date_aggregation_category_subcategory_frequency_value AS (
  ticker varchar,
  date date,
  aggregation_level varchar,
  category varchar,
  subcategory varchar,
  frequency frequency,
  value numeric(32, 16)
);