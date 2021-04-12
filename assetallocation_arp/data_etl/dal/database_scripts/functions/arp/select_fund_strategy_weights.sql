CREATE OR REPLACE FUNCTION arp.select_fund_strategy_weights(
  fund_name varchar,
  _strategy_id int,
  business_date_from date,
  business_date_to date
)
RETURNS TABLE(
  python_code_version varchar,
  strategy_weight numeric,
  asset_subcategory text,
  asset_currency char(3),
  business_date date,
  asset_weight_frequency arp.frequency,
  theoretical_asset_weight numeric,
  implemented_asset_weight numeric
)
AS
$$
BEGIN
  RETURN QUERY
    WITH fund_strategy_weight_cte (fund_id, weight) as (
      SELECT DISTINCT
        fsw.fund_id,
        fsw.weight
      FROM
        fund.fund f
        JOIN arp.fund_strategy_weight fsw ON fsw.fund_id = f.id
      WHERE
        f.name = select_fund_strategy_weights.fund_name
        AND fsw.strategy_id = _strategy_id
        AND upper(fsw.system_tstzrange) = 'infinity'
    ),
    fund_strategy_asset_weight_cte (
          fund_id, model_instance_id, asset_subcategory, currency, business_date, frequency, theoretical_weight,
          implemented_weight
      ) as (
      SELECT DISTINCT
        fswc.fund_id,
        saw.model_instance_id,
        ag.subcategory as asset_subcategory,
        lc.currency,
        saw.business_date,
        saw.frequency,
        saw.theoretical_weight,
        fsaw.implemented_weight
      FROM
        fund_strategy_weight_cte fswc
        JOIN arp.fund_strategy_asset_weight fsaw on fsaw.fund_id = fswc.fund_id
        JOIN arp.strategy_asset_weight saw on saw.id = fsaw.strategy_asset_weight_id
        JOIN asset.asset a on a.id = saw.asset_id
        JOIN lookup.currency lc on a.currency_id = lc.id
        JOIN asset.asset_group ag on ag.id = a.asset_group_id
      WHERE
        upper(fsaw.system_tstzrange) = 'infinity'
        AND saw.strategy_id = _strategy_id
    ),
    model_instance_cte (fund_id, model_instance_id, python_code_version) as (
      SELECT DISTINCT
        fsawc.fund_id,
        fsawc.model_instance_id,
        mi.python_code_version
      FROM
        fund_strategy_asset_weight_cte fsawc
        JOIN config.model_instance mi ON mi.id = fsawc.model_instance_id
      WHERE
        mi.business_daterange && daterange(business_date_from, business_date_to, '[]')
    )
    SELECT DISTINCT
      model_instance_cte.python_code_version,
      fund_strategy_weight_cte.weight as strategy_weight,
      fund_strategy_asset_weight_cte.asset_subcategory,
      fund_strategy_asset_weight_cte.currency as asset_currency,
      fund_strategy_asset_weight_cte.business_date,
      fund_strategy_asset_weight_cte.frequency as asset_weight_frequency,
      fund_strategy_asset_weight_cte.theoretical_weight as theoretical_asset_weight,
      fund_strategy_asset_weight_cte.implemented_weight as implemented_asset_weight
    FROM
      fund_strategy_weight_cte
      JOIN model_instance_cte on fund_strategy_weight_cte.fund_id = model_instance_cte.fund_id
      JOIN fund_strategy_asset_weight_cte on fund_strategy_asset_weight_cte.model_instance_id = model_instance_cte.model_instance_id
  ;
END
$$
LANGUAGE PLPGSQL;
