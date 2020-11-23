import pandas as pd
import numpy as np

from assetallocation_arp.arp_strategies import run_effect_strategy
from assetallocation_arp.data_etl.inputs_effect.find_date import find_date

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
        self.effect_outputs, self.write_logs = run_effect_strategy(strategy_inputs, asset_inputs)


class ProcessDataEffect(ReceiveDataEffect):

    def __init__(self):
        super().__init__()
        self.quarterly_date_chart = ''

    @property
    def quarterly_date_chart(self):
        return self._quarterly_date_chart

    @quarterly_date_chart.setter
    def quarterly_date_chart(self, value):
        dates = [val.replace('/', '-') for val in value]
        self._quarterly_date_chart = dates

    def draw_regions_charts(self):
        # LatAm	CEEMA Asia regions
        region = self.effect_outputs['region']
        latam = self.effect_outputs['combo'][region['latam']].sum(axis=1).to_list()
        ceema = self.effect_outputs['combo'][region['ceema']].sum(axis=1).to_list()
        asia = self.effect_outputs['combo'][region['asia']].sum(axis=1).to_list()
        total_region = self.effect_outputs['combo'].sum(axis=1).to_list()
        average_region = [sum(total_region) / len(total_region)] * len(total_region)
        region_dates = self.effect_outputs['combo'].index.strftime("%Y-%m-%d").to_list()

        return {'latam': latam, 'ceema': ceema, 'asia': asia, 'total': total_region,
                'average': average_region, 'region_dates': region_dates}

    def draw_drawdown_chart(self):
        max_drawdown_no_signals_series = \
            self.effect_outputs['risk_returns']['max_drawdown']['all_max_drawdown_no_signals_series']
        max_drawdown_with_signals_series = \
            self.effect_outputs['risk_returns']['max_drawdown']['all_max_drawdown_with_signals_series']
        drawdown_dates = self.effect_outputs['risk_returns']['max_drawdown']['drawdown_dates']

        return {'max_drawdown_no_signals_series': max_drawdown_no_signals_series,
                'max_drawdown_with_signals_series': max_drawdown_with_signals_series,
                'drawdown_dates': drawdown_dates}

    def draw_year_to_date_contrib_chart(self):
        combo_data_tmp = self.effect_outputs['combo'].head(-1).tail(-1)

        log_ret_tmp = self.effect_outputs['log_ret'].head(-1).loc[pd.to_datetime('31-12-2019', format='%d-%m-%Y'):
                                                                  pd.to_datetime('30-09-2020', format='%d-%m-%Y'), :]
        combo_data_tmp = combo_data_tmp.loc[pd.to_datetime('31-12-2019', format='%d-%m-%Y'):
                                            pd.to_datetime('30-09-2020', format='%d-%m-%Y'), :]

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

    def draw_quarterly_profit_and_loss_chart(self, quarterly_date, end_quarterly_back_date, start_quarterly_live_date):
        # Quarterly P&L
        rng = pd.date_range(start=self.effect_outputs['combo'].index[0], end=self.effect_outputs['combo'].index[-1],
                            freq='Q')
        # combo_quarterly == log_quarterly for the dates range
        combo_quarterly = self.effect_outputs['combo'].reindex(rng, method='pad')
        dates_set = self.effect_outputs['combo'].index.values

        self.quarterly_date_chart = quarterly_date, end_quarterly_back_date, start_quarterly_live_date
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

    def run_process_data_effect(self, quarterly_date='31/03/2014', end_quarterly_back_date='30/06/2017',
                                start_quarterly_live_date='30/09/2017'):
        return {'region_chart': self.draw_regions_charts(),
                'drawdown_chart': self.draw_drawdown_chart(),
                'year_to_date_contrib_chart': self.draw_year_to_date_contrib_chart(),
                'quarterly_profit_and_loss_chart': self.draw_quarterly_profit_and_loss_chart(quarterly_date,
                                                                                             end_quarterly_back_date,
                                                                                             start_quarterly_live_date),
                'effect_data_form': self.effect_form,
                'effect_outputs': self.effect_outputs,
                'write_logs': self.write_logs}
