DROP TYPE IF EXISTS arp.ticker_ticker_currency CASCADE;
CREATE TYPE arp.ticker_ticker_currency AS (
    ppp_ticker text,
    cash_ticker text,
    currency text
)