import pandas as pd
import numpy as np
import datetime

from calendar import monthrange
from dateutil.relativedelta import relativedelta

from assetallocation_arp.data_etl.inputs_effect.compute_working_days_1d2d import ComputeWorkingDays1D2D


class ComputeWarningFlagsOverview:

    def __init__(self, latest_signal_date, frequency_mat):
        self.latest_signal_date = latest_signal_date
        self.frequency = frequency_mat

    @property
    def prev_7_days_from_latest_signal_date(self):
        # Call  ComputeWorkingDays1D2D to check working date
        obj_compute_uk_working_days = ComputeWorkingDays1D2D()
        if self.frequency == 'weekly' or self.frequency == 'daily':
            prev_7_days_date = self.latest_signal_date - datetime.timedelta(days=7)
            return obj_compute_uk_working_days.convert_to_working_date_uk(prev_7_days_date)
        else:
            # Get the previous month
            days = []
            y, m = self.latest_signal_date.year, (self.latest_signal_date - relativedelta(months=1)).month
            for d in range(1, monthrange(y, m)[1] + 1):
                tmp_date = pd.to_datetime('{:02d}-{:02d}-{:04d}'.format(d, m, y), format='%d-%m-%Y')
                if tmp_date.weekday() <= 4:
                    days.append(tmp_date)
            return days[-1]

    def compute_warning_flags_rates(self, three_month_implied_usd, three_month_implied_eur):
        """
        Function computing the warning flags rates
        :return: dataFrames with rates usd and rates eur
        """

        three_month_implied_usd_latest_date = three_month_implied_usd.loc[self.latest_signal_date]
        three_month_implied_usd_previous_seven_days_latest_date = three_month_implied_usd.loc[self.prev_7_days_from_latest_signal_date]

        rates_usd = three_month_implied_usd_latest_date - three_month_implied_usd_previous_seven_days_latest_date

        three_month_implied_eur_latest_date = three_month_implied_eur.loc[self.latest_signal_date]
        three_month_implied_eur_previous_seven_days_latest_date = three_month_implied_eur.loc[self.prev_7_days_from_latest_signal_date]

        rates_eur = three_month_implied_eur_latest_date - three_month_implied_eur_previous_seven_days_latest_date

        rates = pd.concat([rates_usd, rates_eur], axis=0)

        return np.round(rates.values, 2)

    def compute_warning_flags_inflation(self):
        """
        The function will be completed later
        :return:
        """
        pass

