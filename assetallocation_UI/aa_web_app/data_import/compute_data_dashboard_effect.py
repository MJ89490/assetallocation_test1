import datetime
import numpy as np
import pandas as pd

from assetallocation_arp.common_libraries.dal_enums.fund_strategy import AggregationLevel, Signal, Performance

from assetallocation_arp.common_libraries.dal_enums.strategy import Name
from assetallocation_arp.data_etl.inputs_effect.find_date import find_date
from assetallocation_arp.data_etl.dal.arp_proc_caller import EffectProcCaller
from assetallocation_arp.data_etl.dal.data_frame_converter import EffectDataFrameConverter
from assetallocation_UI.aa_web_app.data_import.receive_data_effect import ReceiveDataEffect


class ComputeDataDashboardEffect:

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

    def call_effect_proc_caller(self, fund_name: str, version_strategy: int, date_to, date_to_sidebar=None) -> None:
        """
        Call Times proc caller to grab the data from the db
        :param fund_name: name of the current fund (example: f1, f2,...)
        :param version_strategy: version of the current strategy (version1, version2, ...)
        :param date_to_sidebar: date to sidebar
        :return: None
        """
        fund_name = 'test_fund'
        epc = EffectProcCaller()
        fs = epc.select_fund_strategy_results(fund_name, Name.effect, version_strategy,
                                              business_date_from=datetime.datetime.strptime('01/01/2000', '%d/%m/%Y').date(),
                                              business_date_to=date_to
                                              )
        weight_df = EffectDataFrameConverter.fund_strategy_asset_weights_to_df(fs.asset_weights)

        strategy_analytics, asset_analytics = [], []

        for analytic in fs.analytics:
            if analytic.aggregation_level == AggregationLevel.strategy:
                strategy_analytics.append(analytic)
            else:
                asset_analytics.append(analytic)

        strategy_analytic_df = EffectDataFrameConverter.fund_strategy_analytics_to_df(strategy_analytics)
        asset_analytics_df = EffectDataFrameConverter.fund_strategy_asset_analytics_to_df(asset_analytics)

        trend = asset_analytics_df.xs(Signal.trend, level='analytic_subcategory')
        carry = asset_analytics_df.xs(Signal.carry, level='analytic_subcategory')
        total_incl_signals = strategy_analytic_df[Performance['total return index incl signals']]
        total_excl_signals = strategy_analytic_df[Performance['total return index excl signals']]

        print('trend', '\n', trend.head())
        print('carry', '\n', carry.head())
        print('total_incl_signals', '\n', total_incl_signals.head())
        print('total_excl_signals', '\n', total_excl_signals.head())

        # total_excl_signals = strategy_analytic_df.xs(Performance['total return index excl signals'],
        #                                              # level='analytic_subcategory')

    def get_regions(self, version_strategy: int):

        apc = EffectProcCaller()
        strategy = apc.select_strategy(version_strategy)

        # strategy.position_size

        asset_inputs = [
            (
                i.asset_subcategory, i.asset_3m.ticker, i.spot_asset.ticker, i.carry_asset.ticker, i.usd_weight,
                i.base.name, i.region
            ) for i in strategy.asset_inputs
        ]
        asset_inputs = pd.DataFrame(
            asset_inputs,
            columns=[
                'currency', 'input_implied', 'input_spot_ticker', 'input_carry_ticker', 'input_weight_usd',
                'input_usd_eur',
                'input_region'
            ]
        )

        region = {}

        unique_region = np.unique(asset_inputs['input_region'].to_list())

        for reg in unique_region:
            region_tmp = asset_inputs.loc[asset_inputs['input_region'] == reg]
            curr = ['Combo_' + val for val in region_tmp['input_spot_ticker'].to_list()]
            region[reg.lower()] = curr

        return region











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


if __name__ == "__main__":
    apc = EffectProcCaller()
    v = apc.engine.connect().execute("SELECT * FROM arp.strategy_analytic")

    for a in v.fetchall():
        print(a.value)



    fs = apc.select_fund_strategy_results("test_fund", Name.effect, 55,
                                          business_date_from=datetime.datetime.strptime('01/01/2000',
                                                                                        '%d/%m/%Y').date(),
                                          business_date_to=datetime.date(2020, 8, 12)
                                          )

    print(fs)