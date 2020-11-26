import os

import pandas as pd
import numpy as np

from assetallocation_arp.data_etl.dal.data_models.strategy import Effect
from assetallocation_arp.data_etl.dal.data_models.asset import EffectAssetInput
from assetallocation_UI.aa_web_app.service.strategy import run_strategy


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
        log_ret_data = self.effect_outputs['log_ret'].head(-1)
        combo_data_tmp = combo_data.head(-1).tail(-1)

        log_ret_tmp = log_ret_data.loc[pd.to_datetime('31-12-2019', format='%d-%m-%Y'):pd.to_datetime('30-09-2020', format='%d-%m-%Y'), :]
        combo_data_tmp = combo_data_tmp.loc[pd.to_datetime('31-12-2019', format='%d-%m-%Y'):pd.to_datetime('30-09-2020', format='%d-%m-%Y'), :]

        year_to_date_contrib_sum_prod = []

        for num_col in range(log_ret_tmp.shape[1]):
            tmp = []
            for values_combo, values_log in zip(combo_data_tmp.iloc[:, num_col], log_ret_tmp.iloc[:, num_col]):
                tmp.append(np.nanprod(values_combo * values_log))
            year_to_date_contrib_sum_prod.append((sum(tmp) * self.effect_outputs['pos_size'])*100)

        year_to_date_contrib_sum_prod_total = [sum(year_to_date_contrib_sum_prod)]
        names_curr = self.write_logs['currency_logs']

        # Quarterly P&L
        start_quarterly = pd.to_datetime('31-03-2014', format='%d-%m-%Y')
        rng = pd.date_range(start=combo_data.index[0], end=combo_data.index[-1], freq='Q')
        # combo_quarterly == log_quarterly for the dates range
        combo_quarterly = combo_data.reindex(rng, method='pad')
        dates_set = combo_data.index.values

        from assetallocation_arp.data_etl.inputs_effect.find_date import find_date
        quarterly_currency = pd.DataFrame()

        # Loop through dates
        for currency_combo, currency_log in zip(combo_data, log_ret_data):
            for date in range(len(dates_set)):
                # Set the start date to start the computation
                start_current_date_index_loc = combo_quarterly.index.get_loc(start_quarterly)
                start_current_date_index = find_date(dates_set, combo_quarterly.index[start_current_date_index_loc])

                # Take the previous dates
                previous_start_date_index = find_date(dates_set, combo_quarterly.index[start_current_date_index_loc - 1])

                # Select the range of data according to the current and previous date
                combo_temp = combo_data.iloc[previous_start_date_index:start_current_date_index, currency_combo]
                log_temp = log_ret_data.iloc[previous_start_date_index:start_current_date_index, currency_log]

                # Compute the sumprod between combo_temp and log_temp
                quarterly_sum_prod = []

                for num_col in range(combo_temp.shape[1]):
                    tmp = []
                    for values_combo, values_log in zip(combo_temp.iloc[:, num_col], log_temp.iloc[:, num_col]):
                        tmp.append(np.nanprod(values_combo * values_log))
                    quarterly_sum_prod.append((sum(tmp) * self.effect_outputs['pos_size']) * 100)

            # Save the quarterly sum prod in a dataFrame
            quarterly_currency[currency_combo[:3]] = quarterly_sum_prod

            # Error handling when we reach the end of the dates range

        # combo_quarterly = combo_data.reindex(rng_quarterly, method='pad').loc[start_quarterly:]
        # log_ret_quarterly = log_ret_data.reindex(rng_quarterly, method='pad').loc[start_quarterly:]
        #
        # current_date_quarterly = pd.to_datetime('31-03-2014', format='%d-%m-%Y')

        return {'latam': latam, 'ceema': ceema, 'asia': asia, 'total': total_region, 'average': average_region,
                'max_drawdown_no_signals_series': max_drawdown_no_signals_series,
                'max_drawdown_with_signals_series': max_drawdown_with_signals_series,
                'year_to_year_contrib': year_to_date_contrib_sum_prod,
                'year_to_date_contrib_sum_prod_total': year_to_date_contrib_sum_prod_total,
                'names_curr': names_curr}

    def call_run_effect(self, assets_inputs_effect) -> 'FundStrategy':
        effect = Effect(
            self.effect_form['input_update_imf_effect'], self.effect_form['input_user_date_effect'],
            self.effect_form['input_signal_date_effect'], self.effect_form['input_position_size_effect'],
            self.effect_form['input_risk_weighting'], self.effect_form['input_window_effect'],
            self.effect_form['input_bid_ask_effect'], self.effect_form['input_real_nominal_effect'],
            self.effect_form['input_threshold_effect'], self.effect_form['input_signal_day_effect'],
            self.effect_form['input_frequency_effect'], self.effect_form['input_include_shorts_effect'],
            self.effect_form['input_cut_off_long'], self.effect_form['input_cut_off_short'],
            self.effect_form['input_long_term_ma'], self.effect_form['input_short_term_ma'],
            self.effect_form['input_real_time_inf_effect'], self.effect_form['input_trend_indicator_effect']
        )
        effect.asset_inputs = [
            EffectAssetInput(h, i, j, k, float(l), m, n) for h, i, j, k, l, m, n in
            zip(
                assets_inputs_effect['input_currency'], assets_inputs_effect['input_implied'],
                assets_inputs_effect['input_spot_ticker'], assets_inputs_effect['input_carry_ticker'],
                assets_inputs_effect['input_weight_usd'], assets_inputs_effect['input_usd_eur'],
                assets_inputs_effect['input_region']
            )
        ]
        fund_strategy = run_strategy(
            self.effect_form['input_fund_name_effect'], float(self.effect_form['input_strategy_weight_effect']),
            effect, os.environ.get('USERNAME')
        )
        return fund_strategy











