CREATE OR REPLACE FUNCTION arp.insert_strategy_asset_analytics(
    fund_strategy_id int,
    asset_tickers varchar[],
    analytic_types varchar[],
    analytic_subtypes varchar[],
    analytic_values numeric[],
    execution_state_id int
)
RETURNS void
AS
$$
BEGIN
  if not (array_ndims(asset_tickers) =1 and array_ndims(analytic_types) = 1 and array_ndims(analytic_subtypes) = 1 and array_ndims(analytic_values) = 1) then
    RAISE 'asset_tickers, analytic_types, analytic_subtypes and analytic_values must all be 1 dimensional arrays';
  elsif not (
    array_length(asset_tickers, 1) = array_length(analytic_types, 1)
    and array_length(analytic_types, 1) = array_length(analytic_subtypes, 1)
    and array_length(analytic_subtypes, 1) = array_length(analytic_values, 1)
  ) then
    RAISE 'asset_tickers, analytic_types, analytic_subtypes and analytic_values must all be the same length';
  end if;

  INSERT INTO arp.strategy_asset_analytic (
    fund_strategy_id,
    asset_id,
    type,
    subtype,
    value,
    execution_state_id
  )
  SELECT
    insert_strategy_asset_analytics.fund_strategy_id,
    a.id,
    aa.type,
    aa.subtype,
    aa.value,
    insert_strategy_asset_analytics.execution_state_id
  FROM
    unnest(asset_tickers, analytic_types, analytic_subtypes, analytic_values) as aa (asset_ticker, type, subtype, value)
    JOIN asset.asset a ON aa.asset_ticker = a.ticker;
  RETURN;
END
$$
LANGUAGE PLPGSQL;