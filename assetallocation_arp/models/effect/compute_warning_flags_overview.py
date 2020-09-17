import pandas as pd

from data_etl.inputs_effect.import_process_data_effect import ProcessDataEffect

from data_etl.outputs_effect.write_logs_computations_effect import write_logs_effect


class ComputeWarningFlagsOverview(ProcessDataEffect):

    def __init__(self, latest_signal_date,  prev_7_days_from_latest_signal_date):
        super().__init__()
        self.latest_signal_date = latest_signal_date
        self.prev_7_days_from_latest_signal_date = prev_7_days_from_latest_signal_date

    @property
    def prev_7_days_from_latest_signal_date(self):
        return self._prev_7_days_from_latest_signal_date

    @ prev_7_days_from_latest_signal_date.setter
    def prev_7_days_from_latest_signal_date(self, value):
        prev_7_days_from_latest_signal_date_loc = value.dates_origin_index.get_loc(self.latest_signal_date) - 5
        self._prev_7_days_from_latest_signal_date = value.dates_origin_index[prev_7_days_from_latest_signal_date_loc]

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

