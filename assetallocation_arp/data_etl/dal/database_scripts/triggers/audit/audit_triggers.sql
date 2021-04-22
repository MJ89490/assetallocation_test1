SELECT audit.audit_table('asset.asset', 't', 't');
SELECT audit.audit_table('asset.asset_group', 't', 't');
SELECT audit.audit_table('arp.strategy_asset_analytic', 't', 't');
SELECT audit.audit_table('arp.strategy_asset_weight', 't', 't');
SELECT audit.audit_table('arp.strategy_analytic', 't', 't');
-- TODO decide if any other tables need to be audited