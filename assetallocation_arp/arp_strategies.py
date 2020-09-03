import os
import sys
import xlwings as xw
from time import strftime, gmtime
from configparser import ConfigParser
ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
print(ROOT_DIR)
sys.path.insert(0, ROOT_DIR)
from assetallocation_arp.data_etl import import_data_times as gd
from assetallocation_arp.models import times
from assetallocation_arp.common_libraries import models_names
from assetallocation_arp.models.effect.main_effect import run_effect


def run_model(model_type, mat_file, input_file):

    if model_type == models_names.Models.times.name:
        # get inputs_effect from excel and matlab data
        times_inputs, asset_inputs, all_data = gd.extract_inputs_and_mat_data(model_type, mat_file, input_file)
        # run strategy
        signals, returns, r, positioning = times.format_data_and_calc(times_inputs, asset_inputs, all_data)
        # write results to output sheet
        write_output_to_excel({models_names.Models.times.name: (asset_inputs, positioning, r, signals, times_inputs)}, input_file)

    if model_type == models_names.Models.maven.name:
        print(model_type)
    if model_type == models_names.Models.effect.name:
        user_date, trend_inputs, combo_inputs, carry_inputs, realtime_inflation_forecast, weighting_costs = write_input_effect_excel(input_file)

        profit_and_loss, signals_overview, trades_overview, rates_usd, rates_eur = run_effect(user_start_date=user_date,
                                                                                              trend_inputs=trend_inputs,
                                                                                              combo_inputs=combo_inputs,
                                                                                              carry_inputs=carry_inputs,
                                                                                              weighting_costs=weighting_costs,
                                                                                              realtime_inflation_forecast=realtime_inflation_forecast)

        write_output_to_excel({models_names.Models.effect.name: (profit_and_loss, signals_overview, trades_overview, rates_usd, rates_eur)}, input_file)

    if model_type == models_names.Models.curp.name:
        print(model_type)
    if model_type == models_names.Models.fica.name:
        print(model_type)
    if model_type == models_names.Models.factor.name:
        print(model_type)
    if model_type == models_names.Models.comca.name:
        print(model_type)


def write_input_effect_excel(input_file):
    #TODO put the function in a new script import_data_effect (data_etl)

    xw.Book(input_file).set_mock_caller()

    sheet_effect_input = xw.Book.caller().sheets['effect_input']

    user_date = sheet_effect_input.range('start_date_calculations_effect').value

    if user_date is None:
        # Instantiate ConfigParser
        config = ConfigParser()
        # Parse existing file
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config_effect_model', 'dates_effect.ini'))
        config.read(path)
        # Read values from the dates_effect.ini file
        default_start_date = config.get('start_date_computations', 'start_date_calculations')
        user_date = default_start_date

    # EFFECT inputs
    realtime_inflation_forecast = sheet_effect_input.range('real_time_inf').value.strip().lower()
    trend = sheet_effect_input.range('trend_indicator_input').value
    short_term = sheet_effect_input.range('short_term_input').value
    long_term = sheet_effect_input.range('long_term_input').value
    trend_inputs = {'short_term': int(short_term), 'long_term': int(long_term), 'trend': trend.strip().lower()}

    incl_shorts = sheet_effect_input.range('incl_shorts_input').value
    cut_off = sheet_effect_input.range('cut_off_long_input').value * 100
    cut_off_s = sheet_effect_input.range('cut_off_short_input').value * 100
    thr = sheet_effect_input.range('threshold_closing_input').value * 100

    combo_inputs = {'cut_off': float(cut_off), 'incl_shorts': incl_shorts.strip().lower(),
                    'cut_off_s': float(cut_off_s), 'threshold': float(thr)}

    carry = sheet_effect_input.range('type_carry_input').value

    carry_inputs = {'type': carry.strip().lower(), 'inflation': ''}

    window_size = sheet_effect_input.range('window_input').value
    weight = sheet_effect_input.range('weight_input').value
    position_size_attribution = sheet_effect_input.range('pos_attr_input').value
    bid_ask_spread = sheet_effect_input.range('bid_ask_input').value

    weighting_costs = {'window': int(window_size), 'weight': weight, 'pos_size_attr': float(position_size_attribution),
                       'bid_ask': int(bid_ask_spread)}

    return user_date, trend_inputs, combo_inputs, carry_inputs, realtime_inflation_forecast, weighting_costs


def write_output_to_excel(model_outputs, input_file):

    if models_names.Models.times.name in model_outputs.keys():

        asset_inputs, positioning, returns, signals, times_inputs = model_outputs['times']

        xw.Book(input_file).set_mock_caller()

        sheet_times_output = xw.Book.caller().sheets['times_output']

        sheet_times_inputs = xw.Book.caller().sheets['times_input']

        n_columns = len(signals.columns) + 2

        sheet_times_output.range('rng_times_output').offset(-1, 0).value = "TIMES Signals"

        sheet_times_output.range('rng_times_output').value = signals
        #
        sheet_times_output.range('rng_times_output').offset(-1, n_columns + 2).value = "TIMES Returns"
        #
        sheet_times_output.range('rng_times_output').offset(0, n_columns + 2).value = returns
        #
        sheet_times_output.range('rng_times_output').offset(-1, 2 * n_columns + 4).value = "TIMES Positions"
        #
        sheet_times_output.range('rng_times_output').offset(0, 2 * n_columns + 4).value = positioning
        #
        # write inputs_effect used to excel and run time
        sheet_times_inputs.range('rng_inputs_used').offset(-1, 1).value = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        #
        sheet_times_inputs.range('rng_inputs_used').offset(0, 0).value = times_inputs
        #
        sheet_times_inputs.range('rng_inputs_used').offset(3, 0).value = asset_inputs

    else:

        p_and_l_overview, signals_overview, trades_overview, rates_usd, rates_eur = model_outputs['effect']

        weekly_total_not = p_and_l_overview['profit_and_loss_notional']['profit_and_loss_total_weekly_notional']
        weekly_spot_not = p_and_l_overview['profit_and_loss_notional']['profit_and_loss_spot_weekly_notional']
        weekly_carry_not = p_and_l_overview['profit_and_loss_notional']['profit_and_loss_carry_weekly_notional']

        ytd_total_not = p_and_l_overview['profit_and_loss_notional']['profit_and_loss_total_ytd_notional']
        ytd_spot_not = p_and_l_overview['profit_and_loss_notional']['profit_and_loss_spot_ytd_notional']
        ytd_carry_not = p_and_l_overview['profit_and_loss_notional']['profit_and_loss_carry_ytd_notional']

        weekly_total_matr = p_and_l_overview['profit_and_loss_matr']['profit_and_loss_total_weekly_matr']
        weekly_spot_matr = p_and_l_overview['profit_and_loss_matr']['profit_and_loss_spot_weekly_matr']
        weekly_carry_matr = p_and_l_overview['profit_and_loss_matr']['profit_and_loss_carry_weekly_matr']

        ytd_total_matr = p_and_l_overview['profit_and_loss_matr']['profit_and_loss_total_ytd_matr']
        ytd_spot_matr = p_and_l_overview['profit_and_loss_matr']['profit_and_loss_spot_ytd_matr']
        ytd_carry_matr = p_and_l_overview['profit_and_loss_matr']['profit_and_loss_carry_ytd_matr']

        xw.Book(input_file).set_mock_caller()

        sheet_effect_input = xw.Book.caller().sheets['EFFECT']

        # Profit and Loss overview
        sheet_effect_input.range('profit_and_loss_total_weekly_notional').value = weekly_total_not
        sheet_effect_input.range('profit_and_loss_spot_weekly_notional').value = weekly_spot_not
        sheet_effect_input.range('profit_and_loss_carry_weekly_notional').value = weekly_carry_not

        sheet_effect_input.range('profit_and_loss_total_ytd_notional').value = ytd_total_not
        sheet_effect_input.range('profit_and_loss_spot_ytd_notional').value = ytd_spot_not
        sheet_effect_input.range('profit_and_loss_carry_ytd_notional').value = ytd_carry_not

        sheet_effect_input.range('profit_and_loss_total_weekly_matr').value = weekly_total_matr
        sheet_effect_input.range('profit_and_loss_spot_weekly_matr').value = weekly_spot_matr
        sheet_effect_input.range('profit_and_loss_carry_weekly_matr').value = weekly_carry_matr

        sheet_effect_input.range('profit_and_loss_total_ytd_matr').value = ytd_total_matr
        sheet_effect_input.range('profit_and_loss_spot_ytd_matr').value = ytd_spot_matr
        sheet_effect_input.range('profit_and_loss_carry_ytd_matr').value = ytd_carry_matr

        sheet_effect_input.range('profit_and_loss_combo').options(transpose=True).value = p_and_l_overview['profit_and_loss_combo_overview']
        sheet_effect_input.range('profit_and_loss_total').options(transpose=True).value = p_and_l_overview['profit_and_loss_total_overview']
        sheet_effect_input.range('profit_and_loss_spot').options(transpose=True).value = p_and_l_overview['profit_and_loss_spot_ex_overview']
        sheet_effect_input.range('profit_and_loss_carry').options(transpose=True).value = p_and_l_overview['profit_and_loss_carry_overview']

        sheet_effect_input.range('signals_real_carry').options(transpose=True).value = signals_overview['signals_real_carry']
        sheet_effect_input.range('signals_trend').options(transpose=True).value = signals_overview['signals_trend_overview']
        sheet_effect_input.range('signals_combo').options(transpose=True).value = signals_overview['signals_combo_overview']

        sheet_effect_input.range('drawdown').options(transpose=True).value = signals_overview['signals_drawdown_position_size_matr']['drawdown']
        sheet_effect_input.range('position_matr').options(transpose=True).value = signals_overview['signals_drawdown_position_size_matr']['size_matr']
        sheet_effect_input.range('ex_ante_vol').options(transpose=True).value = signals_overview['signals_limits_controls']['ex_ante_vol']
        sheet_effect_input.range('matr_notional').options(transpose=True).value = signals_overview['signals_limits_controls']['matr_notional']

        sheet_effect_input.range('trades_combo').options(transpose=True).value = trades_overview

        sheet_effect_input.range('warning_rates_usd').options(transpose=True).value = rates_usd
        sheet_effect_input.range('warning_rates_eur').options(transpose=True).value = rates_eur


def get_inputs_from_excel():

    # select data from excel
    mat_file = xw.Range('rng_mat_file_path').value
    model_type = xw.Range('rng_model_type').value
    file = xw.Range('rng_full_path').value

    # run selected model
    run_model(model_type, mat_file, file)


def get_inputs_from_python(model, input_file):

    # launch the script from Python
    mat_file = None
    # input_file = None

    models_list = [model.name for model in models_names.Models]

    xw.Book(input_file).set_mock_caller()

    if model in models_list:
        model_type = model
        run_model(model_type, mat_file, input_file)
    else:
        raise NameError("Your input is incorrect.")


def get_input_user():

    # model_str = input("Choose a Model: ")
    model_str = 'effect'
    return model_str


if __name__ == "__main__":

    # get_inputs_from_excel()
    get_inputs_from_python(get_input_user(), "arp_dashboard_effect.xlsm")
