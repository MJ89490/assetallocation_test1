from assetallocation_arp.models.effect.currencies_computations import CurrencyComputations
from assetallocation_arp.models.effect.data_effect import DataProcessingEffect
from assetallocation_arp.models.effect.inflation_differential import InflationDifferential


def run_effect():
    # moving_average= {"short": input("Short: "), "long": input("Long: ")}

    obj_import_data = CurrencyComputations(start_date_calculations='2000-01-14')
    obj_import_data.data_processing_effect()

    # -------------------------- inflation differential calculations -------------------------- #
    obj_inflation_differential = InflationDifferential(dates_index=obj_import_data.dates_index)
    obj_inflation_differential.inflation_release_computations()
    #todo change data currencies by a list with usd values and eur values
    inflation_differential = \
        obj_inflation_differential.inflation_differential_computations(data_currencies_usd=
                                                                       obj_import_data.data_currencies_usd,
                                                                       start_date_computations=
                                                                       obj_import_data.start_date_calculations)

    # -------------------------- carry calculations -------------------------------------- #
    carry = obj_import_data.carry_computations(carry_type='Real',  inflation_differential= inflation_differential)

    # -------------------------- trend calculations -------------------------------------- #
    trend_inputs = {'short_term': 4, 'long_term': 16, 'trend': 'spot'} # could be Spot or Total Return
    trend = obj_import_data.trend_computations(trend_ind=trend_inputs['trend'], short_term=trend_inputs['short_term'],
                                               long_term=trend_inputs['long_term'])

    # # -------------------------- combo calculations -------------------------------------- #
    combo_inputs = {'cut_off': 0.002, 'incl_shorts': 'yes', 'cut_off_s': 0.00, 'threshold': 0.0025}
    combo = obj_import_data.combo_computations(cut_off=combo_inputs['cut_off'], incl_shorts=combo_inputs['incl_shorts'],
                                               cut_off_s=combo_inputs['cut_off_s'],
                                               threshold_for_closing=combo_inputs['threshold'])

    # -------------------------- spot ex costs calculations ------------------------------ #
    spot_ex = obj_import_data.spot_ex_costs_computations()

    # -------------------------- spot incl calculations ---------------------------------- #
    obj_import_data.bid_ask_spread = 10
    spot_incl = obj_import_data.spot_incl_computations()

    # -------------------------- return ex costs calculations ---------------------------- #
    return_ex = obj_import_data.return_ex_costs_computations()

    # -------------------------- return incl costs calculations -------------------------- #
    return_incl = obj_import_data.return_incl_costs_computations()


if __name__ == '__main__':
    run_effect()
