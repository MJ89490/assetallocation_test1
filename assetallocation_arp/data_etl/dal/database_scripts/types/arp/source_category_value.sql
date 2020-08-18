DROP TYPE IF EXISTS  arp.source_category_value CASCADE;
CREATE TYPE arp.source_category_value AS (
  source varchar,
  category varchar,
  value numeric(32, 16)
);