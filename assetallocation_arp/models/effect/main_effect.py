from assetallocation_arp.models.effect.effect_model import CurrencyComputations


def run_effect():
    # moving_average= {"short": input("Short: "), "long": input("Long: ")}
    obj_import_data = CurrencyComputations()
    obj_import_data.import_data_matlab()
    obj_import_data.data_processing_effect()

    obj_import_data.start_date_calculations = '2000-01-11'

    # -------------------------- carry calculations -------------------------------------- #
    obj_import_data.carry_computations(carry_type='Real')

    # -------------------------- trend calculations -------------------------------------- #
    trend_inputs = {'short_term': 4, 'long_term': 16, 'trend': 'spot'} # could be Spot or Total Return
    obj_import_data.trend_computations(trend_ind=trend_inputs['trend'], short_term=trend_inputs['short_term'],
                                       long_term=trend_inputs['long_term'])

    # -------------------------- combo calculations -------------------------------------- #
    combo_inputs = {'cut_off': 0.002, 'incl_shorts': 'yes', 'cut_off_s': 0.00, 'threshold': 0.0025}
    obj_import_data.combo_computations(cut_off=combo_inputs['cut_off'], incl_shorts=combo_inputs['incl_shorts'],
                                       cut_off_s=combo_inputs['cut_off_s'],
                                       threshold_for_closing=combo_inputs['threshold'])

    # -------------------------- spot ex costs calculations ------------------------------ #
    obj_import_data.spot_ex_costs_computations()

    # -------------------------- spot incl calculations ---------------------------------- #
    obj_import_data.bid_ask_spread = 10
    obj_import_data.spot_incl_computations()

    # -------------------------- return ex costs calculations ---------------------------- #
    obj_import_data.return_ex_costs_computations()

    # -------------------------- return incl costs calculations -------------------------- #
    obj_import_data.return_incl_costs_computations()

    # -------------------------- inflation release calculations -------------------------- #
    obj_import_data.inflation_release_computations()

    # -------------------------- inflation differential calculations -------------------------- #
    obj_import_data.inflation_differential_computations()


if __name__ == '__main__':
    run_effect()
