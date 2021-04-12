DROP TYPE IF EXISTS  arp.ticker_category_subcategory_value CASCADE;
CREATE TYPE arp.ticker_category_subcategory_value AS (
  ticker varchar,
  category varchar,
  subcategory varchar,
  value numeric(32, 16)
);