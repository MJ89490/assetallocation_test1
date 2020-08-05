from data_etl.inputs_effect.import_process_data_effect import ProcessDataEffect


class ComputeWarningFlagsOverview(ProcessDataEffect):

    def __init__(self, latest_signal_date, previous_seven_days_latest_date):
        super().__init__()
        self.latest_signal_date = latest_signal_date
        self.seven_previous_latest_date = previous_seven_days_latest_date

    def compute_warning_flags_rates(self):

        three_month_implied_usd_latest_date = self.three_month_implied_usd.loc[self.latest_signal_date]
        three_month_implied_usd_previous_seven_days_latest_date = self.three_month_implied_usd.loc[self.seven_previous_latest_date]

        rates_usd = three_month_implied_usd_latest_date - three_month_implied_usd_previous_seven_days_latest_date

        three_month_implied_eur_latest_date = self.three_month_implied_eur.loc[self.latest_signal_date]
        three_month_implied_eur_previous_seven_days_latest_date = self.three_month_implied_eur.loc[self.seven_previous_latest_date]

        rates_eur = three_month_implied_eur_latest_date - three_month_implied_eur_previous_seven_days_latest_date

        return rates_usd, rates_eur

    def compute_warning_flags_inflation(self):
        pass