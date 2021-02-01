INSERT INTO config.model (name, description, execution_state_id)
Values('ARP', 'Alternative Risk Premia', config.insert_execution_state('config.insert_model'))
ON CONFLICT DO NOTHING;