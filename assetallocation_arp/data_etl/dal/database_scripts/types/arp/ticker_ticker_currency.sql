DROP TYPE IF EXISTS arp.ticker_ticker_currency CASCADE;
CREATE TYPE arp.ticker_ticker_currency AS (
    ppp_ticker VARCHAR,
    cash_rate_ticker VARCHAR,
    currency VARCHAR
)