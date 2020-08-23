DROP TYPE IF EXISTS  arp.category_datetime_value CASCADE;
CREATE TYPE arp.category_datetime_value AS (
  category varchar,
  business_datetime timestamp with time zone,
  value numeric(32, 16)
);