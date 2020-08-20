CREATE OR REPLACE FUNCTION arp.insert_fund_strategy_asset_analytics(
    fund_strategy_id int,
    analytics arp.ticker_date_category_subcategory_value[],
    execution_state_id int
)
RETURNS void
AS
$$
BEGIN
  INSERT INTO arp.fund_strategy_asset_analytic (
    fund_strategy_id,
    asset_id,
    business_date,
    category,
    subcategory,
    value,
    execution_state_id
  )
  SELECT
    insert_fund_strategy_asset_analytics.fund_strategy_id,
    a.id,
    (aa).date,
    (aa).category,
    (aa).subcategory,
    (aa).value,
    insert_fund_strategy_asset_analytics.execution_state_id
  FROM
    unnest(analytics) as aa
    JOIN asset.asset a ON (aa).ticker = a.ticker;
  RETURN;
END
$$
LANGUAGE PLPGSQL;