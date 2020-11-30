import os
import calendar
import pandas as pd
from configparser import ConfigParser
from datetime import timedelta
from dateutil.relativedelta import relativedelta


def read_user_date(user_date):
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


def read_update_imf(bool_update_imf):
    if bool_update_imf.item() == 'False':
        imf_data_update = False
    else:
        imf_data_update = True

    return imf_data_update


def read_latest_signal_date(latest_signal_date, obj_import_data, freq):
    if latest_signal_date is None:
        latest_signal_date = obj_import_data.dates_origin_index[-2]
        # Previous Wednesday
        if freq.item() == 'weekly' or freq.item() == 'daily':
            delta = (latest_signal_date.weekday() + 4) % 7 + 1
            latest_signal_date = pd.to_datetime(latest_signal_date.replace('/', '-') - timedelta(days=delta), format='%d-%m-%Y')
        # Previous month
        else:
            days = []
            y, m = latest_signal_date.year, (latest_signal_date - relativedelta(months=1)).month
            for d in range(1, calendar.monthrange(y, m)[1] + 1):
                tmp_date = pd.to_datetime('{:04d}-{:02d}-{:02d}'.format(y, m, d), format='%Y-%m-%d')
                days.append(tmp_date)
            latest_signal_date = pd.to_datetime(days[-1], format='%d-%m-%Y')

    return latest_signal_date


def read_aggregate_calc(agg_total_excl_signals, total_incl_signals, spot_incl_signals, spot_excl_signals):
    agg_dates = agg_total_excl_signals.index.strftime("%Y-%m-%d").to_list()[:-1]
    agg_total_excl_signals = agg_total_excl_signals
    agg_total_excl_signals = agg_total_excl_signals['Total_Excl_Signals'].to_list()[:-1]

    agg_total_incl_signals = total_incl_signals
    agg_total_incl_signals = agg_total_incl_signals['Total_Incl_Signals'].to_list()[:-1]

    agg_spot_incl_signals = spot_incl_signals
    agg_spot_incl_signals = agg_spot_incl_signals['Spot_Incl_Signals'].to_list()[:-1]

    agg_spot_excl_signals = spot_excl_signals
    agg_spot_excl_signals = agg_spot_excl_signals['Spot_Excl_Signals'].to_list()[:-1]

    return {'agg_dates': agg_dates, 'agg_total_excl_signals': agg_total_excl_signals,
            'agg_total_incl_signals': agg_total_incl_signals, 'agg_spot_incl_signals': agg_spot_incl_signals,
            'agg_spot_excl_signals': agg_spot_excl_signals}
