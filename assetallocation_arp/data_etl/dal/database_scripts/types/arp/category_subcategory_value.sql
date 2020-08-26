DROP TYPE IF EXISTS  arp.category_subcategory_value CASCADE;
CREATE TYPE arp.category_subcategory_value AS (
  category varchar,
  subcategory varchar,
  value numeric(32, 16)
);