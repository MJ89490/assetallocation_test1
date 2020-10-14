CREATE OR REPLACE FUNCTION arp.select_fund_strategy_results(
  fund_name varchar,
  strategy_name varchar,
  strategy_version int
)
RETURNS TABLE(
  python_code_version varchar,
  output_is_saved boolean,
  weight numeric,
  asset_ticker varchar,
  asset_category varchar,
  asset_subcategory varchar,
  business_date date,
  strategy_weight numeric,
  implemented_weight numeric,
  asset_analytics arp.category_subcategory_value[]
)
AS
$$
BEGIN
  RETURN QUERY
    WITH fsr (fund_strategy_id, python_code_version, output_is_saved, weight) AS (
      SELECT
        fs.id,
        fs.python_code_version,
        fs.output_is_saved,
        fs.weight
      FROM
        fund.fund fu
        JOIN arp.fund_strategy fs
        ON fu.id = fs.fund_id
        JOIN arp.strategy s
        ON fs.strategy_id = s.id
        FULL OUTER JOIN arp.times t on s.id = t.strategy_id
        FULL OUTER JOIN arp.fica fi on s.id = fi.strategy_id
        FULL OUTER JOIN arp.effect e on s.id = e.strategy_id
      WHERE
        fu.name = select_fund_strategy_results.fund_name
        AND s.name = select_fund_strategy_results.strategy_name
        AND COALESCE(t.version, fi.version, e.version) = select_fund_strategy_results.strategy_version
      ORDER BY
        fs.system_datetime desc
    )
    SELECT
      fsr.python_code_version,
      fsr.output_is_saved,
      fsr.weight,
      a.ticker as asset_ticker,
      a.category as asset_category,
      a.subcategory as asset_subcategory,
      fsaw.business_date,
      fsaw.strategy_weight,
      fsaw.implemented_weight,
      array_agg((fsaa.category, fsaa.subcategory, fsaa.value):: arp.category_subcategory_value) as asset_analytics
    FROM
      arp.fund_strategy_asset_weight fsaw
      JOIN asset.asset a ON fsaw.asset_id = a.id
      JOIN fsr ON fsaw.fund_strategy_id = fsr.fund_strategy_id
      JOIN arp.fund_strategy_asset_analytic fsaa
          ON fsaa.fund_strategy_id = fsr.fund_strategy_id
          AND fsaa.asset_id = fsaw.asset_id
          AND fsaa.asset_id = a.id
          AND fsaa.business_date = fsaw.business_date
    GROUP BY
      fsr.python_code_version,
      fsr.output_is_saved,
      fsr.weight,
      a.ticker,
      a.category,
      a.subcategory,
      fsaw.business_date,
      fsaw.strategy_weight,
      fsaw.implemented_weight
  ;
END
$$
LANGUAGE PLPGSQL;