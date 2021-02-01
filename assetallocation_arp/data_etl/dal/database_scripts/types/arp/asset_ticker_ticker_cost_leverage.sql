DROP TYPE IF EXISTS arp.ticker_ticker_cost_leverage CASCADE;
CREATE TYPE arp.ticker_ticker_cost_leverage AS (
    signal_ticker VARCHAR,
    future_ticker VARCHAR,
    cost NUMERIC(32, 16),
    s_leverage int
)