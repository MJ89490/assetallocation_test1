CREATE OR REPLACE FUNCTION arp.insert_fund_strategy_asset_weights(
    fund_strategy_id int,
    weights arp.ticker_date_weight_weight[],
    execution_state_id int
)
RETURNS void
AS
$$
BEGIN
  INSERT INTO arp.fund_strategy_asset_weight (
    fund_strategy_id,
    asset_id,
    business_date,
    strategy_weight,
    implemented_weight,
    execution_state_id
  )
  SELECT
    insert_fund_strategy_asset_weights.fund_strategy_id,
    a.id,
    (aw).date,
    (aw).strategy_weight,
    (aw).implemented_weight,
    insert_fund_strategy_asset_weights.execution_state_id
  FROM
    unnest(weights) as aw
    JOIN asset.asset a ON (aw).ticker = a.ticker;
  RETURN;
END
$$
LANGUAGE PLPGSQL;