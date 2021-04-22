DROP TYPE IF EXISTS  arp.category_subcategory_frequency_value_comp_name_comp_value CASCADE;
CREATE TYPE arp.category_subcategory_frequency_value_comp_name_comp_value AS (
  category text,
  subcategory text,
  frequency arp.frequency,
  value numeric(32, 16),
  comparator_name text,
  comparator_value text
);