import xlwings as xw
import pandas as pd

from assetallocation_arp.models.effect.compute_currencies import ComputeCurrencies

from data_etl.inputs_effect.compute_inflation_differential import ComputeInflationDifferential

from assetallocation_arp.models.effect.compute_profit_and_loss_overview import ComputeProfitAndLoss
from assetallocation_arp.models.effect.compute_signals_overview import ComputeSignalsOverview
from assetallocation_arp.models.effect.compute_trades_overview import compute_trades_overview
from assetallocation_arp.models.effect.compute_warning_flags_overview import ComputeWarningFlagsOverview

from assetallocation_arp.models.effect.compute_aggregate_currencies import ComputeAggregateCurrencies
from assetallocation_arp.models.compute_risk_return_calculations import ComputeRiskReturnCalculations
from data_etl.outputs_effect.write_logs_computations_effect import remove_logs_effect

from assetallocation_arp.data_etl.inputs_effect.write_inputs_effect_excel import get_latest_date_signal_excel

"""
    Main function to run the EFFECT computations
"""

#TODO
# - derniers tests (refaire tests pour qql devise + tab controls)
# - ajouter fct pour matlab
# - ajouter doctrings
# - envoyer version à Simone


def run_effect(inputs_effect, input_file):

    xw.Book(input_file).set_mock_caller()
    remove_logs_effect()

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                         EFFECT ALL CURRENCIES COMPUTATIONS                                       #
    # ---------------------------------------------------------------------------------------------------------------- #
    obj_import_data = ComputeCurrencies(bid_ask_spread=inputs_effect['weighting_costs']['bid_ask'])
    spx_index_values = obj_import_data.process_data_effect()
    obj_import_data.start_date_calculations = inputs_effect['user_start_date']

    # -------------------------- Inflation differential calculations ------------------------------------------------- #
    obj_inflation_differential = ComputeInflationDifferential(dates_index=obj_import_data.dates_index)
    inflation_differential = obj_inflation_differential.compute_inflation_differential(inputs_effect['realtime_inflation_forecast'])

    # -------------------------- Carry - Trend - Combo - Returns - Spot ---------------------------------------------- #
    inputs_effect['carry_inputs']['inflation'] = inflation_differential
    currencies_calculations = obj_import_data.run_compute_currencies(inputs_effect['carry_inputs'],
                                                                     inputs_effect['trend_inputs'],
                                                                     inputs_effect['combo_inputs'])

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                                 EFFECT OVERVIEW                                                  #
    # ---------------------------------------------------------------------------------------------------------------- #
    latest_signal_date = get_latest_date_signal_excel(obj_import_data)

    spot_origin, carry_origin = obj_import_data.process_data_config_effect()

    # -------------------------------- Aggregate Currencies ---------------------------------------------------------- #
    obj_compute_agg_currencies = ComputeAggregateCurrencies(window=inputs_effect['weighting_costs']['window'],
                                                            weight=inputs_effect['weighting_costs']['weight'],
                                                            dates_index=obj_import_data.dates_origin_index,
                                                            start_date_calculations=obj_import_data.start_date_calculations)

    agg_currencies = obj_compute_agg_currencies.run_aggregate_currencies(
                                                   returns_incl_costs=currencies_calculations['return_incl_curr'],
                                                   spot_origin=spot_origin,
                                                   spot_incl_costs=currencies_calculations['spot_incl_curr'],
                                                   carry_origin=carry_origin,
                                                   combo_curr=currencies_calculations['combo_curr'])

    # -------------------------- Profit and Loss overview Combo; Returns Ex costs; Spot; Carry ----------------------- #
    obj_compute_profit_and_loss_overview = ComputeProfitAndLoss(latest_date=latest_signal_date,
                                                                position_size_attribution=inputs_effect['weighting_costs']['pos_size_attr'],
                                                                index_dates=obj_import_data.dates_origin_index)

    profit_and_loss = obj_compute_profit_and_loss_overview.run_profit_and_loss(
                                                   combo_curr=currencies_calculations['combo_curr'],
                                                   returns_ex_costs=currencies_calculations['return_excl_curr'],
                                                   spot_origin=spot_origin,
                                                   total_incl_signals=agg_currencies['agg_total_incl_signals'],
                                                   spot_incl_signals=agg_currencies['agg_spot_incl_signals'],
                                                   weighted_perf=agg_currencies['weighted_performance'])

    # -------------------------- Signals: Combo; Returns Ex costs; Spot; Carry --------------------------------------- #
    obj_compute_signals_overview = ComputeSignalsOverview(latest_signal_date=latest_signal_date,
                                                          size_attr=inputs_effect['weighting_costs']['pos_size_attr'],
                                                          window=inputs_effect['weighting_costs']['window'],
                                                          next_latest_date=obj_import_data)

    signals_overview = obj_compute_signals_overview.run_signals_overview(
                                                    real_carry_curr=currencies_calculations['carry_curr'],
                                                    trend_curr=currencies_calculations['trend_curr'],
                                                    combo_curr=currencies_calculations['combo_curr'],
                                                    agg_total_incl_signals=agg_currencies['agg_total_incl_signals'],
                                                    agg_log_returns=agg_currencies['log_returns_excl_costs'])

    # -------------------------- Trades: Combo ----------------------------------------------------------------------- #
    trades_overview = compute_trades_overview(profit_and_loss_combo_overview=profit_and_loss['profit_and_loss_combo_overview'],
                                              signals_combo_overview=signals_overview['signals_combo_overview'])

    # -------------------------- Warning Flags: Rates; Inflation ----------------------------------------------------- #
    obj_compute_warning_flags_overview = ComputeWarningFlagsOverview(latest_signal_date=latest_signal_date,
                                                                     prev_7_days_from_latest_signal_date=obj_import_data)
    obj_compute_warning_flags_overview.process_data_effect()
    rates_usd, rates_eur = obj_compute_warning_flags_overview.compute_warning_flags_rates()

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                            EFFECT RISK RETURN CALCULATIONS                                       #
    # ---------------------------------------------------------------------------------------------------------------- #
    obj_compute_risk_return_calculations = ComputeRiskReturnCalculations(
                                                    start_date=obj_import_data.start_date_calculations,
                                                    end_date=obj_import_data.dates_origin_index[-1],
                                                    dates_index=obj_import_data.dates_origin_index)

    risk_returns = obj_compute_risk_return_calculations.run_compute_risk_return_calculations(
                                                    returns_excl_signals=agg_currencies['agg_total_excl_signals'],
                                                    returns_incl_signals=agg_currencies['agg_total_incl_signals'],
                                                    spxt_index_values=spx_index_values.loc[pd.to_datetime(
                                                        inputs_effect['user_start_date'], format='%d-%m-%Y'):])

    effect_outputs = {'profit_and_loss': profit_and_loss, 'signals_overview': signals_overview,
                      'trades_overview': trades_overview, 'rates_usd': rates_usd, 'rates_eur': rates_eur,
                      'risk_returns': risk_returns, 'combo': currencies_calculations['combo_curr'],
                      'total_excl_signals': agg_currencies['agg_total_excl_signals'],
                      'total_incl_signals': agg_currencies['agg_total_incl_signals'],
                      'spot_incl_signals': agg_currencies['agg_spot_incl_signals'],
                      'spot_excl_signals': agg_currencies['agg_spot_excl_signals']}

    return effect_outputs
