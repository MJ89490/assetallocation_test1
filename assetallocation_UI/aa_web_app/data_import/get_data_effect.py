import os
import pandas as pd
import numpy as np
import datetime as dt

from assetallocation_arp.models.effect.main_effect import run_effect
from assetallocation_arp.data_etl.dal.data_models.strategy import Effect, EffectAssetInput, DayOfWeek
from assetallocation_UI.aa_web_app.service.strategy import run_strategy
from assetallocation_arp.data_etl.inputs_effect.find_date import find_date
from assetallocation_arp.common_libraries.dal_enums.strategy import DayOfWeek
from assetallocation_arp.models.effect.read_inputs_effect import read_user_date
from assetallocation_arp.data_etl.dal.data_models.asset_analytic import AssetAnalytic

# TODO add class to another module


class ReceiveDataEffect:
    def __init__(self):
        self.effect_outputs = {}
        self.effect_form = {}
        self.write_logs = {}

    def receive_data_effect(self, form_data):
        for idx, val in enumerate(form_data):
            if idx > 1:
                self.effect_form[val.split('=', 1)[0]] = val.split('=', 1)[1]

        # Process date under format '12%2F09%2F2000 to 12/09/2000
        self.effect_form['input_user_date_effect'] = '/'.join(self.effect_form['input_user_date_effect'].split('%2F'))
        self.effect_form['input_signal_date_effect'] = '/'.join(self.effect_form['input_signal_date_effect'].split('%2F'))

        if 'Total' and 'return' in self.effect_form['input_trend_indicator_effect']:
            self.effect_form['input_trend_indicator_effect'] = ' '.join(self.effect_form['input_trend_indicator_effect'].split('%20'))

        if 'inverse' in self.effect_form['input_risk_weighting']:
            self.effect_form['input_risk_weighting'] = ' '.join(self.effect_form['input_risk_weighting'].split('%20'))
        else:
            self.effect_form['input_risk_weighting'] = '/'.join(self.effect_form['input_risk_weighting'].split('%2F'))

        return self.effect_form

    def call_run_effect(self, assets_inputs_effect):

        strategy_inputs = pd.DataFrame.from_dict(self.effect_form, orient='index').T
        asset_inputs = pd.DataFrame.from_dict(assets_inputs_effect, orient='index').T

        effect = Effect(
            self.effect_form['input_update_imf_effect'].strip().lower() == 'true',
            read_user_date(pd.to_datetime(self.effect_form['input_user_date_effect'], format='%d/%m/%Y')).date(),
            pd.to_datetime(self.effect_form['input_signal_date_effect'], format='%d/%m/%Y').date(),
            float(self.effect_form['input_position_size_effect']) / 100,
            self.effect_form['input_risk_weighting'].strip(), int(self.effect_form['input_window_effect']),
            int(self.effect_form['input_bid_ask_effect']), self.effect_form['input_real_nominal_effect'].strip().lower(),
            float(self.effect_form['input_threshold_effect']), DayOfWeek[self.effect_form['input_signal_day_effect']],
            self.effect_form['input_frequency_effect'], self.effect_form['input_include_shorts_effect'].strip().lower() == 'yes',
            float(self.effect_form['input_cut_off_long']), float(self.effect_form['input_cut_off_short']),
            int(self.effect_form['input_long_term_ma']), int(self.effect_form['input_short_term_ma']),
            self.effect_form['input_real_time_inf_effect'].strip().lower() == 'yes',
            self.effect_form['input_trend_indicator_effect'].strip().lower()
        )
        # TODO effect asset_subcategory is set as currency. refactor once database is restructured to link via asset_id!
        effect.asset_inputs = [EffectAssetInput(h, h, i, j, k, float(l), m, n) for h, i, j, k, l, m, n in
            zip(
                assets_inputs_effect['input_currency'], assets_inputs_effect['input_implied'],
                assets_inputs_effect['input_spot_ticker'], assets_inputs_effect['input_carry_ticker'],
                assets_inputs_effect['input_weight_usd'], assets_inputs_effect['input_usd_eur'],
                assets_inputs_effect['input_region']
            )
        ]


        # self.effect_outputs = run_effect(effect)

        # print()

        # float(self.effect_form['input_strategy_weight_effect']
        fund_strategy = run_strategy(
            "test_fund", 0.46,
            effect, os.environ.get('USERNAME'),
            dt.date(2000, 1, 1),
            dt.date(2020, 8, 12),
            True
        )
        return fund_strategy.analytics














        # self.effect_outputs, self.write_logs = run_strategy(strategy_inputs, asset_inputs,
        #                                                     dt.datetime.strptime(
        #                                                         "01/01/2000",
        #                                                         '%d/%m/%Y').date(),
        #                                                     dt.datetime.strptime(
        #                                                         "12/08/2020",
        #                                                         '%d/%m/%Y').date(),
        #                                                     is_new_strategy=True
        #                                                     )

        # self.effect_outputs = run_strategy("f1",
        #                                    float(0.46),
        #                                    effect,
        #                                    os.environ.get('USERNAME'),
        #                                    dt.datetime.strptime("01/01/2000", '%d/%m/%Y').date(),
        #                                    dt.datetime.strptime("12/08/2020",'%d/%m/%Y').date(),
        #                                    is_new_strategy=True
        #                              )


class ProcessDataEffect(ReceiveDataEffect):

    def __init__(self):
        super().__init__()
        self.quarterly_date_chart = ''
        self.start_quarterly_back_p_and_l_date = ''
        self.end_quarterly_back_p_and_l_date = ''
        self.start_quarterly_live_p_and_l_date = ''
        self.start_year_to_year_contrib_date = ''

    @property
    def quarterly_date_chart(self):
        return self._quarterly_date_chart

    @quarterly_date_chart.setter
    def quarterly_date_chart(self, value):
        if isinstance(value, str):
            dates = value.replace('/', '-')
        else:
            dates = [val.replace('/', '-') for val in value]
        self._quarterly_date_chart = dates

    @property
    def start_quarterly_back_p_and_l_date(self):
        return self._start_quarterly_back_p_and_l_date

    @start_quarterly_back_p_and_l_date.setter
    def start_quarterly_back_p_and_l_date(self, value):
        if value == '':
            self._start_quarterly_back_p_and_l_date = '31/03/2014'
        else:
            self._start_quarterly_back_p_and_l_date = value

    @property
    def end_quarterly_back_p_and_l_date(self):
        return self._end_quarterly_back_p_and_l_date

    @end_quarterly_back_p_and_l_date.setter
    def end_quarterly_back_p_and_l_date(self, value):
        if value == '':
            self._end_quarterly_back_p_and_l_date = '30/06/2017'
        else:
            self._end_quarterly_back_p_and_l_date = value

    @property
    def start_quarterly_live_p_and_l_date(self):
        return self._start_quarterly_live_p_and_l_date

    @start_quarterly_live_p_and_l_date.setter
    def start_quarterly_live_p_and_l_date(self, value):
        if value == '':
            self._start_quarterly_live_p_and_l_date = '30/09/2017'
        else:
            self._start_quarterly_live_p_and_l_date = value

    @property
    def start_year_to_year_contrib_date(self):
        return self._start_year_to_year_contrib_date

    @start_year_to_year_contrib_date.setter
    def start_year_to_year_contrib_date(self, value):
        if value == '':
            self._start_year_to_year_contrib_date = '31/12/2019'
        else:
            self._start_year_to_year_contrib_date = value

    def draw_regions_charts(self):
        region = self.effect_outputs['region']

        region_keys = region.keys()
        region_lst, region_names = [], []

        for key in region_keys:
            region_lst.append(self.effect_outputs['combo'][region[key]].sum(axis=1).to_list())
            region_names.append(key)

        total_region = self.effect_outputs['combo'].sum(axis=1).to_list()
        average_region = [sum(total_region) / len(total_region)] * len(total_region)
        region_dates = [self.effect_outputs['combo'].index.strftime("%Y-%m-%d").to_list()]

        region_names.append('Total')
        region_lst.append(total_region)
        region_names.append('Average')
        region_lst.append(average_region)

        return {'regions': region_lst, 'region_dates': region_dates, 'region_names': region_names}

    def draw_drawdown_chart(self):
        max_drawdown_no_signals_series = \
            self.effect_outputs['risk_returns']['max_drawdown']['all_max_drawdown_no_signals_series']
        max_drawdown_with_signals_series = \
            self.effect_outputs['risk_returns']['max_drawdown']['all_max_drawdown_with_signals_series']
        max_drawdown_jgenvuug = self.effect_outputs['risk_returns']['max_drawdown']['all_max_drawdown_jgenvuug']
        drawdown_dates = self.effect_outputs['risk_returns']['max_drawdown']['drawdown_dates']

        return {'max_drawdown_no_signals_series': max_drawdown_no_signals_series,
                'max_drawdown_with_signals_series': max_drawdown_with_signals_series,
                'max_drawdown_jgenvuug': max_drawdown_jgenvuug,
                'drawdown_dates': drawdown_dates}

    def draw_year_to_date_contrib_chart(self):
        combo_data_tmp = self.effect_outputs['combo'].head(-1).tail(-1)

        self.quarterly_date_chart = self.start_year_to_year_contrib_date
        start_year_to_year_contrib_date = self.quarterly_date_chart

        start_date = find_date(combo_data_tmp.index.values, pd.to_datetime(start_year_to_year_contrib_date, format='%d-%m-%Y'))
        end_date = find_date(combo_data_tmp.index.values, pd.to_datetime('30-09-2020', format='%d-%m-%Y'))

        log_ret_tmp = self.effect_outputs['log_ret'].head(-1).loc[start_date:end_date, :]
        combo_data_tmp = combo_data_tmp.loc[start_date:end_date, :]

        year_to_date_contrib_sum_prod = []

        for num_col in range(log_ret_tmp.shape[1]):
            tmp = []
            for values_combo, values_log in zip(combo_data_tmp.iloc[:, num_col], log_ret_tmp.iloc[:, num_col]):
                tmp.append(np.nanprod(values_combo * values_log))
            year_to_date_contrib_sum_prod.append((sum(tmp) * self.effect_outputs['pos_size']))

        year_to_date_contrib_sum_prod_total = [sum(year_to_date_contrib_sum_prod)]

        return {'year_to_year_contrib': year_to_date_contrib_sum_prod,
                'year_to_date_contrib_sum_prod_total': year_to_date_contrib_sum_prod_total,
                'names_curr': self.write_logs['currency_logs']}

    def draw_quarterly_profit_and_loss_chart(self):
        # Quarterly P&L
        rng = pd.date_range(start=self.effect_outputs['combo'].index[0], end=self.effect_outputs['combo'].index[-1],
                            freq='Q')
        # combo_quarterly == log_quarterly for the dates range
        combo_quarterly = self.effect_outputs['combo'].reindex(rng, method='pad')
        dates_set = self.effect_outputs['combo'].index.values

        self.quarterly_date_chart = self.start_quarterly_back_p_and_l_date, self.end_quarterly_back_p_and_l_date, self.start_quarterly_live_p_and_l_date
        start_quarterly_date, end_quarterly_back_date, start_quarterly_live_date = self.quarterly_date_chart

        start_quarterly = pd.to_datetime(start_quarterly_date, format='%d-%m-%Y')
        start_prev_quarterly_loc = combo_quarterly.index.get_loc(start_quarterly) - 1
        start_prev_quarterly = combo_quarterly.index[start_prev_quarterly_loc]

        quarterly_currency = pd.DataFrame()
        counter = 0

        # Loop through dates
        for currency_combo, currency_log in zip(self.effect_outputs['combo'], self.effect_outputs['log_ret'].head(-1)):
            quarterly_sum_prod = []

            for date in range(len(rng)):
                # Set the start date to start the computation
                start_current_date_index_loc = combo_quarterly.index.get_loc(start_prev_quarterly)
                start_current_date_index = find_date(dates_set, combo_quarterly.index[start_current_date_index_loc])

                # Take the next dates
                try:
                    start_next_date_index_loc = self.effect_outputs['combo'].index.get_loc(start_current_date_index) + 1
                    start_next_date_index = self.effect_outputs['combo'].index[start_next_date_index_loc]

                    next_start_date_index = find_date(dates_set,
                                                      combo_quarterly.index[start_current_date_index_loc + 1])
                except IndexError:
                    # We reach the end of the dates range, we can go to the next currency
                    break

                # Select the range of data according to the current and previous date
                combo_temp = self.effect_outputs['combo'].loc[start_next_date_index:next_start_date_index, currency_combo]
                log_temp = self.effect_outputs['log_ret'].head(-1).loc[start_next_date_index:next_start_date_index, currency_log]

                # Compute the sum prod between combo_temp and log_temp
                tmp = []
                for values_combo, values_log in zip(combo_temp.to_list(), log_temp.to_list()):
                    tmp.append(np.nanprod(values_combo * values_log))

                quarterly_sum_prod.append((sum(tmp) * self.effect_outputs['pos_size']))

                # Error handling when we reach the end of the dates range
                start_prev_quarterly = combo_quarterly.index[start_current_date_index_loc + 1]

            # Save the quarterly sum prod in a dataFrame
            quarterly_currency[self.write_logs['currency_logs'][counter]] = quarterly_sum_prod
            start_prev_quarterly = combo_quarterly.index[start_prev_quarterly_loc]
            counter += 1

        index_quarterly = combo_quarterly.loc[start_quarterly:].index.values

        quarterly_currency = quarterly_currency.set_index(index_quarterly)

        # Total (live)
        quarterly_currency['Total live'] = quarterly_currency.sum(axis=1)

        # Backtest
        backtest = self.create_backtest(quarterly_currency, start_quarterly_date, end_quarterly_back_date)

        # Live
        livetest = self.create_livetest(quarterly_currency, start_quarterly_live_date)

        # Set the quarters depending on the dates
        self.create_quarterly_dates(quarterly_currency)

        # Quarters for backtest
        quarters_backtest = quarterly_currency.loc[backtest['start_quarterly_backtest']:
                                                   backtest['end_quarterly_backtest'], 'Quarters'].to_list()
        # Quarters for live
        quarters_live = quarterly_currency.loc[livetest['start_quarterly_live']:, 'Quarters'].to_list()

        return {'backtest_quarterly_profit_and_loss': backtest['quarterly_backtest'],
                'live_quarterly_profit_and_loss': livetest['quarterly_live'],
                'quarterly_backtest_dates': backtest['quarterly_backtest_dates'],
                'quarterly_live_dates': livetest['quarterly_live_dates'],
                'quarters_backtest': quarters_backtest,
                'quarters_live': quarters_live}

    @staticmethod
    def create_backtest(quarterly_currency, quarterly_date, end_quarterly_back_date):
        start_quarterly_backtest = pd.to_datetime(quarterly_date, format='%d-%m-%Y')
        end_quarterly_backtest = pd.to_datetime(end_quarterly_back_date, format='%d-%m-%Y')
        quarterly_backtest = quarterly_currency.loc[start_quarterly_backtest:end_quarterly_backtest, 'Total live']
        quarterly_backtest_dates = quarterly_backtest.index.strftime("%Y-%m").to_list()
        return {'start_quarterly_backtest': start_quarterly_backtest,
                'end_quarterly_backtest': end_quarterly_backtest,
                'quarterly_backtest': quarterly_backtest.to_list(),
                'quarterly_backtest_dates': quarterly_backtest_dates}

    @staticmethod
    def create_livetest(quarterly_currency, start_quarterly_live_date):
        start_quarterly_live = pd.to_datetime(start_quarterly_live_date, format='%d-%m-%Y')
        quarterly_live = quarterly_currency.loc[start_quarterly_live:, 'Total live']
        quarterly_live_dates = quarterly_live.index.strftime("%Y-%m").to_list()
        return {'start_quarterly_live': start_quarterly_live,
                'quarterly_live': quarterly_live.to_list(),
                'quarterly_live_dates': quarterly_live_dates}

    @staticmethod
    def create_quarterly_dates(quarterly_currency):
        quarterly_currency.loc[pd.DatetimeIndex(quarterly_currency.index.values).month == 3, 'Quarters'] = 'Q1'
        quarterly_currency.loc[pd.DatetimeIndex(quarterly_currency.index.values).month == 6, 'Quarters'] = 'Q2'
        quarterly_currency.loc[pd.DatetimeIndex(quarterly_currency.index.values).month == 9, 'Quarters'] = 'Q3'
        quarterly_currency.loc[pd.DatetimeIndex(quarterly_currency.index.values).month == 12, 'Quarters'] = 'Q4'

    # TODO to move later to download_data_chart_effect.py when db set up
    def download_year_to_year_contrib_chart(self):
        combo = self.effect_outputs['combo'].head(-1).tail(-1)
        log_ret = self.effect_outputs['log_ret'].head(-1)
        df = pd.concat([combo, log_ret], ignore_index=False, sort=False, axis=1)
        # TODO to change to Domino format
        df.to_csv(r'C:\Users\AJ89720\download_data_charts_effect\year_to_year_contrib_chart.csv', index=True, header=True)

    def download_regions_charts(self):
        region = self.effect_outputs['region']
        latam = self.effect_outputs['combo'][region['latam']]
        ceema = self.effect_outputs['combo'][region['ceema']]
        asia = self.effect_outputs['combo'][region['asia']]
        df = pd.concat([latam, ceema, asia], ignore_index=False, sort=False, axis=1)
        # TODO to change to Domino format
        df.to_csv(r'C:\Users\AJ89720\download_data_charts_effect\region_chart.csv', index=True, header=True)

    def download_drawdown_chart(self):
        df = pd.DataFrame({'Exclude_shorts': self.effect_outputs['risk_returns']['max_drawdown']['all_max_drawdown_no_signals_series'],
                           'Include_shorts': self.effect_outputs['risk_returns']['max_drawdown']['all_max_drawdown_with_signals_series'],
                           'jgenvuug_index':  self.effect_outputs['risk_returns']['max_drawdown']['all_max_drawdown_jgenvuug']})
        df['Dates'] = self.effect_outputs['risk_returns']['max_drawdown']['drawdown_dates']
        df = df.set_index(df.Dates)
        del df['Dates']
        # TODO to change to Domino format
        df.to_csv(r'C:\Users\AJ89720\download_data_charts_effect\drawdown_chart.csv', index=True, header=True)

    def download_quarterly_profit_and_loss_chart(self):
        pass

    def download_aggregate_chart(self):
        df = pd.DataFrame({'Total_Excl_Signals': self.effect_outputs['total_excl_signals'],
                           'Total_Incl_Signals': self.effect_outputs['total_incl_signals'],
                           'Spot_Incl_Signals': self.effect_outputs['spot_incl_signals'],
                           'Spot_Excl_Signals': self.effect_outputs['spot_excl_signals']})
        df['Dates'] = self.effect_outputs['agg_dates']
        df = df.set_index(df.Dates)
        del df['Dates']
        # TODO to change to Domino format
        df.to_csv(r'C:\Users\AJ89720\download_data_charts_effect\aggregate_chart.csv', index=True, header=True)

    def run_process_data_effect(self):
        return {'region_chart': self.draw_regions_charts(),
                'drawdown_chart': self.draw_drawdown_chart(),
                'year_to_date_contrib_chart': self.draw_year_to_date_contrib_chart(),
                'quarterly_profit_and_loss_chart': self.draw_quarterly_profit_and_loss_chart(),
                'effect_data_form': self.effect_form,
                'effect_outputs': self.effect_outputs,
                'write_logs': self.write_logs}
