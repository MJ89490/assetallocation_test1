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
  weight_frequency frequency,
  strategy_weight numeric,
  implemented_weight numeric,
  analytics arp.aggregation_category_subcategory_frequency_value[]
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
      fsa.business_date,
      fsaw.frequency as weight_frequency,
      fsaw.strategy_weight,
      fsaw.implemented_weight,
      array_agg(
            (fsa.aggregation_level, fsa.category, fsa.subcategory, fsa.frequency, fsa.value)
            :: arp.aggregation_category_subcategory_frequency_value
          ) as analytics
    FROM
      fsr
      JOIN arp.fund_strategy_analytic fsa ON fsa.fund_strategy_id = fsr.fund_strategy_id
      LEFT JOIN arp.fund_strategy_asset_weight fsaw
          ON fsaw.fund_strategy_id = fsr.fund_strategy_id
          AND fsaw.asset_id = fsa.asset_id
          AND fsaw.business_date = fsa.business_date
      JOIN asset.asset a ON fsaw.asset_id = a.id
    GROUP BY
      fsr.python_code_version,
      fsr.output_is_saved,
      fsr.weight,
      a.ticker,
      a.category,
      a.subcategory,
      fsa.business_date,
      fsaw.frequency,
      fsaw.strategy_weight,
      fsaw.implemented_weight
  ;
END
$$
LANGUAGE PLPGSQL;