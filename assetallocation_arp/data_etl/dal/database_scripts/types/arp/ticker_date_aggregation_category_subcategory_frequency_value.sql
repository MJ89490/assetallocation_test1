DROP TYPE IF EXISTS  arp.asset_date_aggregation_category_subcategory_frequency_value CASCADE;
CREATE TYPE arp.asset_date_aggregation_category_subcategory_frequency_value AS (
  asset_subcategory varchar,
  date date,
  aggregation_level varchar,
  category varchar,
  subcategory varchar,
  frequency frequency,
  value numeric(32, 16)
);