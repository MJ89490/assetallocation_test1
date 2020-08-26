import sys
import os
import json
import pandas as pd
from configparser import ConfigParser

from assetallocation_arp.models.effect.compute_currencies import ComputeCurrencies
from data_etl.inputs_effect.compute_inflation_differential import ComputeInflationDifferential

from assetallocation_arp.models.effect.compute_profit_and_loss_overview import ComputeProfitAndLoss
from assetallocation_arp.models.effect.compute_signals_overview import ComputeSignalsOverview
from assetallocation_arp.models.effect.compute_trades_overview import compute_trades_overview
from assetallocation_arp.models.effect.compute_warning_flags_overview import ComputeWarningFlagsOverview

from assetallocation_arp.models.effect.compute_aggregate_currencies import ComputeAggregateCurrencies

"""
    Main function to run the EFFECT computations
"""


def run_effect():
    # ---------------------------------------------------------------------------------------------------------------- #
    #                                         EFFECT ALL CURRENCIES COMPUTATIONS                                       #
    # ---------------------------------------------------------------------------------------------------------------- #
    # moving_average= {"short": input("Short: "), "long": input("Long: ")}
    bid_ask_spread = 10
    obj_import_data = ComputeCurrencies(bid_ask_spread=bid_ask_spread)
    obj_import_data.process_data_effect()
    #TODO read from the config file ; ask to Simone if the date will change
    obj_import_data.start_date_calculations = '2000-01-11'

    # -------------------------- Inflation differential calculations ------------------------------------------------- #
    realtime_inflation_forecast = 'yes'
    obj_inflation_differential = ComputeInflationDifferential(dates_index=obj_import_data.dates_index)
    inflation_differential = obj_inflation_differential.compute_inflation_differential(realtime_inflation_forecast)

    # -------------------------- Carry - Trend - Combo - Returns - Spot ---------------------------------------------- #
    carry_inputs = {'type': 'nominal', 'inflation': inflation_differential}
    trend_inputs = {'short_term': 4, 'long_term': 16, 'trend': 'total return'}  # could be Spot or Total Return
    combo_inputs = {'cut_off': 2, 'incl_shorts': 'no', 'cut_off_s': 0.00, 'threshold': 0.25}
    currencies_calculations = obj_import_data.run_compute_currencies(carry_inputs, trend_inputs, combo_inputs)

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                                 EFFECT OVERVIEW                                                  #
    # ---------------------------------------------------------------------------------------------------------------- #
    latest_signal_date = pd.to_datetime('24-04-2020',  format='%d-%m-%Y')
    # latest_date = dates_index[-5]
    # dates_index[-4]
    next_latest_date = pd.to_datetime('27-04-2020',  format='%d-%m-%Y')
    previous_seven_days_latest_date = obj_import_data.dates_origin_index[-10]
    position_size_attribution = 0.03 * 1.33
    window_size = 52
    weight = 'inverse_vol'
    spot_origin, carry_origin = obj_import_data.process_data_config_effect()

    # -------------------------------- Aggregate Currencies ---------------------------------------------------------- #
    obj_compute_agg_currencies = ComputeAggregateCurrencies(window=window_size,
                                                            weight=weight,
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
                                                                position_size_attribution=position_size_attribution,
                                                                index_dates=obj_import_data.dates_origin_index)

    profit_and_loss = obj_compute_profit_and_loss_overview.run_profit_and_loss(
                                                   combo_curr=currencies_calculations['combo_curr'],
                                                   returns_ex_costs=currencies_calculations['return_excl_curr'],
                                                   spot_origin=spot_origin,
                                                   total_incl_signals=aggregate_currencies['agg_total_incl_signals'],
                                                   spot_incl_signals=aggregate_currencies['agg_spot_incl_signals'],
                                                   weighted_perf=aggregate_currencies['weighted_performance'])

    # -------------------------- Signals: Combo; Returns Ex costs; Spot; Carry --------------------------------------- #
    obj_compute_signals_overview = ComputeSignalsOverview(
                                                    next_latest_date=next_latest_date,
                                                    latest_signal_date=latest_signal_date,
                                                    size_attr=position_size_attribution,
                                                    window=window_size)

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
    obj_compute_warning_flags_overview = ComputeWarningFlagsOverview(
                                              latest_signal_date=latest_signal_date,
                                              previous_seven_days_latest_date=previous_seven_days_latest_date)
    obj_compute_warning_flags_overview.process_data_effect()
    rates_usd, rates_eur = obj_compute_warning_flags_overview.compute_warning_flags_rates()

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                            EFFECT RISK RETURN CALCULATIONS                                       #
    # ---------------------------------------------------------------------------------------------------------------- #

    from assetallocation_arp.models.compute_risk_return_calculations import ComputeRiskReturnCalculations

    obj_compute_risk_return_calculations = ComputeRiskReturnCalculations(
                                                    start_date=obj_import_data.start_date_calculations,
                                                    end_date=obj_import_data.dates_origin_index[-1],
                                                    dates_index=obj_import_data.dates_origin_index)

    obj_compute_risk_return_calculations.run_compute_risk_return_calculations(
                                                    returns_excl_signals=aggregate_currencies['agg_total_excl_signals'],
                                                    returns_incl_signals=aggregate_currencies['agg_total_incl_signals'])


if __name__ == '__main__':
    sys.exit(run_effect())
