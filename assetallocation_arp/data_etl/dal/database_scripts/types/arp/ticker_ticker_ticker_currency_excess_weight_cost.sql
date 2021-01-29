DROP TYPE IF EXISTS arp.ticker_ticker_ticker_currency_excess_weight_cost CASCADE;
CREATE TYPE arp.ticker_ticker_ticker_currency_excess_weight_cost AS (
    bbg_tr_ticker varchar,
    bbg_er_ticker varchar,
    cash_ticker varchar,
    currency varchar,
    is_excess boolean,
    asset_weight numeric,
    transaction_cost numeric
)