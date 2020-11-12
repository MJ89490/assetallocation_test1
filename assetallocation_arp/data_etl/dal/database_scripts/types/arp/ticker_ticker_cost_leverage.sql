DROP TYPE IF EXISTS arp.asset_ticker_ticker_cost_leverage CASCADE;
CREATE TYPE arp.asset_ticker_ticker_cost_leverage AS (
    asset_subcategory VARCHAR,
    signal_ticker VARCHAR,
    future_ticker VARCHAR,
    cost NUMERIC(32, 16),
    s_leverage int
)