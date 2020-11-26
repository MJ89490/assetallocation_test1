DROP TYPE IF EXISTS arp.currency_ticker_ticker_ticker_weight_base_region CASCADE;
CREATE TYPE arp.currency_ticker_ticker_ticker_weight_base_region AS (
    currency VARCHAR,
    ticker_3m VARCHAR,
    spot_ticker VARCHAR,
    carry_ticker VARCHAR,
    usd_weight NUMERIC(32, 16),
    base VARCHAR,
    region VARCHAR
)