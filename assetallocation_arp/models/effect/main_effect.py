import sys
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
from assetallocation_arp.models.effect.write_logs_computations import remove_logs_effect

from assetallocation_arp.data_etl.inputs_effect.write_inputs_effect_excel import get_latest_date_signal_excel

"""
    Main function to run the EFFECT computations
"""

#TODO
# - tout vérifier
# - envoyer première version à Simone
# - ajouter les outputs
# - envoyer seconde version à Simnone
# - réviser code + finir excel pour derniers tests (refaire tests pour qql devise + tab controls)
# - ajouter doctrings


def run_effect(trend_inputs, combo_inputs, carry_inputs, realtime_inflation_forecast, weighting_costs,
               input_file, user_start_date='11-01-2000'):

    xw.Book(input_file).set_mock_caller()
    remove_logs_effect()

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                         EFFECT ALL CURRENCIES COMPUTATIONS                                       #
    # ---------------------------------------------------------------------------------------------------------------- #
    obj_import_data = ComputeCurrencies(bid_ask_spread=weighting_costs['bid_ask'])
    spx_index_values = obj_import_data.process_data_effect()
    obj_import_data.start_date_calculations = user_start_date

    # -------------------------- Inflation differential calculations ------------------------------------------------- #
    obj_inflation_differential = ComputeInflationDifferential(dates_index=obj_import_data.dates_index)
    inflation_differential = obj_inflation_differential.compute_inflation_differential(realtime_inflation_forecast)

    # -------------------------- Carry - Trend - Combo - Returns - Spot ---------------------------------------------- #
    carry_inputs['inflation'] = inflation_differential
    currencies_calculations = obj_import_data.run_compute_currencies(carry_inputs, trend_inputs, combo_inputs)

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                                 EFFECT OVERVIEW                                                  #
    # ---------------------------------------------------------------------------------------------------------------- #
    latest_signal_date = get_latest_date_signal_excel(obj_import_data)

    spot_origin, carry_origin = obj_import_data.process_data_config_effect()

    # -------------------------------- Aggregate Currencies ---------------------------------------------------------- #
    obj_compute_agg_currencies = ComputeAggregateCurrencies(window=weighting_costs['window'],
                                                            weight=weighting_costs['weight'],
                                                            dates_index=obj_import_data.dates_origin_index,
                                                            start_date_calculations=obj_import_data.start_date_calculations)

    aggregate_currencies = obj_compute_agg_currencies.run_aggregate_currencies(
                                                   returns_incl_costs=currencies_calculations['return_incl_curr'],
                                                   spot_origin=spot_origin,
                                                   spot_incl_costs=currencies_calculations['spot_incl_curr'],
                                                   carry_origin=carry_origin,
                                                   combo_curr=currencies_calculations['combo_curr'])

    # -------------------------- Profit and Loss overview Combo; Returns Ex costs; Spot; Carry ----------------------- #
    obj_compute_profit_and_loss_overview = ComputeProfitAndLoss(latest_date=latest_signal_date,
                                                                position_size_attribution=weighting_costs['pos_size_attr'],
                                                                index_dates=obj_import_data.dates_origin_index)

    profit_and_loss = obj_compute_profit_and_loss_overview.run_profit_and_loss(
                                                   combo_curr=currencies_calculations['combo_curr'],
                                                   returns_ex_costs=currencies_calculations['return_excl_curr'],
                                                   spot_origin=spot_origin,
                                                   total_incl_signals=aggregate_currencies['agg_total_incl_signals'],
                                                   spot_incl_signals=aggregate_currencies['agg_spot_incl_signals'],
                                                   weighted_perf=aggregate_currencies['weighted_performance'])

    # -------------------------- Signals: Combo; Returns Ex costs; Spot; Carry --------------------------------------- #
    obj_compute_signals_overview = ComputeSignalsOverview(latest_signal_date=latest_signal_date,
                                                          size_attr=weighting_costs['pos_size_attr'],
                                                          window=weighting_costs['window'],
                                                          next_latest_date=obj_import_data)

    signals_overview = obj_compute_signals_overview.run_signals_overview(
                                                    real_carry_curr=currencies_calculations['carry_curr'],
                                                    trend_curr=currencies_calculations['trend_curr'],
                                                    combo_curr=currencies_calculations['combo_curr'],
                                                    agg_total_incl_signals=aggregate_currencies['agg_total_incl_signals'],
                                                    agg_log_returns=aggregate_currencies['log_returns_excl_costs'])

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
                                                    returns_excl_signals=aggregate_currencies['agg_total_excl_signals'],
                                                    returns_incl_signals=aggregate_currencies['agg_total_incl_signals'],
                                                    spxt_index_values=spx_index_values.loc[pd.to_datetime(user_start_date, format='%d-%m-%Y'):])

    return profit_and_loss, signals_overview, trades_overview, rates_usd, rates_eur, risk_returns


if __name__ == '__main__':
    carry_inputs = {'type': 'real', 'inflation': ''}
    trend_inputs = {'short_term': 4, 'long_term': 16, 'trend': 'spot'}  # could be Spot or Total Return
    combo_inputs = {'cut_off': 2, 'incl_shorts': 'yes', 'cut_off_s': 0.00, 'threshold': 0.25}

    position_size_attribution = 0.03 * 1.33
    window_size = 52
    weight = '1/N'

    realtime_inflation_forecast = 'no'

    input_file = "arp_dashboard_effect.xlsm"

    weighting_costs = {'window': 52, 'weight': weight, 'pos_size_attr': position_size_attribution, 'bid_ask': 10}
    run_effect(trend_inputs, combo_inputs, carry_inputs, realtime_inflation_forecast, weighting_costs, input_file)
    sys.exit()

