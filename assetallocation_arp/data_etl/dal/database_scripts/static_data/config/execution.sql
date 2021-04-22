INSERT INTO config.execution (name, description, in_use)
VALUES
  ('arp.insert_times_strategy', 'Insert times strategy', 't'),
  ('arp.insert_times_assets', 'Insert times assets into arp.times_asset and asset.asset', 't'),
  ('arp.insert_fx_strategy', 'Insert fx strategy', 't'),
  ('arp.insert_fx_assets', 'Insert fx assets into arp.fx_asset and asset.asset', 't'),
  ('arp.insert_effect_strategy', 'Insert effect strategy', 't'),
  ('arp.insert_effect_assets', 'Insert effect assets into arp.effect_asset and asset.asset', 't'),
  ('arp.insert_fica_strategy', 'Insert fica strategy', 't'),
  ('arp.insert_fica_assets', 'Insert fica assets into arp.fica_asset arp.fica_asset_group and asset.asset', 't'),
  ('arp.insert_maven_strategy', 'Insert maven strategy', 't'),
  ('arp.insert_maven_assets', 'Insert maven assets into arp.maven_asset and asset.asset', 't'),
  ('arp.insert_fund_strategy_results', 'Insert fund strategy results', 't'),
  ('fund.insert_fund', 'Insert fund', 't'),
  ('arp.insert_app_user', 'Insert app user into arp.app_user', 't'),
  ('config.insert_model', 'Insert model into config.model', 't'),
  ('config.insert_asset_analytic', 'Insert asset analytic into config.asset_analytic', 't'),
  ('staging.load_assets', 'Load assets from staging.asset into asset.asset, asset.asset_group and asset.asset_analytic', 't'),
  ('staging.load_asset_analytics', 'Load asset_analytics from staging.asset_analytic into asset.asset_analytic', 't')
ON CONFLICT DO NOTHING
;

