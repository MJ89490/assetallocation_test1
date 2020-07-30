CREATE OR REPLACE FUNCTION arp.select_strategy_asset_analytics(
    fund_strategy_id int
)
RETURNS TABLE(
  asset_ticker varchar,
  type varchar,
  subtype varchar,
  value numeric
)
AS
$$
BEGIN
  RETURN QUERY
    SELECT
      ticker as asset_ticker,
      type,
      subtype,
      value
    FROM
      arp.strategy_asset_analytic saa
      JOIN asset.asset a ON saa.asset_id = a.id
    WHERE
      saa.fund_strategy_id = select_strategy_asset_analytics.fund_strategy_id;
END
$$
LANGUAGE PLPGSQL;