/* Create schemas*/
CREATE SCHEMA IF NOT EXISTS asset;
GRANT USAGE ON SCHEMA asset TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA asset
  GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON TABLES TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA asset GRANT EXECUTE ON FUNCTIONS TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA asset GRANT USAGE ON TYPES TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA asset GRANT USAGE ON SEQUENCES TO d00_asset_allocation_data_app;

CREATE SCHEMA IF NOT EXISTS lookup;
GRANT USAGE ON SCHEMA lookup TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA lookup
  GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON TABLES TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA lookup GRANT EXECUTE ON FUNCTIONS TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA lookup GRANT USAGE ON TYPES TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA lookup GRANT USAGE ON SEQUENCES TO d00_asset_allocation_data_app;

CREATE SCHEMA IF NOT EXISTS arp;
GRANT USAGE ON SCHEMA arp TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA arp
  GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON TABLES TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA arp GRANT EXECUTE ON FUNCTIONS TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA arp GRANT USAGE ON TYPES TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA arp GRANT USAGE ON SEQUENCES TO d00_asset_allocation_data_app;

CREATE SCHEMA IF NOT EXISTS fund;
GRANT USAGE ON SCHEMA fund TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA fund
  GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON TABLES TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA fund GRANT EXECUTE ON FUNCTIONS TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA fund GRANT USAGE ON TYPES TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA fund GRANT USAGE ON SEQUENCES TO d00_asset_allocation_data_app;

CREATE SCHEMA IF NOT EXISTS audit;
GRANT USAGE ON SCHEMA audit TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA audit
  GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON TABLES TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA audit GRANT EXECUTE ON FUNCTIONS TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA audit GRANT USAGE ON TYPES TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA audit GRANT USAGE ON SEQUENCES TO d00_asset_allocation_data_app;

CREATE SCHEMA IF NOT EXISTS config;
GRANT USAGE ON SCHEMA config TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA config
  GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON TABLES TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA config GRANT EXECUTE ON FUNCTIONS TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA config GRANT USAGE ON TYPES TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA config GRANT USAGE ON SEQUENCES TO d00_asset_allocation_data_app;

CREATE SCHEMA IF NOT EXISTS staging;
GRANT USAGE ON SCHEMA staging TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA staging
  GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON TABLES TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA staging GRANT EXECUTE ON FUNCTIONS TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA staging GRANT USAGE ON TYPES TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA staging GRANT USAGE ON SEQUENCES TO d00_asset_allocation_data_app;

CREATE SCHEMA IF NOT EXISTS auth;
GRANT USAGE ON SCHEMA auth TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA auth
  GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON TABLES TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA auth GRANT EXECUTE ON FUNCTIONS TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA auth GRANT USAGE ON TYPES TO d00_asset_allocation_data_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA auth GRANT USAGE ON SEQUENCES TO d00_asset_allocation_data_app;