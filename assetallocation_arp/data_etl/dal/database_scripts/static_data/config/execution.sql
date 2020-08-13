-- TODO add stored proc names and improve descriptions
INSERT INTO config.execution(name, description, in_use)
VALUES
  ('arp.insert_times_strategy', 'Insert times strategy', 't'),
  ('arp.insert_fund_strategy_results', 'Insert fund strategy results', 't'),
  ('fund.insert_fund', 'Insert fund', 't'),
  ('arp.insert_times_assets', 'Insert times assets into arp.times_asset and asset.asset', 't')
;

