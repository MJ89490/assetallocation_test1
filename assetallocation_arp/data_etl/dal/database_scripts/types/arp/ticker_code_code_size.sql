DROP TYPE IF EXISTS arp.ticker_code_code_size CASCADE;
CREATE TYPE arp.ticker_code_code_size AS (
    ticker text,
    ndf_code text,
    spot_code text,
    position_size NUMERIC(32, 16)
)