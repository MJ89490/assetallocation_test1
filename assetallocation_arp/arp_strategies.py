import os
import sys
import json
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
        user_date = write_input_effect_excel(input_file)
        profit_and_loss = run_effect(user_start_date=user_date)
        # write_output_to_excel({"date": "11-01-2020"}, input_file)



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

    return user_date


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
        d = model_outputs['date']

        xw.Book(input_file).set_mock_caller()

        sheet_effect_input = xw.Book.caller().sheets['effect_input']

        sheet_effect_input.range('start_date_calculations_effect').value = d


def get_inputs_from_excel():

    # select data from excel
    mat_file = xw.Range('rng_mat_file_path').value
    model_type = xw.Range('rng_model_type').value
    file = xw.Range('rng_full_path').value
    # run selected model
    # write_output_to_excel({"date": "11-01-2020"}, "arp_dashboard_effect.xlsm")
    write_input_effect_excel("arp_dashboard_effect.xlsm")
    # run_model(model_type, mat_file, file)


def get_inputs_from_python(model, file):

    # launch the script from Python
    mat_file = None

    # input_file = None

    models_list = [model.name for model in models_names.Models]

    xw.Book(file).set_mock_caller()

    if model in models_list:
        model_type = model
        run_model(model_type, mat_file, file)
    else:
        raise NameError("Your input is incorrect.")


def get_input_user():

    # model_str = input("Choose a Model: ")
    model_str = 'effect'
    return model_str


if __name__ == "__main__":

    # get_inputs_from_excel()
    get_inputs_from_python(get_input_user(), file="arp_dashboard_effect.xlsm")
