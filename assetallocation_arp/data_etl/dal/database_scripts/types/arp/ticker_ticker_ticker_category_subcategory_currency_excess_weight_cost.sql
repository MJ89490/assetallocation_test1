DROP TYPE IF EXISTS arp.ticker_ticker_ticker_category_subcategory_currency_excess_weight_cost CASCADE;
CREATE TYPE arp.ticker_ticker_ticker_category_subcategory_currency_excess_weight_cost AS (
    bbg_tr_ticker integer,
    bbg_er_ticker integer,
    cash_ticker integer,
    asset_category varchar,
    asset_subcategory varchar,
    currency varchar,
    is_excess boolean,
    asset_weight numeric,
    transaction_cost numeric
)