CREATE OR REPLACE FUNCTION arp.select_strategy_asset_analytics(
    fund_strategy_id int
)
RETURNS TABLE(
  asset_ticker varchar,
  business_date date,
  type varchar,
  subtype varchar,
  value numeric
)
AS
$$
BEGIN
  RETURN QUERY
    SELECT
      a.ticker as asset_ticker,
      fsaa.business_date,
      fsaa.category,
      fsaa.subcategory,
      fsaa.value
    FROM
      arp.fund_strategy_asset_analytic fsaa
      JOIN asset.asset a ON fsaa.asset_id = a.id
    WHERE
      fsaa.fund_strategy_id = arp.select_strategy_asset_analytics.fund_strategy_id;
END
$$
LANGUAGE PLPGSQL;