DROP TYPE IF EXISTS arp.id_weight CASCADE;
CREATE TYPE arp.id_weight AS (
    id int,
    weight NUMERIC(32, 16)
)