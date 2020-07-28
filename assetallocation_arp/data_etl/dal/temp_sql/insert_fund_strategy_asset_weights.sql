CREATE OR REPLACE FUNCTION insert_fund_strategy_asset_weights(
    fund_strategy_id int,
    asset_tickers varchar[],
    strategy_weights numeric[],
    implemented_weights numeric[],
    execution_state_id int
)
RETURNS void
AS
$$
BEGIN
  INSERT INTO arp.fund_strategy_asset_weight (
    fund_strategy_id,
    asset_id,
    strategy_weight,
    implemented_weight,
    execution_state_id
  )
  SELECT
    insert_fund_strategy_asset_weights.fund_strategy_id,
    a.id,
    aw.strategy_weight,
    aw.implemented_weight,
    insert_fund_strategy_asset_weights.execution_state_id
  FROM
    unnest(asset_tickers, strategy_weights, implemented_weights) as aw (asset_ticker, strategy_weight, implemented_weight)
    JOIN asset.asset a ON aw.asset_ticker = a.ticker;
  RETURN;
END
$$
LANGUAGE PLPGSQL;