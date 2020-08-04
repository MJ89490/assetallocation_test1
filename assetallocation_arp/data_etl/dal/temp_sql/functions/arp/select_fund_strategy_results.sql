CREATE OR REPLACE FUNCTION arp.select_fund_strategy_results(
  fund_name varchar,
  strategy_name varchar,
  business_datetime timestamp with time zone,
  system_datetime timestamp with time zone
)
RETURNS TABLE(
  save_output_flag boolean,
  weight numeric,
  asset_ticker varchar,
  strategy_weight numeric,
  implemented_weight numeric,
  asset_analytics arp.type_subtype_value[]
)
AS
$$
BEGIN
  RETURN QUERY
    WITH fsr (fund_strategy_id, save_output_flag, weight) AS (
      SELECT
        fs.id,
        fs.save_output_flag,
        fs.weight
      FROM
        fund.fund f
        JOIN arp.fund_strategy fs
        ON f.id = fs.fund_id
        JOIN arp.strategy s
        ON fs.strategy_id = s.id
      WHERE
        f.name = select_fund_strategy_results.fund_name
        AND s.name = select_fund_strategy_results.strategy_name
        AND fs.business_datetime <= select_fund_strategy_results.business_datetime
        AND fs.system_datetime <= select_fund_strategy_results.system_datetime
      ORDER BY
        fs.system_datetime desc,
        fs.business_datetime desc
      LIMIT 1
    )
    SELECT
      fsr.save_output_flag,
      fsr.weight,
      a.ticker as asset_ticker,
      fsaw.strategy_weight,
      fsaw.implemented_weight,
      array_agg((saa.type, saa.subtype, saa.value):: arp.type_subtype_value) as asset_analytics
    FROM
      arp.fund_strategy_asset_weight fsaw
      JOIN asset.asset a ON fsaw.asset_id = a.id
      JOIN fsr ON fsaw.fund_strategy_id = fsr.fund_strategy_id
      JOIN arp.strategy_asset_analytic saa
          ON saa.fund_strategy_id = fsr.fund_strategy_id
          AND saa.asset_id = fsaw.asset_id
          AND saa.asset_id = a.id
    GROUP BY
      fsr.save_output_flag,
      fsr.weight,
      a.ticker,
      fsaw.strategy_weight,
      fsaw.implemented_weight
  ;
END
$$
LANGUAGE PLPGSQL;