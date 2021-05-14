import os
import pandas as pd
import datetime as dt

from assetallocation_UI.aa_web_app.service.strategy import run_strategy
from assetallocation_arp.common_libraries.dal_enums.strategy import Name
from assetallocation_arp.data_etl.dal.arp_proc_caller import TimesProcCaller
from assetallocation_arp.data_etl.dal.data_models.strategy import Times, TimesAssetInput, DayOfWeek


class ReceiveDataTimes:
    def __init__(self):
        self.times_form = {}
        self.write_logs = {}
        self.inputs_existing_versions_times = {}
        self.assets_existing_versions_times = {}
        self.version_strategy = 0
        self.version_strategy_export = 0
        self.strategy_weight = 0
        self.strategy_weight_user = 0
        self.match_date_db = None
        self.date_to = None
        self.fund_name = None
        self.fund_name_export = None
        self.strategy = None
        self.type_of_request = None
        self._date_to_sidebar = None
        self.date_to_export_sidebar = None
        self.version_description = ''
        self.is_new_strategy = True
        self.domino_username = None

    @property
    def domino_username(self) -> bool:
        return self._domino_username

    @domino_username.setter
    def domino_username(self, x) -> None:
        self._domino_username = x

    @property
    def is_new_strategy(self) -> bool:
        return self._is_new_strategy

    @is_new_strategy.setter
    def is_new_strategy(self, x) -> None:
        self._is_new_strategy = x

    @property
    def version_description(self) -> bool:
        return self._version_description

    @version_description.setter
    def version_description(self, x) -> None:
        self._version_description = x

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
    def version_strategy(self):
        return int(self._version_strategy)

    @version_strategy.setter
    def version_strategy(self, value):
        self._version_strategy = value

    @property
    def version_strategy_export(self):
        return int(self._version_strategy_export)

    @version_strategy_export.setter
    def version_strategy_export(self, value):
        self._version_strategy_export = value

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
    def fund_name_export(self):
        return self._fund_name_export

    @fund_name_export.setter
    def fund_name_export(self, value):
        self._fund_name_export = value

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
        if value is not None:
            self._date_to_sidebar = dt.datetime.strptime(value, '%d/%m/%Y').date()

    @property
    def date_to_export_sidebar(self):
        return self._date_to_export_sidebar

    @date_to_export_sidebar.setter
    def date_to_export_sidebar(self, value) -> None:
        self._date_to_export_sidebar = pd.to_datetime(value, format='%d/%m/%Y')

    @staticmethod
    def _select_asset_tickers_with_names_and_subcategories_from_db():
        apc = TimesProcCaller()

        asset_tickers_names_subcategories = apc.select_asset_tickers_names_subcategories()

        return asset_tickers_names_subcategories.set_index(asset_tickers_names_subcategories.ticker)

    def select_tickers(self):
        """
        Select all asset tickers with names and subcategories that exist in the database
        :return: all asset tickers with names and subcategories
        """

        asset_tickers_names_subcategories = self._select_asset_tickers_with_names_and_subcategories_from_db()

        return asset_tickers_names_subcategories.ticker

    def select_names_subcategories(self, user_ticker):
        """
        Select all asset tickers with names and subcategories that exist in the database
        :return: all asset tickers with names and subcategories
        """

        asset_tickers_names_subcategories = self._select_asset_tickers_with_names_and_subcategories_from_db()

        ticker_selected_data = asset_tickers_names_subcategories.loc[user_ticker]

        name, subcategory = ticker_selected_data.loc["name"], ticker_selected_data.loc["subcategory"]

        return name, subcategory

    def check_in_date_to_existing_version(self) -> bool:
        apc = TimesProcCaller()
        result_dates = apc.select_all_fund_strategy_result_dates()
        result_dates = result_dates[(result_dates['fund_name'] == self.fund_name) & (result_dates['strategy_version'] == self.version_strategy)]
        return dt.date(self.date_to.year, self.date_to.month, self.date_to.day) in result_dates['business_date_to'].values

    def receive_data_latest_version_dashboard(self, business_date_to):
        apc = TimesProcCaller()
        self.version_strategy = max(apc.select_strategy_versions(Name.times))
        self.strategy_weight = apc.select_fund_strategy_weight(self.fund_name, Name.times, self.version_strategy)

    def receive_data_sidebar_dashboard(self, all_fund_strategy_result_dates: pd.DataFrame):

        data = all_fund_strategy_result_dates

        select_fund = data.loc[data['fund_name'] == self.fund_name]
        select_version = select_fund.loc[select_fund['strategy_version'] == self.version_strategy]
        select_date_to = [str(d.day) + "/" + str(d.month) + "/" + str(d.year) for d in
                          select_version.business_date_to.values.tolist()]

        return select_date_to

    def receive_data_existing_versions(self, strategy_version):
        apc = TimesProcCaller()
        self.version_strategy = strategy_version
        self.strategy = apc.select_strategy(strategy_version)

        # Inputs
        strategy_weight = apc.select_fund_strategy_weight(self.fund_name, Name.times, strategy_version)
        self.strategy_weight = strategy_weight or self.strategy_weight_user

        inputs_versions = {'fund': self.fund_name,
                           'version': strategy_version,
                           'input_date_from_times': '2000-01-01',
                           'input_date_to_times': self.date_to,
                           'input_strategy_weight_times': self.strategy_weight,
                           'input_time_lag_times': self.strategy.time_lag_in_days,
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

        return self.times_form

    def call_run_times(self, assets_input_times):

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

        # print(f"times.business_date_from: {times.business_date_from}", flush=True)
        # print(f"times.description: { times.description}", flush=True)
        # print(f"user_id: {os.environ.get('USERNAME')}", flush=True)
        # print(f"times.time_lag_interval: {times.time_lag_interval}", flush=True)
        # print(f"times.leverage_type.name: {times.leverage_type.name}", flush=True)
        # print(f"times.volatility_window: {times.volatility_window}", flush=True)
        # print(f"times.short_signals: {times.short_signals}", flush=True)
        # print(f"times.long_signals: {times.long_signals}", flush=True)
        # print(f"times.frequency.name: {times.frequency.name}", flush=True)
        # print(f"times.day_of_week.value: {times.day_of_week.value}", flush=True)

        times.description = self.version_description
        self.strategy = self.strategy_weight_user

        self.date_to = self.times_form['input_date_to_new_version_times']

        times.asset_inputs = [
            TimesAssetInput(h, int(i), j, k, float(l)) for h, i, j, k, l in zip(
                assets_input_times['input_asset'], assets_input_times['input_leverage'],
                assets_input_times['input_signal_ticker'],
                assets_input_times['input_future_ticker'], assets_input_times['input_costs']
            )
        ]

        print(f"fund_name: {self.fund_name}, strategy_weight_user = {self.strategy_weight_user}", flush=True)
        print(f"self.strategy: {self.strategy}", flush=True)

        fund_strategy = run_strategy(self.fund_name, float(self.strategy_weight_user),
                                     times, os.environ.get('USERNAME'),
                                     dt.datetime.strptime(self.times_form['input_date_from_times'], '%d/%m/%Y').date(),
                                     dt.datetime.strptime(self.times_form['input_date_to_new_version_times'], '%d/%m/%Y').date(),
                                     is_new_strategy=self.is_new_strategy
                                     )
        self.version_strategy = fund_strategy.strategy_version

        return fund_strategy

    def run_existing_strategy(self):
        fund_strategy = run_strategy(self.fund_name,
                                     float(self.strategy_weight),
                                     self.strategy,
                                     os.environ.get('USERNAME'),
                                     dt.datetime.strptime(self.inputs_existing_versions_times['input_date_from_times'],
                                                          '%Y-%m-%d').date(),
                                     self.inputs_existing_versions_times['input_date_to_times'],
                                     is_new_strategy=self.is_new_strategy
                                     )

        self.version_strategy = fund_strategy.strategy_version
        return fund_strategy
