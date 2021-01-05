import os
from assetallocation_UI.aa_web_app.service.strategy import run_strategy
from assetallocation_arp.data_etl.dal.data_models.strategy import Times, TimesAssetInput, DayOfWeek
from assetallocation_arp.data_etl.dal.arp_proc_caller import TimesProcCaller
from assetallocation_arp.common_libraries.dal_enums.strategy import Name


class ReceivedDataTimes:
    def __init__(self):
        self.times_form = {}
        self.write_logs = {}
        self.inputs_existing_versions_times = {}
        self.assets_existing_versions_times = {}
        self.version_strategy = 0
        self.strategy_weight = 0
        self.is_new_strategy = True
        self.fund_name = None

    @property
    def version_strategy(self):
        return int(self._version_strategy)

    @version_strategy.setter
    def version_strategy(self, value):
        self._version_strategy = value

    @property
    def is_new_strategy(self):
        return self._is_new_strategy

    @is_new_strategy.setter
    def is_new_strategy(self, value):
        self._is_new_strategy = value

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

    @property
    def fund_strategy_dict(self):
        return {'fund': self._fund_name, 'strategy': self.version_strategy}

    @property
    def inputs_existing_versions_times(self):
        return self._inputs_existing_versions_times

    @inputs_existing_versions_times.setter
    def inputs_existing_versions_times(self, value):
        self._inputs_existing_versions_times = value

    @property
    def assets_existing_versions_times(self):
        return self._assets_existing_versions_times

    @assets_existing_versions_times.setter
    def assets_existing_versions_times(self, value):
        self._assets_existing_versions_times = value

    def receive_data_existing_versions(self, version_strategy):
        apc = TimesProcCaller()
        self.version_strategy = version_strategy
        strat = apc.select_strategy(version_strategy)
        # Inputs
        fs = apc.select_fund_strategy_results(self.fund_name, Name.times, version_strategy)

        inputs_versions = {'fund': self.fund_name, 'version': version_strategy,
                           'input_date_from_times': '01/01/2000',
                           'input_strategy_weight_times': fs.weight,
                           'input_time_lag_times': strat.time_lag_in_months,
                           'input_leverage_times': strat.leverage_type.name,
                           'input_vol_window_times': strat.volatility_window,
                           'input_frequency_times': strat.frequency.name,
                           'input_weekday_times': strat.day_of_week.name,
                           'input_signal_one_short_times': strat.short_signals[0],
                           'input_signal_one_long_times': strat.long_signals[0],
                           'input_signal_two_short_times': strat.short_signals[1],
                           'input_signal_two_long_times': strat.long_signals[1],
                           'input_signal_three_short_times': strat.short_signals[2],
                           'input_signal_three_long_times': strat.long_signals[2]}

        self.inputs_existing_versions_times = inputs_versions
        # Assets
        assets_names, assets, signal, future, costs, leverage = [], [], [], [], [], []

        for asset in strat.asset_inputs:
            assets_names.append(asset.asset_subcategory.name)
            signal.append(asset.signal_ticker)
            future.append(asset.future_ticker)
            costs.append(asset.cost)
            leverage.append(asset.s_leverage)
            assets.append([asset.asset_subcategory.name, asset.signal_ticker, asset.future_ticker, asset.cost,
                           asset.s_leverage])

        self.assets_existing_versions_times = {'input_asset': assets_names,
                                               'input_signal_ticker': signal,
                                               'input_future_ticker': future,
                                               'input_costs': costs,
                                               'input_leverage': leverage}

        self.is_new_strategy = False

        return assets

    def received_data_times(self, form_data):
        if self.is_new_strategy:
            self.times_form = form_data
            for idx, val in enumerate(self.times_form):
                if idx > 1:
                    self.times_form[val.split('=', 1)[0]] = val.split('=', 1)[1]
            # Process date under format '12%2F09%2F2000 to 01/01/2000
            self.times_form['input_date_from_times'] = '/'.join(self.times_form['input_date_from_times'].split('%2F'))
        else:
            self.times_form = form_data

        print(self.times_form)
        return self.times_form

    def call_run_times(self, assets_input_times):

        self.strategy_weight = float(self.times_form['input_strategy_weight_times'])

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
                                     times, os.environ.get('USERNAME'), self.is_new_strategy, self.version_strategy,
                                     self.times_form['input_date_from_times']
                                     )

        self.version_strategy = fund_strategy.strategy_version

        return fund_strategy
