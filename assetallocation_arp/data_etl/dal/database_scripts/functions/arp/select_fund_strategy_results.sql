--DROP FUNCTION arp.select_fund_strategy_results(character varying,character varying,timestamp with time zone,timestamp with time zone)
CREATE OR REPLACE FUNCTION arp.select_fund_strategy_results(
  fund_name varchar,
  strategy_name varchar,
  max_business_datetime timestamp with time zone,
  max_system_datetime timestamp with time zone
)
RETURNS TABLE(
  strategy_version int,
  python_code_version varchar,
  business_datetime timestamp with time zone,
  output_is_saved boolean,
  weight numeric,
  asset_ticker varchar,
  strategy_weight numeric,
  implemented_weight numeric,
  asset_analytics arp.category_subcategory_value[]
)
AS
$$
BEGIN
  RETURN QUERY
    WITH fsr (fund_strategy_id, strategy_version, business_datetime, python_code_version, output_is_saved, weight) AS (
      SELECT
        fs.id,
        COALESCE(t.version, fi.version, e.version) as strategy_version,
        fs.business_datetime,
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
        AND fs.business_datetime <= select_fund_strategy_results.max_business_datetime
        AND fs.system_datetime <= select_fund_strategy_results.max_system_datetime
      ORDER BY
        fs.system_datetime desc,
        fs.business_datetime desc
      LIMIT 1
    )
    SELECT
      fsr.strategy_version,
      fsr.python_code_version,
      fsr.business_datetime,
      fsr.output_is_saved,
      fsr.weight,
      a.ticker as asset_ticker,
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
    GROUP BY
      fsr.strategy_version,
      fsr.business_datetime,
      fsr.python_code_version,
      fsr.output_is_saved,
      fsr.weight,
      a.ticker,
      fsaw.strategy_weight,
      fsaw.implemented_weight
  ;
END
$$
LANGUAGE PLPGSQL;