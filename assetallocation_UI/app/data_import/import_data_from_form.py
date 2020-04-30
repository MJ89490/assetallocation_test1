from app.forms import InputsTimesModel
import pandas as pd


class TimesInputs:

    def __init__(self):
        self.form = InputsTimesModel()

    def inputs_times_model(self):

        return {self.form.time_lag.name: [int(self.form.time_lag.data)],
                self.form.leverage_type.name: [self.form.leverage_type.data],
                self.form.volatility_window.name: [int(self.form.volatility_window.data)],
                self.form.sig1_short.name: [int(self.form.sig1_short.data)],
                self.form.sig1_long.name: [int(self.form.sig1_long.data)],
                self.form.sig2_short.name: [int(self.form.sig2_short.data)],
                self.form.sig2_long.name: [int(self.form.sig2_long.data)],
                self.form.sig3_short.name: [int(self.form.sig3_short.data)],
                self.form.sig3_long.name: [int(self.form.sig3_long.data)],
                self.form.frequency.name: [self.form.frequency.data],
                self.form.week_day.name: [self.form.week_day.data]
               }

    def strategy_times_inputs(self, data):

        return pd.DataFrame(data, columns=[self.form.time_lag.name,
                                           self.form.leverage_type.name,
                                           self.form.volatility_window.name,
                                           self.form.sig1_short.name,
                                           self.form.sig1_long.name,
                                           self.form.sig2_short.name,
                                           self.form.sig2_long.name,
                                           self.form.sig3_short.name,
                                           self.form.sig3_long.name,
                                           self.form.frequency.name,
                                           self.form.week_day.name
                                          ])
