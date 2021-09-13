DROP FUNCTION IF EXISTS arp.select_fund_strategy_analytics(character varying,integer,date,date);
CREATE OR REPLACE FUNCTION arp.select_fund_strategy_analytics(
  fund_name varchar,
  _strategy_id int,
  business_date_from date,
  business_date_to date
)
RETURNS TABLE(
  business_date date,
  category varchar,
  subcategory varchar,
  frequency arp.frequency,
  value numeric(32, 16),
  comparator_name varchar,
  comparator_value numeric(32, 16)
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
        f.name = select_fund_strategy_analytics.fund_name
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
        sa.business_date,
        sa.category,
        sa.subcategory,
        sa.frequency,
        sa.value,
        sa.comparator_name,
        sa.comparator_value
      FROM
        arp.strategy_analytic sa
        JOIN model_instance_cte mic on mic.model_instance_id = sa.model_instance_id
  ;
END
$$
LANGUAGE PLPGSQL;
