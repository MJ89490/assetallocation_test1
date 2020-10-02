import pandas as pd
import datetime

from calendar import monthrange
from dateutil.relativedelta import relativedelta

from data_etl.inputs_effect.process_data_effect import ProcessDataEffect
from data_etl.outputs_effect.write_logs_computations_effect import write_logs_effect

from assetallocation_arp.data_etl.inputs_effect.compute_working_days_1d2d import ComputeWorkingDays1D2D


class ComputeWarningFlagsOverview(ProcessDataEffect):

    def __init__(self, latest_signal_date, frequency_mat, start_date_mat, end_date_mat, signal_day_mat, asset_inputs, all_data):
        super().__init__(asset_inputs, frequency_mat, start_date_mat, end_date_mat, signal_day_mat, all_data)
        self.latest_signal_date = latest_signal_date
        self.frequency = frequency_mat

    @property
    def prev_7_days_from_latest_signal_date(self):
        # Call  ComputeWorkingDays1D2D to check working date
        obj_compute_uk_working_days = ComputeWorkingDays1D2D()
        if self.frequency == 'weekly' or self.frequency == 'daily':
            prev_7_days_date = self.latest_signal_date - datetime.timedelta(days=7)
        else:
            # Get the previous month
            days = []
            y, m = self.latest_signal_date.year, (self.latest_signal_date - relativedelta(months=1)).month
            for d in range(1, monthrange(y, m)[1] + 1):
                tmp_date = pd.to_datetime('{:04d}-{:02d}-{:02d}'.format(y, m, d), format='%Y-%m-%d')
                if tmp_date.weekday() <= 4:
                    days.append(tmp_date)
            prev_7_days_date = days[-1]

        return obj_compute_uk_working_days.convert_to_working_date_uk(prev_7_days_date)

    def compute_warning_flags_rates(self):
        """
        Function computing the warning flags rates
        :return: dataFrames with rates usd and rates eur
        """
        write_logs_effect("Computing warnings flags rates...", "logs_warnings_rates")

        three_month_implied_usd_latest_date = self.three_month_implied_usd.loc[self.latest_signal_date]
        three_month_implied_usd_previous_seven_days_latest_date = self.three_month_implied_usd.loc[self.prev_7_days_from_latest_signal_date]

        rates_usd = three_month_implied_usd_latest_date - three_month_implied_usd_previous_seven_days_latest_date

        three_month_implied_eur_latest_date = self.three_month_implied_eur.loc[self.latest_signal_date]
        three_month_implied_eur_previous_seven_days_latest_date = self.three_month_implied_eur.loc[self.prev_7_days_from_latest_signal_date]

        rates_eur = three_month_implied_eur_latest_date - three_month_implied_eur_previous_seven_days_latest_date

        rates = pd.concat([rates_usd, rates_eur], axis=0)

        return rates.values

    def compute_warning_flags_inflation(self):
        """
        The function will be completed later
        :return:
        """
        pass

