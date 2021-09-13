INSERT INTO lookup.source (source)
VALUES ('Bloomberg'), ('IMF')
ON CONFLICT DO NOTHING
;