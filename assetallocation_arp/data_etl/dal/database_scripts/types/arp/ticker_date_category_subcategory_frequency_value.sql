DROP TYPE IF EXISTS  arp.ticker_date_category_subcategory_frequency_value CASCADE;
CREATE TYPE arp.ticker_date_category_subcategory_frequency_value AS (
  ticker varchar,
  business_date date,
  category varchar,
  subcategory varchar,
  frequency arp.frequency,
  value numeric(32, 16)
);