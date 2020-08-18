/* Create schemas*/
CREATE SCHEMA IF NOT EXISTS asset;
GRANT ALL ON SCHEMA asset TO d00_asset_allocation_data_migration;
GRANT ALL ON SCHEMA asset TO d00_asset_allocation_data_app;

CREATE SCHEMA IF NOT EXISTS curve;
GRANT ALL ON SCHEMA curve TO d00_asset_allocation_data_migration;
GRANT ALL ON SCHEMA asset TO d00_asset_allocation_data_app;

CREATE SCHEMA IF NOT EXISTS lookup;
GRANT ALL ON SCHEMA lookup TO d00_asset_allocation_data_migration;
GRANT ALL ON SCHEMA asset TO d00_asset_allocation_data_app;

CREATE SCHEMA IF NOT EXISTS arp;
GRANT ALL ON SCHEMA arp TO d00_asset_allocation_data_migration;
GRANT ALL ON SCHEMA asset TO d00_asset_allocation_data_app;

CREATE SCHEMA IF NOT EXISTS fund;
GRANT ALL ON SCHEMA fund TO d00_asset_allocation_data_migration;
GRANT ALL ON SCHEMA asset TO d00_asset_allocation_data_app;

CREATE SCHEMA IF NOT EXISTS audit;
GRANT ALL ON SCHEMA audit TO d00_asset_allocation_data_migration;
GRANT ALL ON SCHEMA asset TO d00_asset_allocation_data_app;

CREATE SCHEMA IF NOT EXISTS lookup;
GRANT ALL ON SCHEMA lookup TO d00_asset_allocation_data_migration;
GRANT ALL ON SCHEMA asset TO d00_asset_allocation_data_app;

CREATE SCHEMA IF NOT EXISTS config;
GRANT ALL ON SCHEMA config TO d00_asset_allocation_data_migration;
GRANT ALL ON SCHEMA asset TO d00_asset_allocation_data_app;