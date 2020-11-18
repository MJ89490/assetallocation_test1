import pandas as pd
import numpy as np

from assetallocation_arp.arp_strategies import run_effect_strategy


class ReceivedDataEffect:
    def __init__(self):
        self.effect_outputs = {}
        self.effect_form = {}
        self.write_logs = {}

    @property
    def effect_data_form(self):
        return self.effect_form

    def process_received_data_effect(self, form_data):
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

        print(self.effect_form)

        return self.effect_form

    def process_data_charts_(self):
        combo_data = self.effect_outputs['combo']
        # LatAm	CEEMA Asia regions
        region = self.effect_outputs['region']
        latam = combo_data[region['latam']].sum(axis=1).to_list()
        ceema = combo_data[region['ceema']].sum(axis=1).to_list()
        asia = combo_data[region['asia']].sum(axis=1).to_list()
        total_region = combo_data.sum(axis=1).to_list()
        average_region = [sum(total_region) / len(total_region)] * len(total_region)
        max_drawdown_no_signals_series = self.effect_outputs['risk_returns']['max_drawdown']['all_max_drawdown_no_signals_series']
        max_drawdown_with_signals_series = self.effect_outputs['risk_returns']['max_drawdown']['all_max_drawdown_with_signals_series']

        # Year to date contribution
        log_ret = self.effect_outputs['log_ret'].head(-1)
        combo_data_tmp = combo_data.head(-1).tail(-1)

        log_ret = log_ret.loc[pd.to_datetime('31-12-2019', format='%d-%m-%Y'):pd.to_datetime('30-09-2020', format='%d-%m-%Y'), :]
        combo_data_tmp = combo_data_tmp.loc[pd.to_datetime('31-12-2019', format='%d-%m-%Y'):pd.to_datetime('30-09-2020', format='%d-%m-%Y'), :]

        year_to_date_contrib_sum_prod = []

        for num_col in range(log_ret.shape[1]):
            tmp = []
            for values_combo, values_log in zip(combo_data_tmp.iloc[:, num_col], log_ret.iloc[:, num_col]):
                tmp.append(np.nanprod(values_combo * values_log))
            year_to_date_contrib_sum_prod.append((sum(tmp) * self.effect_outputs['pos_size'])*100)

        year_to_date_contrib_sum_prod_total = [sum(year_to_date_contrib_sum_prod)]
        names_curr = self.write_logs['currency_logs']

        # Quarterly P&L
        # combo_quarterly_tmp = combo_data
        # Select quarterly months
        # combo_quarterly = combo_quarterly_tmp.loc[(pd.DatetimeIndex(combo_quarterly_tmp['Dates']).month == 3) |
        #                                           (pd.DatetimeIndex(combo_quarterly_tmp['Dates']).month == 6) |
        #                                           (pd.DatetimeIndex(combo_quarterly_tmp['Dates']).month == 9) |
        #                                           (pd.DatetimeIndex(combo_quarterly_tmp['Dates']).month == 12)]

        rng_quarterly = pd.date_range(start=combo_data.index[0], end=combo_data.index[-1], freq='Q')
        combo_quarterly = combo_data.reindex(rng_quarterly, method='pad')
        log_ret_quarterly = log_ret.reindex(rng_quarterly, method='pad')

        return {'latam': latam, 'ceema': ceema, 'asia': asia, 'total': total_region, 'average': average_region,
                'max_drawdown_no_signals_series': max_drawdown_no_signals_series,
                'max_drawdown_with_signals_series': max_drawdown_with_signals_series,
                'year_to_year_contrib': year_to_date_contrib_sum_prod,
                'year_to_date_contrib_sum_prod_total': year_to_date_contrib_sum_prod_total,
                'names_curr': names_curr}

    def call_run_effect(self, assets_inputs_effect):

        strategy_inputs = pd.DataFrame.from_dict(self.effect_form, orient='index').T
        asset_inputs = pd.DataFrame.from_dict(assets_inputs_effect, orient='index').T

        self.effect_outputs, self.write_logs = run_effect_strategy(strategy_inputs, asset_inputs)











