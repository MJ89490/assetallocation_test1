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
  ('auth.insert_user', 'Insert user into auth.user', 't'),
  ('config.insert_model', 'Insert model into config.model', 't')
ON CONFLICT DO NOTHING
;


