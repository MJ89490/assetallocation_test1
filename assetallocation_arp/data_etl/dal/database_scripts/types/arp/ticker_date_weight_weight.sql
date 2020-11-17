DROP TYPE IF EXISTS  arp.asset_date_frequency_weight_weight CASCADE;
CREATE TYPE arp.asset_date_frequency_weight_weight AS (
  asset_subcategory varchar,
  date date,
  frequency frequency,
  strategy_weight numeric(32, 16),
  implemented_weight numeric(32, 16)
);