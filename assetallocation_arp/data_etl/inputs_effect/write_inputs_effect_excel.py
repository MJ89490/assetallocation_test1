from configparser import ConfigParser
import xlwings as xw
import pandas as pd
from datetime import timedelta
import os


def get_inputs_effect_excel(input_file):
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

    inputs_effect = {'user_start_date': user_date, 'trend_inputs': trend_inputs, 'combo_inputs': combo_inputs,
                     'carry_inputs': carry_inputs, 'realtime_inflation_forecast': realtime_inflation_forecast,
                     'weighting_costs': weighting_costs}
    return inputs_effect


def get_inputs_matlab_effect():
    """
    Function getting the inputs for the matlab file from excel dashboard
    :return: a dictionary
    """
    sheet_effect_input = xw.Book.caller().sheets['effect_input']
    signal_day_effect = sheet_effect_input.range('signal_day_effect').value
    start_date_effect = sheet_effect_input.range('start_date_effect').value
    frequency_effect = sheet_effect_input.range('frequency_effect').value

    return {'signal_day_effect': signal_day_effect,
            'start_date_effect': start_date_effect, 'frequency_effect': frequency_effect}


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
