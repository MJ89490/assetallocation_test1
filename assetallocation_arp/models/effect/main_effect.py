import sys
import os
import json
import pandas as pd
from configparser import ConfigParser

from assetallocation_arp.models.effect.compute_currencies import ComputeCurrencies
from data_etl.inputs_effect.compute_inflation_differential import ComputeInflationDifferential

from assetallocation_arp.models.effect.compute_profit_and_loss_overview_overview import ComputeProfitAndLoss
from assetallocation_arp.models.effect.compute_signals_overview import ComputeSignalsOverview
from assetallocation_arp.models.effect.compute_trades_overview import compute_trades_overview
from assetallocation_arp.models.effect.compute_warning_flags_overview import ComputeWarningFlagsOverview


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
    obj_import_data.start_date_calculations = '2000-01-11'

    # -------------------------- Inflation differential calculations ------------------------------------------------- #
    obj_inflation_differential = ComputeInflationDifferential(dates_index=obj_import_data.dates_index)
    inflation_differential = obj_inflation_differential.compute_inflation_differential()

    # -------------------------- Carry - Trend - Combo - Returns - Spot ---------------------------------------------- #
    carry_inputs = {'type': 'real', 'inflation': inflation_differential}
    trend_inputs = {'short_term': 4, 'long_term': 16, 'trend': 'spot'}  # could be Spot or Total Return
    combo_inputs = {'cut_off': 2, 'incl_shorts': 'yes', 'cut_off_s': 0.00, 'threshold': 0.25}
    currencies_calculations = obj_import_data.run_compute_currencies(carry_inputs, trend_inputs, combo_inputs)

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                                 EFFECT OVERVIEW                                                  #
    # ---------------------------------------------------------------------------------------------------------------- #
    dates_index = obj_import_data.dates_origin_index
    latest_date = pd.to_datetime('24-04-2020',  format='%d-%m-%Y')
    # latest_date = dates_index[-5]
    next_latest_date = dates_index[-4]
    previous_seven_days_latest_date = dates_index[-10]
    position_size_attribution = 0.03 * 1.33
    spot_data, carry_data = obj_import_data.process_data_config_effect()

    from assetallocation_arp.models.effect.compute_aggregate_currencies import run_aggregate_currencies

    aggregate_currencies = run_aggregate_currencies(weight='1/N', date=obj_import_data.start_date_calculations,
                                                    returns_incl_costs=currencies_calculations['return_incl'],
                                                    spot_data=spot_data, window=52, index=dates_index,
                                                    spot_incl_costs=currencies_calculations['spot_incl'],
                                                    carry_data=carry_data, combo=currencies_calculations['combo'])

    # -------------------------- Profit and Loss overview Combo; Returns Ex costs; Spot; Carry ----------------------- #
    obj_compute_profit_and_loss_overview = ComputeProfitAndLoss(latest_date=latest_date,
                                                                position_size_attribution=position_size_attribution,
                                                                index_dates=dates_index)

    profit_and_loss = obj_compute_profit_and_loss_overview.run_profit_and_loss(
                      combo=currencies_calculations['combo'],
                      returns_ex_costs=currencies_calculations['return_excl'],
                      spot=spot_data, total_incl_signals=aggregate_currencies['agg_total_incl_signals'],
                      spot_incl_signals=aggregate_currencies['agg_spot_incl_signals'],
                      weighted_perf=aggregate_currencies['weighted_performance'])

    # -------------------------- Signals: Combo; Returns Ex costs; Spot; Carry --------------------------------------- #
    obj_compute_signals_overview = ComputeSignalsOverview(next_latest_date=next_latest_date)

    signals_overview = obj_compute_signals_overview.run_signals_overview(real_carry=currencies_calculations['carry'],
                                                                         trend=currencies_calculations['trend'],
                                                                         combo=currencies_calculations['combo'])

    # -------------------------- Trades: Combo ----------------------------------------------------------------------- #
    trades_overview = compute_trades_overview(profit_and_loss_combo_overview=profit_and_loss['profit_and_loss_combo_overview'],
                                              signals_combo_overview=signals_overview['signals_combo_overview'])

    # -------------------------- Warning Flags: Rates; Inflation ----------------------------------------------------- #
    obj_compute_warning_flags_overview = ComputeWarningFlagsOverview(latest_date=latest_date,
                                                                     previous_seven_days_latest_date=
                                                                     previous_seven_days_latest_date)
    obj_compute_warning_flags_overview.process_data_effect()
    rates_usd, rates_eur = obj_compute_warning_flags_overview.compute_warning_flags_rates()


if __name__ == '__main__':
    sys.exit(run_effect())
