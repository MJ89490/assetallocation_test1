import sys

from assetallocation_arp.models.effect.compute_currencies import ComputeCurrencies
from data_etl.inputs_effect.compute_inflation_differential import ComputeInflationDifferential

from assetallocation_arp.models.effect.compute_profit_and_loss import ComputeProfitAndLoss
"""
    Main function to run the EFFECT computations
"""


def run_effect():
    # moving_average= {"short": input("Short: "), "long": input("Long: ")}
    bid_ask_spread = 10
    obj_import_data = ComputeCurrencies(bid_ask_spread=bid_ask_spread)
    obj_import_data.process_data_effect()
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
    obj_compute_profit_and_loss = ComputeProfitAndLoss(latest_date=pd.to_datetime('24-04-2020', format='%d-%m-%Y'))

    profit_and_loss_combo, returns_ex, spot_ex, carry = \
        obj_compute_profit_and_loss.run_profit_and_loss(combo=combo, returns_ex_costs=return_ex, spot_ex_costs=spot_ex)

    obj_compute_profit_and_loss.format_profit_and_loss_data(combo=profit_and_loss_combo,
                                                            returns_ex=returns_ex,
                                                            spot_ex=spot_ex,
                                                            carry=carry)


if __name__ == '__main__':
    sys.exit(run_effect())
