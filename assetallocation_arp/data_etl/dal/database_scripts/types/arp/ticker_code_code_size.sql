DROP TYPE IF EXISTS arp.ticker_code_code_size CASCADE;
CREATE TYPE arp.ticker_code_code_size AS (
    ticker VARCHAR,
    ndf_code VARCHAR,
    spot_code VARCHAR,
    position_size NUMERIC(32, 16)
)