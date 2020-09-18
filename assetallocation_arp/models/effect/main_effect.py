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

from assetallocation_arp.data_etl.inputs_effect.get_inputs_effect_excel import get_latest_date_signal_excel

from assetallocation_arp.data_etl.inputs_effect.get_inputs_effect_excel import get_user_date_effect_excel

"""
    Main function to run the EFFECT computations
"""


def run_effect(strategy_inputs, input_file, asset_inputs):

    xw.Book(input_file).set_mock_caller()
    remove_logs_effect()

    user_date = get_user_date_effect_excel(input_file)

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                         EFFECT ALL CURRENCIES COMPUTATIONS                                       #
    # ---------------------------------------------------------------------------------------------------------------- #
    obj_import_data = ComputeCurrencies(bid_ask_spread=strategy_inputs['Bid-ask spread (bp)'][1],
                                        frequency_mat=strategy_inputs['Frequency'][1], start_date_mat=strategy_inputs['StartDate'][1],
                                        signal_day_mat=strategy_inputs['SignalDay'][1], asset_inputs=asset_inputs)
    spx_index_values = obj_import_data.process_data_effect()
    obj_import_data.start_date_calculations = user_date

    # -------------------------- Inflation differential calculations ------------------------------------------------- #
    obj_inflation_differential = ComputeInflationDifferential(dates_index=obj_import_data.dates_index)

    inflation_differential = obj_inflation_differential.compute_inflation_differential(
                             strategy_inputs['Realtime Inflation Forecast'][1], obj_import_data.all_currencies_spot,
                             obj_import_data.currencies_spot['currencies_spot_usd'])

    # -------------------------- Carry - Trend - Combo - Returns - Spot ---------------------------------------------- #
    carry_inputs = {'type': strategy_inputs['Real/Nominal'][1].strip().lower(), 'inflation': inflation_differential}
    trend_inputs = {'short_term': int(strategy_inputs['Short-term MA'][1]), 'long_term': int(strategy_inputs['Long-term MA'][1]), 'trend': strategy_inputs['TrendIndicator'][1].strip().lower()}
    combo_inputs = {'cut_off': float(strategy_inputs['Interest rate cut-off (long)'][1])*100, 'incl_shorts': strategy_inputs['Include Shorts'][1].strip().lower(), 'cut_off_s': float(strategy_inputs['Interest rate cut-off (short)'][1])*100, 'threshold': float(strategy_inputs['Threshold for closing'][1])*100}

    currencies_calculations = obj_import_data.run_compute_currencies(carry_inputs, trend_inputs, combo_inputs)

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                                 EFFECT OVERVIEW                                                  #
    # ---------------------------------------------------------------------------------------------------------------- #
    latest_signal_date = get_latest_date_signal_excel(obj_import_data)

    spot_origin, carry_origin = obj_import_data.process_data_config_effect()

    # -------------------------------- Aggregate Currencies ---------------------------------------------------------- #
    obj_compute_agg_currencies = ComputeAggregateCurrencies(window=int(strategy_inputs['STDev window (weeks)'][1]),
                                                            weight=strategy_inputs['Risk-weighting'][1].strip(),
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
                                                                position_size_attribution=float(strategy_inputs['Position size (for attribution)'][1]),
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
                                                          size_attr=float(strategy_inputs['Position size (for attribution)'][1]),
                                                          window=int(strategy_inputs['STDev window (weeks)'][1]),
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
                                                                     prev_7_days_from_latest_signal_date=obj_import_data,
                                                                     asset_inputs=asset_inputs)
    obj_compute_warning_flags_overview.process_data_effect()
    rates = obj_compute_warning_flags_overview.compute_warning_flags_rates()

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
                                                    spxt_index_values=spx_index_values.loc[pd.to_datetime(user_date, format='%d-%m-%Y'):])

    effect_outputs = {'profit_and_loss': profit_and_loss, 'signals_overview': signals_overview,
                      'trades_overview': trades_overview, 'rates': rates,
                      'risk_returns': risk_returns, 'combo': currencies_calculations['combo_curr'],
                      'total_excl_signals': agg_currencies['agg_total_excl_signals'],
                      'total_incl_signals': agg_currencies['agg_total_incl_signals'],
                      'spot_incl_signals': agg_currencies['agg_spot_incl_signals'],
                      'spot_excl_signals': agg_currencies['agg_spot_excl_signals']}

    return effect_outputs
