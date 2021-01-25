DROP TYPE IF EXISTS  arp.category_subcategory_frequency_value CASCADE;
CREATE TYPE arp.category_subcategory_frequency_value AS (
  category varchar,
  subcategory varchar,
  frequency arp.frequency,
  value numeric(32, 16)
);