import os
import pandas as pd
# from datetime import datetime, date
import datetime as dt

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
        self.strategy_weight_user = 0
        self.match_date_db = None
        self.date_to = None
        self.is_new_strategy = None
        self.fund_name = None
        self.strategy = None
        self.type_of_request = None
        self.date_to_sidebar = None

    @property
    def match_date_db(self) -> bool:
        return self._match_date_db

    @match_date_db.setter
    def match_date_db(self, x) -> None:
        self._match_date_db = x

    @property
    def type_of_request(self) -> bool:
        return self._type_of_request

    @type_of_request.setter
    def type_of_request(self, x) -> None:
        if x is None:
            x = False
        self._type_of_request = x

    @property
    def date_to(self):
        return self._date_to

    @date_to.setter
    def date_to(self, x) -> None:
        if x is not None:
            self._date_to = dt.datetime.strptime(x, '%d/%m/%Y').date()

    @property
    def strategy(self) -> Times:
        return self._strategy

    @strategy.setter
    def strategy(self, x: Times) -> None:
        self._strategy = x

    @property
    def is_new_strategy(self) -> bool:
        return bool(self._is_new_strategy)

    @is_new_strategy.setter
    def is_new_strategy(self, value: bool):
        self._is_new_strategy = value

    @property
    def version_strategy(self):
        return int(self._version_strategy)

    @version_strategy.setter
    def version_strategy(self, value):
        self._version_strategy = value

    @property
    def strategy_weight(self):
        return self._strategy_weight

    @strategy_weight.setter
    def strategy_weight(self, value):
        self._strategy_weight = value

    @property
    def strategy_weight_user(self):
        return self._strategy_weight_user

    @strategy_weight_user.setter
    def strategy_weight_user(self, value):
        self._strategy_weight_user = value

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

    @property
    def date_to_sidebar(self):
        return self._date_to_sidebar

    @date_to_sidebar.setter
    def date_to_sidebar(self, value) -> None:
        self._date_to_sidebar = pd.to_datetime(value, format='%d/%m/%Y')

    def check_in_date_to_existing_version(self):
        apc = TimesProcCaller()
        match_date = apc.select_fund_strategy_result_dates(fund_name=self.fund_name,
                                                           strategy_version=self.version_strategy)

        return match_date[dt.date(self.date_to.year, self.date_to.month, self.date_to.day)]

    def receive_data_latest_version_dashboard(self, business_date_to):
        apc = TimesProcCaller()
        self.version_strategy = max(apc.select_strategy_versions(Name.times))
        # TODO CHANGE DATE TO TO FLEXIBLE DATE
        # TODO EACH STRATEGY VERSIONS RETURN NONE
        # for v in apc.select_strategy_versions(Name.times):
        fs = apc.select_fund_strategy_results(self.fund_name, Name.times, self.version_strategy,
                                              business_date_from=dt.date(2000, 1, 1), business_date_to=business_date_to
                                              )
        print(fs)
        self.strategy_weight = fs.weight

    def receive_data_selected_version_sidebar_dashboard(self, business_date_to):
        apc = TimesProcCaller()
        fs = apc.select_fund_strategy_results(self.fund_name, Name.times, self.version_strategy,
                                              business_date_from=dt.date(2000, 1, 1),
                                              business_date_to=business_date_to
                                              )
        # self.strategy_weight = fs.weight
        self.strategy_weight = 0.46

    def receive_data_existing_versions(self, strategy_version):
        apc = TimesProcCaller()
        self.version_strategy = strategy_version
        self.strategy = apc.select_strategy(strategy_version)
        # Inputs
        fs = apc.select_fund_strategy_results(fund_name=self.fund_name,
                                              strategy_name=Name.times,
                                              strategy_version=strategy_version,
                                              business_date_from=dt.date(2000, 1, 1),
                                              business_date_to=dt.date(self.date_to.year, self.date_to.month, self.date_to.day)
                                              )

        # self.strategy_weight = fs.weight
        try:
            self.strategy_weight = fs.weight
        except AttributeError:
            self.strategy_weight = self.strategy_weight_user

        inputs_versions = {'fund': self.fund_name,
                           'version': strategy_version,
                           'input_date_from_times': '2000-01-01',
                           'input_date_to_times': self.date_to,
                           'input_strategy_weight_times': self.strategy_weight,
                           'input_time_lag_times': self.strategy.time_lag_in_months,
                           'input_leverage_times': self.strategy.leverage_type.name,
                           'input_vol_window_times': self.strategy.volatility_window,
                           'input_frequency_times': self.strategy.frequency.name,
                           'input_weekday_times': self.strategy.day_of_week.name,
                           'input_signal_one_short_times': self.strategy.short_signals[0],
                           'input_signal_one_long_times': self.strategy.long_signals[0],
                           'input_signal_two_short_times': self.strategy.short_signals[1],
                           'input_signal_two_long_times': self.strategy.long_signals[1],
                           'input_signal_three_short_times': self.strategy.short_signals[2],
                           'input_signal_three_long_times': self.strategy.long_signals[2]}

        self.inputs_existing_versions_times = inputs_versions
        # Assets
        assets_names, assets, signal, future, costs, leverage = [], [], [], [], [], []

        for asset in self.strategy.asset_inputs:
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
            tmp = {}
            for idx, val in enumerate(form_data):
                # if idx > 1:
                tmp[val.split('=', 1)[0]] = val.split('=', 1)[1]
            # Process date under format '12%2F09%2F2000 to 01/01/2000
            tmp['input_date_from_times'] = '/'.join(tmp['input_date_from_times'].split('%2F'))
            tmp['input_date_to_new_version_times'] = '/'.join(tmp['input_date_to_new_version_times'].split('%2F'))
            self.times_form = tmp

        print(self.times_form)
        return self.times_form

    def call_run_times(self, assets_input_times):

        # self.strategy_weight = float(self.times_form['input_strategy_weight_times'])

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

        # Times.description = self.times_form['input_version_name']
        Times.description = self.fund_name

        # self.date_to = datetime.strptime(self.times_form['input_date_to_new_version_times'], '%d/%m/%Y').date()
        self.date_to = self.times_form['input_date_to_new_version_times']

        times.asset_inputs = [
            TimesAssetInput(h, int(i), j, k, float(l)) for h, i, j, k, l in zip(
                assets_input_times['input_asset'], assets_input_times['input_leverage'],
                assets_input_times['input_signal_ticker'],
                assets_input_times['input_future_ticker'], assets_input_times['input_costs']
            )
        ]

        # TODO self.times_form['input_strategy_weight_times'] had been removed from the inputs!!!
        fund_strategy = run_strategy(self.fund_name, float(0.46),
                                     times, os.environ.get('USERNAME'),
                                     dt.datetime.strptime(self.times_form['input_date_from_times'], '%d/%m/%Y').date(),
                                     dt.datetime.strptime(self.times_form['input_date_to_new_version_times'], '%d/%m/%Y').date()
                                     )
        self.version_strategy = fund_strategy.strategy_version

        print(self.version_strategy)

        return fund_strategy

    def run_existing_strategy(self):
        fund_strategy = run_strategy(self.fund_name,
                                     float(self.strategy_weight),
                                     self.strategy,
                                     os.environ.get('USERNAME'),
                                     dt.datetime.strptime(self.inputs_existing_versions_times['input_date_from_times'],
                                                          '%d/%m/%Y').date(),
                                     self.inputs_existing_versions_times['input_date_to_times']
                                     )

        # fund_strategy = run_strategy(
        #     self.fund_name, float(self.strategy_weight), self.strategy, os.environ.get('USERNAME'),
        #     self.inputs_existing_versions_times['input_date_from_times'], self.is_new_strategy
        # )
        # TODO CREATE A NEW VERSION !!!
        self.version_strategy = 188

        # self.version_strategy = fund_strategy.strategy_version
        return fund_strategy