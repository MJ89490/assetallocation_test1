WITH es (id) AS (SELECT * FROM config.insert_execution_state('auth.insert_user'))
INSERT INTO auth.user (name, domino_username, email, windows_username, in_use, execution_state_id)
Values
  ('Jessica Smart', 'jessica_smart', 'jessica.smart@lgim.com', 'JS89275', 't', (SELECT es.id FROM es)),
  ('Anais Jeremie', 'anais_jeremie', 'anais.jeremie@lgim.com', 'AJ89720', 't', (SELECT es.id FROM es)),
  ('Simone Nascimento', 'simone_nascimento', 'simone.nascimento@lgim.com', 'SN69248', 't', (SELECT es.id FROM es))
ON CONFLICT DO NOTHING
;
