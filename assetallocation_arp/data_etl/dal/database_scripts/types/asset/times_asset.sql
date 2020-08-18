DROP TYPE IF EXISTS  asset.times_asset CASCADE;
CREATE TYPE asset.times_asset AS (
    category VARCHAR,
    country VARCHAR,
    currency VARCHAR,
    description VARCHAR,
    name VARCHAR,
    ticker VARCHAR,
    is_tr BOOLEAN,
    type VARCHAR,
    signal_ticker VARCHAR,
    future_ticker VARCHAR,
    cost NUMERIC(32, 16),
    s_leverage int
)