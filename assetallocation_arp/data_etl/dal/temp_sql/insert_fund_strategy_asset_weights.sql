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
  if not (array_ndims(asset_tickers) =1 and array_ndims(strategy_weights) = 1 and array_ndims(implemented_weights) = 1) then
    RAISE 'asset_tickers, strategy_weights and implemented_weights must all be 1 dimensional arrays';
  elsif not (array_length(asset_tickers, 1) = array_length(strategy_weights, 1) and array_length(strategy_weights, 1) = array_length(implemented_weights, 1)) then
    RAISE 'asset_tickers, strategy_weights and implemented_weights must all be the same length';
  end if;

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