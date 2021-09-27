GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA asset TO l00_asset_allocation_data_app;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA asset TO l00_asset_allocation_data_app;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA asset TO l00_asset_allocation_data_app;

GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA portfolio_construction TO l00_asset_allocation_data_app;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA portfolio_construction TO l00_asset_allocation_data_app;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA portfolio_construction TO l00_asset_allocation_data_app;

GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA lookup TO l00_asset_allocation_data_app;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA lookup TO l00_asset_allocation_data_app;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA lookup TO l00_asset_allocation_data_app;

GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA arp TO l00_asset_allocation_data_app;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA arp TO l00_asset_allocation_data_app;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA arp TO l00_asset_allocation_data_app;

GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA fund TO l00_asset_allocation_data_app;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA fund TO l00_asset_allocation_data_app;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA fund TO l00_asset_allocation_data_app;

GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA audit TO l00_asset_allocation_data_app;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA audit TO l00_asset_allocation_data_app;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA audit TO l00_asset_allocation_data_app;

GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA config TO l00_asset_allocation_data_app;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA config TO l00_asset_allocation_data_app;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA config TO l00_asset_allocation_data_app;

GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA staging TO l00_asset_allocation_data_app;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA staging TO l00_asset_allocation_data_app;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA staging TO l00_asset_allocation_data_app;

GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA auth TO l00_asset_allocation_data_app;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA auth TO l00_asset_allocation_data_app;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA auth TO l00_asset_allocation_data_app;