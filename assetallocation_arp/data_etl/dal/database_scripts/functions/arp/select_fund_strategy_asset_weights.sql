CREATE OR REPLACE FUNCTION arp.select_fund_strategy_asset_weights(
    fund_strategy_id int
)
RETURNS TABLE(
  asset_ticker varchar,
  strategy_weight numeric,
  implemented_weight numeric
)
AS
$$
BEGIN
  RETURN QUERY
    SELECT
      a.ticker as asset_ticker,
      strategy_weight,
      implemented_weight
    FROM
      arp.fund_strategy_asset_weight fsaw
      JOIN asset.asset a ON fsaw.asset_id = a.id
    WHERE
      fsaw.fund_strategy_id = select_fund_strategy_asset_weights.fund_strategy_id;
END
$$
LANGUAGE PLPGSQL;