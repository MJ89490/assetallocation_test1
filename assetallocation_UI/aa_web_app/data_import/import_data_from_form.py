from assetallocation_arp.data_etl.dal.data_models.strategy import Times


class TimesInputs:
    """
        Class for the Times inputs form from the Times page
    """

    def __init__(self, form):
        self.form = form

    def inputs_times_model(self) -> Times:
        """
        Function gathering the inputs (from the Flask form) of the user
        :return: dictionary of the inputs of the form
        """
        t = Times(day_of_week=int(self.form.week_day.data), frequency=self.form.frequency.data,
                  leverage_type=self.form.leverage_type.data,
                  long_signals=[float(i.data) for i in (self.form.sig1_long, self.form.sig2_long, self.form.sig3_long)],
                  short_signals=[float(i.data) for i in (self.form.sig1_short, self.form.sig2_short, self.form.sig3_short)],
                  time_lag_in_days=int(self.form.time_lag.data),
                  volatility_window=int(self.form.volatility_window.data))

        return t
