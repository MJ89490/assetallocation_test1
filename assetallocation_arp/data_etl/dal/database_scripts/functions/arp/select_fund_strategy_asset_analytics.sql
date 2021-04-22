CREATE OR REPLACE FUNCTION arp.select_fund_strategy_asset_analytics(
  fund_name varchar,
  _strategy_id int,
  business_date_from date,
  business_date_to date
)
RETURNS TABLE(
  asset_ticker varchar,
  asset_name varchar,
  asset_subcategory text,
  business_date date,
  category varchar,
  subcategory varchar,
  frequency arp.frequency,
  value numeric(32, 16)
)
AS
$$
BEGIN
  RETURN QUERY
    WITH fund_cte (fund_id) as (
      SELECT DISTINCT
        f.id as fund_id
      FROM
        fund.fund f
      WHERE
        f.name = select_fund_strategy_asset_analytics.fund_name
    ),
    fund_strategy_asset_weight_cte (model_instance_id) as (
      SELECT DISTINCT
        saw.model_instance_id
      FROM
        fund_cte fswc
        JOIN arp.fund_strategy_asset_weight fsaw on fsaw.fund_id = fswc.fund_id
        JOIN arp.strategy_asset_weight saw on saw.id = fsaw.strategy_asset_weight_id
      WHERE
        upper(fsaw.system_tstzrange) = 'infinity'
        AND saw.strategy_id = _strategy_id
    ),
    model_instance_cte (model_instance_id) as (
      SELECT DISTINCT
        fsawc.model_instance_id
      FROM
        fund_strategy_asset_weight_cte fsawc
        JOIN config.model_instance mi ON mi.id = fsawc.model_instance_id
      WHERE
         mi.business_daterange && daterange(business_date_from, business_date_to, '[]')
      )
      SELECT DISTINCT
        a.ticker as asset_ticker,
        a.name as asset_name,
        ag.subcategory as asset_subcategory,
        saa.business_date,
        saa.category,
        saa.subcategory,
        saa.frequency,
        saa.value
      FROM
        arp.strategy_asset_analytic saa
        JOIN model_instance_cte mic on mic.model_instance_id = saa.model_instance_id
        JOIN asset.asset a on a.id = saa.asset_id
        JOIN asset.asset_group ag on ag.id = a.asset_group_id
  ;
END
$$
LANGUAGE PLPGSQL;
