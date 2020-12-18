import os
import pandas as pd
from assetallocation_UI.aa_web_app.service.strategy import run_strategy
from assetallocation_arp.data_etl.dal.data_models.strategy import Times, TimesAssetInput, DayOfWeek


class ReceivedDataTimes:
    def __init__(self):
        self.times_form = {}
        self.write_logs = {}
        self.version_strategy = 0
        self.strategy_weight = 0
        self.fund_name = None

    @property
    def strategy_weight(self):
        return self._strategy_weight

    @strategy_weight.setter
    def strategy_weight(self, value):
        self._strategy_weight = value

    @property
    def fund_name(self):
        return self._fund_name

    @fund_name.setter
    def fund_name(self, value):
        self._fund_name = value

    def received_data_times(self, form_data):
        for idx, val in enumerate(form_data):
            if idx > 1:
                self.times_form[val.split('=', 1)[0]] = val.split('=', 1)[1]

        # Process date under format '12%2F09%2F2000 to 01/01/2000
        self.times_form['input_date_from_times'] = '/'.join(self.times_form['input_date_from_times'].split('%2F'))

        print(self.times_form)
        return self.times_form

    def call_run_times(self, assets_input_times):

        self.strategy_weight = float(self.times_form['input_strategy_weight_times'])
        self.fund_name = self.times_form['input_fund_name_times']

        long_signals = list(map(float, [self.times_form['input_signal_one_long_times'],
                                        self.times_form['input_signal_two_long_times'],
                                        self.times_form['input_signal_three_long_times']]))

        short_signals = list(map(float, [self.times_form['input_signal_one_short_times'],
                                         self.times_form['input_signal_two_short_times'],
                                         self.times_form['input_signal_three_short_times']]))

        times = Times(DayOfWeek[self.times_form['input_weekday_times'].upper()],
                      self.times_form['input_frequency_times'].lower(),
                      self.times_form['input_leverage_times'], long_signals, short_signals,
                      int(self.times_form['input_time_lag_times']),
                      int(self.times_form['input_vol_window_times']))

        times.asset_inputs = [
            TimesAssetInput(h, int(i), j, k, float(l)) for h, i, j, k, l in zip(
                assets_input_times['input_asset'], assets_input_times['input_leverage'],
                assets_input_times['input_signal_ticker'],
                assets_input_times['input_future_ticker'], assets_input_times['input_costs']
            )
        ]

        fund_strategy = run_strategy(self.fund_name, float(self.times_form['input_strategy_weight_times']),
                                     times, os.environ.get('USERNAME'),
                                     self.times_form['input_date_from_times'])

        self.version_strategy = fund_strategy.strategy_version

        return fund_strategy
