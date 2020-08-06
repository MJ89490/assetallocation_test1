CREATE TYPE arp.ticker_weight_weight AS (
  ticker varchar,
  strategy_weight numeric(32, 16),
  implemented_weight numeric(32, 16)
);