DROP TYPE IF EXISTS  arp.ticker_date_category_subcategory_value CASCADE;
CREATE TYPE arp.ticker_date_category_subcategory_value AS (
  ticker varchar,
  date date,
  category varchar,
  subcategory varchar,
  value numeric(32, 16)
);