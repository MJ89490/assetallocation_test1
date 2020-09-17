from configparser import ConfigParser
import xlwings as xw
import pandas as pd
from datetime import timedelta
import os


def get_user_date_effect_excel(input_file):
    """
    Function getting the different inputs from excel dashboard
    :param input_file: the name of the excel file
    :return: a dictionary
    """
    xw.Book(input_file).set_mock_caller()

    sheet_effect_input = xw.Book.caller().sheets['effect_input']

    user_date = sheet_effect_input.range('start_date_calculations_effect').value

    # EFFECT inputs

    if user_date is None:
        # Instantiate ConfigParser
        config = ConfigParser()
        # Parse existing file
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config_effect_model', 'dates_effect.ini'))
        config.read(path)
        # Read values from the dates_effect.ini file
        default_start_date = config.get('start_date_computations', 'start_date_calculations')
        user_date = default_start_date

    return user_date


def get_latest_date_signal_excel(obj_import_data: object):
    """
    Function getting the latest date signal from excel dashboard
    :param obj_import_data: object from compute_currencies class
    :return: a string
    """

    sheet_effect_input = xw.Book.caller().sheets['effect_input']
    latest_signal_date = sheet_effect_input.range('latest_signal_date').value

    if latest_signal_date is None:
        # latest_signal_date = pd.to_datetime('15-07-2020', format='%d-%m-%Y')
        latest_signal_date = obj_import_data.dates_origin_index[-1]
        offset = (latest_signal_date.weekday() - 2) % 7
        latest_signal_date = pd.to_datetime(latest_signal_date - timedelta(days=offset), format='%d-%m-%Y')

    return latest_signal_date
