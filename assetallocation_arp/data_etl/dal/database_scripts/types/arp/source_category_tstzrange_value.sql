DROP TYPE IF EXISTS  arp.source_category_tstzrange_value CASCADE;
CREATE TYPE arp.source_category_tstzrange_value AS (
  source varchar,
  category varchar,
  business_tstzrange tstzrange,
  value numeric(32, 16)
);