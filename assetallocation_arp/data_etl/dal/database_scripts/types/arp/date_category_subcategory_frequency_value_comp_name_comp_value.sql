DROP TYPE IF EXISTS  arp.date_category_subcategory_frequency_value_comp_name_comp_value CASCADE;
CREATE TYPE arp.date_category_subcategory_frequency_value_comp_name_comp_value AS (
  business_date date,
  category text,
  subcategory text,
  frequency arp.frequency,
  value numeric(32, 16),
  comparator_name text,
  comparator_value numeric(32, 16)
);