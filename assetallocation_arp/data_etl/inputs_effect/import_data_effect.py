import calendar
import pandas as pd
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from assetallocation_arp.data_etl.data_manipulation import set_data_frequency
from assetallocation_arp.data_etl.inputs_effect.compute_working_days_1d2d import ComputeWorkingDays1D2D

"""
    Class to import data from matlab file
"""


class ImportDataEffect:

    def __init__(self, end_date_mat, start_date_mat, frequency_mat, signal_day_mat, all_data):
        self.data_currencies = pd.DataFrame()
        self.data_currencies_copy = pd.DataFrame()
        self.data_currencies_no_end_date = pd.DataFrame()
        self.data_currencies_no_start_date = pd.DataFrame()
        self.frequency_mat = frequency_mat
        self.start_date_mat = start_date_mat
        self.signal_day_mat = signal_day_mat
        self.end_date_mat = end_date_mat
        self.all_data = all_data

    @property
    def frequency_mat(self):
        return self._frequency_mat

    @frequency_mat.setter
    def frequency_mat(self, value):
        self._frequency_mat = value

    @property
    def start_date_mat(self):
        return self._start_date_mat

    @start_date_mat.setter
    def start_date_mat(self, value):
        self._start_date_mat = value

    @property
    def end_date_mat(self):
        return self._end_date_mat

    @end_date_mat.setter
    def end_date_mat(self, value):
        self._end_date_mat = value

    @property
    def signal_day_mat(self):
        return self._signal_day_mat

    @signal_day_mat.setter
    def signal_day_mat(self, value):
        self._signal_day_mat = value

    def import_data_matlab(self, calculation_type):
        """
        Function importing the data from matlab file
        :return: a dataFrame self.data_currencies with matlab data
        """

        self.data_currencies = self.all_data

        self.data_currencies = self.data_currencies.loc[self.start_date_mat:self.end_date_mat]

        self.data_currencies_no_start_date = set_data_frequency(self.all_data, self.frequency_mat, self.signal_day_mat) # Anais will remove this line

        self.data_currencies = set_data_frequency(self.data_currencies, self.frequency_mat, self.signal_day_mat,
                                                  calculation_type)

        next_date_values, next_date = self.add_next_date(self.frequency_mat)

        self.data_currencies_copy = self.data_currencies.copy()

        self.data_currencies_copy.loc[next_date] = next_date_values

        return self.data_currencies_copy

    def add_next_date(self, frequency):
        """
        Function adding the next day from the last day in the data_currencies dataFrame
        That is mandatory for combo, trend and carry for the Signals overview
        :return: a list of values for the next date and the next date
        """

        obj_compute_uk_working_days = ComputeWorkingDays1D2D()

        last_date = pd.to_datetime(self.data_currencies.index.values[-1], format='%d-%m-%Y')

        if frequency == 'weekly':
            next_date = pd.to_datetime(last_date + timedelta(days=7), format='%d-%m-%Y')
        elif frequency == 'daily':
            next_date = pd.to_datetime(last_date + timedelta(days=1), format='%d-%m-%Y')
        else:
            dates = []
            y, m = last_date.year, (last_date + relativedelta(months=1)).month
            for d in range(1, calendar.monthrange(y, m)[1] + 1):
                tmp_date = pd.to_datetime('{:04d}-{:02d}-{:02d}'.format(y, m, d), format='%Y-%m-%d')
                if tmp_date.weekday() <= 4:
                    dates.append(tmp_date)
            next_date = dates[-1]

        # Check if the next date is a working date in UK calendar
        working_date = obj_compute_uk_working_days.convert_to_working_date_uk(next_date)

        # Set the new date with values equal to zero
        return [0] * self.data_currencies.shape[1], pd.to_datetime(working_date, format='%Y-%m-%d')
