DROP TYPE IF EXISTS  arp.aggregation_category_subcategory_frequency_value CASCADE;
CREATE TYPE arp.aggregation_category_subcategory_frequency_value AS (
  aggregation_level varchar,
  category varchar,
  subcategory varchar,
  frequency frequency,
  value numeric(32, 16)
);