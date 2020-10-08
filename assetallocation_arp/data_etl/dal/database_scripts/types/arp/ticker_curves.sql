DROP TYPE IF EXISTS arp.ticker_curves CASCADE;
CREATE TYPE arp.ticker_curves AS (
    asset_ticker varchar,
    sovereign_ticker curve.ticker_months_years,
    swap_ticker curve.ticker_months_years,
    swap_cr_ticker curve.ticker_months_years
)