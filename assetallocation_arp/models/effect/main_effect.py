import sys

from assetallocation_arp.models.effect.compute_currencies import ComputeCurrencies
from data_etl.inputs_effect.compute_inflation_differential import ComputeInflationDifferential

from assetallocation_arp.models.effect.compute_profit_and_loss_overview_overview import ComputeProfitAndLoss
from assetallocation_arp.models.effect.compute_signals_overview import ComputeSignalsOverview
from assetallocation_arp.models.effect.compute_trades_overview import compute_trades_overview
from assetallocation_arp.models.effect.compute_warning_flags_overview import ComputeWarningFlagsOverview

import assetallocation_arp.common_libraries.names_all_currencies as all_currencies

"""
    Main function to run the EFFECT computations
"""


def run_effect():
    # moving_average= {"short": input("Short: "), "long": input("Long: ")}
    bid_ask_spread = 10
    obj_import_data = ComputeCurrencies(bid_ask_spread=bid_ask_spread)
    data_currencies_usd, data_currencies_eur = obj_import_data.process_data_effect()
    obj_import_data.start_date_calculations = '2000-01-11'

    # -------------------------- inflation differential calculations ------------------------------------------------- #
    obj_inflation_differential = ComputeInflationDifferential(dates_index=obj_import_data.dates_index)
    inflation_differential = obj_inflation_differential.compute_inflation_differential()

    # -------------------------- carry calculations ------------------------------------------------------------------ #
    carry = obj_import_data.compute_carry(carry_type='Real',  inflation_differential=inflation_differential)

    # -------------------------- trend calculations ------------------------------------------------------------------ #
    trend_inputs = {'short_term': 4, 'long_term': 16, 'trend': 'spot'} # could be Spot or Total Return
    trend = obj_import_data.compute_trend(trend_ind=trend_inputs['trend'], short_term=trend_inputs['short_term'],
                                          long_term=trend_inputs['long_term'])

    # # -------------------------- combo calculations ---------------------------------------------------------------- #
    combo_inputs = {'cut_off': 2, 'incl_shorts': 'yes', 'cut_off_s': 0.00, 'threshold': 0.25}
    combo = obj_import_data.compute_combo(cut_off=combo_inputs['cut_off'], incl_shorts=combo_inputs['incl_shorts'],
                                          cut_off_s=combo_inputs['cut_off_s'],
                                          threshold_for_closing=combo_inputs['threshold'])

    # -------------------------- return ex costs calculations -------------------------------------------------------- #
    return_ex = obj_import_data.compute_return_ex_costs()

    # -------------------------- return incl costs calculations ------------------------------------------------------ #
    return_incl = obj_import_data.compute_return_incl_costs()

    # -------------------------- spot ex costs calculations ---------------------------------------------------------- #
    spot_ex = obj_import_data.compute_spot_ex_costs()

    # -------------------------- spot incl calculations -------------------------------------------------------------- #
    spot_incl = obj_import_data.compute_spot_incl_costs()



    import pandas as pd

    latest_date = pd.to_datetime('24-04-2020', format='%d-%m-%Y')
    next_latest_date = pd.to_datetime('27-04-2020', format='%d-%m-%Y')
    previous_seven_days_latest_date = pd.to_datetime('17-04-2020', format='%d-%m-%Y')

    obj_compute_profit_and_loss_overview = ComputeProfitAndLoss(latest_date=latest_date)

    profit_and_loss_combo_overview, profit_and_loss_returns_ex_overview, profit_and_loss_spot_ex_overview, \
    profit_and_loss_carry_overview = \
        obj_compute_profit_and_loss_overview.run_profit_and_loss(combo=combo, returns_ex_costs=return_ex, spot_ex_costs=spot_ex)

    obj_compute_signals_overview = ComputeSignalsOverview(next_latest_date=next_latest_date)

    signals_real_carry_overview, signals_trend_overview, signals_combo_overview = \
        obj_compute_signals_overview.run_signals_overview(real_carry=carry, trend=trend, combo=combo)

    trades_overview = compute_trades_overview(profit_and_loss_combo_overview=profit_and_loss_combo_overview,
                                              signals_combo_overview=signals_combo_overview)

    obj_compute_warning_flags_overview = ComputeWarningFlagsOverview(latest_date=latest_date,
                                                                     previous_seven_days_latest_date=previous_seven_days_latest_date)

    from configparser import ConfigParser
    import os
    import json
    # Instantiate ConfigParser
    config = ConfigParser()
    # Parse existing file
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'all_currencies_effect.ini'))
    config.read(path)
    # Read values from the all_currencies_effect.ini file
    currencies_three_month_implied_usd_config = json.loads(config.get('currencies_three_month_implied_usd', 'three_month_implied_usd_data'))
    currencies_three_month_implied_eur_config = json.loads(config.get('currencies_three_month_implied_eur', 'three_month_implied_eur_data'))

    currencies_three_month_implied_usd = pd.DataFrame(currencies_three_month_implied_usd_config).three_month_implied_usd
    currencies_three_month_implied_eur = pd.DataFrame(currencies_three_month_implied_eur_config).three_month_implied_eur

    three_month_implied_usd = data_currencies_usd[currencies_three_month_implied_usd]
    three_month_implied_eur = data_currencies_eur[currencies_three_month_implied_eur]

    obj_compute_warning_flags_overview.compute_warning_flags_rates(currency_three_month_implied_usd=three_month_implied_usd,
                                                                   currency_three_month_implied_eur=three_month_implied_eur)


if __name__ == '__main__':
    sys.exit(run_effect())

