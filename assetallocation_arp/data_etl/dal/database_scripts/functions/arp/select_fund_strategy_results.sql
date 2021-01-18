-- TODO check filtering and test the code below
CREATE OR REPLACE FUNCTION arp.select_fund_strategy_results(
  fund_name varchar,
  strategy_name varchar,
  strategy_version int,
  business_tstzrange tstzrange
)
RETURNS TABLE(
  python_code_version varchar,
  strategy_weight numeric,
  asset_subcategory varchar,
  business_date date,
  asset_weight_frequency frequency,
  theoretical_asset_weight numeric,
  implemented_asset_weight numeric,
  strategy_analytics arp.category_subcategory_frequency_value_comp_name_comp_value,
  strategy_asset_analytics arp.category_subcategory_frequency_value
)
AS
$$
DECLARE
  strategy_id int;
BEGIN
  select arp.select_strategy_id(strategy_name, strategy_version) into strategy_id;

  RETURN QUERY
    WITH fund_strategy_weight_cte (fund_id, weight) as (
      SELECT
        fsw.fund_id,
        fsw.weight
      FROM
        fund.fund f
        JOIN arp.fund_strategy_weight fsw ON fsw.fund_id = f.id
      WHERE
        f.name = select_fund_strategy_results.fund_name
        AND fsw.strategy_id = select_fund_strategy_results.strategy_id
        AND upper_inf(fsw.system_tstzrange)
    ),
    fund_strategy_asset_weight_cte (fund_id, model_instance_id, asset_subcategory, business_date, frequency, theoretical_weight, implemented_weight) as (
      SELECT
        fswc.fund_id,
        saw.model_instance_id,
        ag.subcategory as asset_subcategory,
        saw.business_date,
        saw.frequency,
        saw.theoretical_weight,
        fsaw.implemented_weight
      FROM
        fund_strategy_weight_cte fswc
        JOIN arp.fund_strategy_asset_weight fsaw on fsaw.fund_id = fswc.fund_id
        JOIN arp.strategy_asset_weight saw on saw.id = fsaw.strategy_asset_weight_id
        JOIN asset.asset a on a.id = saw.asset_id
        JOIN asset.asset_group ag on ag.id = a.asset_group_id
      WHERE
        upper_inf(fsaw.system_tstzrange)
        AND saw.strategy_id = select_fund_strategy_results.strategy_id
    ),
    model_instance_cte (fund_id, model_instance_id, python_code_version) as (
      SELECT
        fund_id,
        model_instance_id,
        python_code_version
      FROM
        fund_strategy_asset_weight_cte fsawc
        JOIN config.model_instance mi ON mi.id = fsawc.model_instance_id
      WHERE
        mi.business_tstzrange = select_fund_strategy_results.business_tstzrange
      ),
    strategy_analytic_cte (model_instance_id, business_date, category, subcategory, frequency, value, comparator_name, comparator_value) as (
      SELECT
        sa.model_instance_id,
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
    ),
    strategy_asset_analtyic_cte (model_instance_id, asset_subcategory, business_date, category, subcategory, frequency, value) as (
      SELECT
        saa.model_instance_id,
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
      )
    SELECT
      model_instance_cte.python_code_version,
      fund_strategy_weight_cte.weight as strategy_weight,
      fund_strategy_asset_weight_cte.asset_subcategory,
      fund_strategy_asset_weight_cte.business_date,
      fund_strategy_asset_weight_cte.frequency as asset_weight_frequency,
      fund_strategy_asset_weight_cte.theoretical_weight as theoretical_asset_weight,
      fund_strategy_asset_weight_cte.implemented_weight as implemented_asset_weight,
      array_agg(
          (
            strategy_analytic_cte.category,
            strategy_analytic_cte.subcategory,
            strategy_analytic_cte.frequency,
            strategy_analytic_cte.value,
            strategy_analytic_cte.comparator_name,
            strategy_analytic_cte.comparator_value
          )
          :: arp.category_subcategory_frequency_value_comp_name_comp_value
        ) as strategy_analytics,
        array_agg(
          (
            strategy_asset_analtyic_cte.category,
            strategy_asset_analtyic_cte.subcategory,
            strategy_asset_analtyic_cte.frequency,
            strategy_asset_analtyic_cte.value
          )
          :: arp.category_subcategory_frequency_value
        ) as strategy_asset_analytics
      FROM
        fund_strategy_weight_cte
        JOIN model_instance_cte on fund_strategy_weight_cte.fund_id = model_instance_cte.fund_id
        JOIN strategy_analytic_cte on strategy_analytic_cte.model_instance_id = model_instance_cte.model_instance_id
        JOIN fund_strategy_asset_weight_cte on fund_strategy_asset_weight_cte.model_instance_id = model_instance_cte.model_instance_id
        JOIN strategy_asset_analtyic_cte
          ON fund_strategy_asset_weight_cte.model_instance_id = fund_strategy_asset_weight_cte.model_instance_id
          AND fund_strategy_asset_weight_cte.asset_subcategory = fund_strategy_asset_weight_cte.asset_subcategory
          AND fund_strategy_asset_weight_cte.business_date = fund_strategy_asset_weight_cte.business_date
  ;
END
$$
LANGUAGE PLPGSQL;
