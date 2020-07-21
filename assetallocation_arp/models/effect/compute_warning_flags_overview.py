

class ComputeWarningFlagsOverview:

    def __init__(self, latest_date, previous_seven_days_latest_date):
        self.latest_date = latest_date
        self.seven_previous_latest_date = previous_seven_days_latest_date

    def compute_warning_flags_rates(self, currency_three_month_implied_usd, currency_three_month_implied_eur):

        three_month_implied_usd_latest_date = currency_three_month_implied_usd.loc[self.latest_date]
        three_month_implied_usd_previous_seven_days_latest_date = currency_three_month_implied_usd.loc[self.seven_previous_latest_date]

        rates_usd = three_month_implied_usd_latest_date - three_month_implied_usd_previous_seven_days_latest_date

        three_month_implied_eur_latest_date = currency_three_month_implied_eur.loc[self.latest_date]
        three_month_implied_eur_previous_seven_days_latest_date = currency_three_month_implied_eur.loc[self.seven_previous_latest_date]

        rates_eur = three_month_implied_eur_latest_date - three_month_implied_eur_previous_seven_days_latest_date

        return rates_usd, rates_eur

    def compute_warning_flags_inflation(self):
        pass