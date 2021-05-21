import datetime as dt
from assetallocation_UI.aa_web_app.service.strategy import run_strategy
from assetallocation_arp.data_etl.dal.data_models.strategy import Times, TimesAssetInput, DayOfWeek


class CallRunTimes:

    def __init__(self, fund_name, strategy_weight, user_name, strategy_description, is_new_strategy=True):

        self.fund_name = fund_name
        self.strategy_weight = strategy_weight
        self.user_name = user_name
        self.strategy_description = strategy_description
        self.is_new_strategy = is_new_strategy

    @staticmethod
    def process_data_times(form_data):

        # if self.is_new_strategy:
        tmp = {}
        for idx, val in enumerate(form_data):
            # if idx > 1:
            tmp[val.split('=', 1)[0]] = val.split('=', 1)[1]

        # Process date under format '12%2F09%2F2000 to 01/01/2000
        tmp['input_date_from_times'] = '/'.join(tmp['input_date_from_times'].split('%2F'))
        tmp['input_date_to_new_version_times'] = '/'.join(tmp['input_date_to_new_version_times'].split('%2F'))
        times_form = tmp

        return times_form

    def call_run_times(self, assets_input_times, times_form):

        long_signals = list(map(float, [times_form['input_signal_one_long_times'],
                                        times_form['input_signal_two_long_times'],
                                        times_form['input_signal_three_long_times']]))

        short_signals = list(map(float, [times_form['input_signal_one_short_times'],
                                         times_form['input_signal_two_short_times'],
                                         times_form['input_signal_three_short_times']]))

        times = Times(DayOfWeek[times_form['input_weekday_times'].upper()],
                      times_form['input_frequency_times'].lower(),
                      times_form['input_leverage_times'], long_signals, short_signals,
                      int(times_form['input_time_lag_times']),
                      int(times_form['input_vol_window_times']))

        times.description = self.strategy_description

        date_to = times_form['input_date_to_new_version_times']

        times.asset_inputs = [
            TimesAssetInput(h, int(i), j, k, float(l)) for h, i, j, k, l in zip(
                assets_input_times['input_asset'], assets_input_times['input_leverage'],
                assets_input_times['input_signal_ticker'],
                assets_input_times['input_future_ticker'], assets_input_times['input_costs']
            )
        ]

        print(f"----- fund_name ------- = {self.fund_name}", flush=True)
        print(f"----- self.strategy_weight ----- = {self.strategy_weight}", flush=True)
        print(f"----- self.user_name ----- = {self.user_name}", flush=True)

        fund_strategy = run_strategy(self.fund_name,
                                     float(self.strategy_weight),
                                     times,
                                     self.user_name,
                                     dt.datetime.strptime(times_form['input_date_from_times'], '%d/%m/%Y').date(),
                                     dt.datetime.strptime(times_form['input_date_to_new_version_times'], '%d/%m/%Y').date(),
                                     is_new_strategy=self.is_new_strategy
                                     )
        # self.strategy_version = fund_strategy.strategy_version

        return fund_strategy, date_to
