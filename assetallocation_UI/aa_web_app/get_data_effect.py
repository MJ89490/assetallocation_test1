import pandas as pd

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

        return {'latam': latam, 'ceema': ceema, 'asia': asia, 'total': total_region, 'average': average_region,
                'max_drawdown_no_signals_series': max_drawdown_no_signals_series,
                'max_drawdown_with_signals_series': max_drawdown_with_signals_series}

    def call_run_effect(self, assets_inputs_effect):

        strategy_inputs = pd.DataFrame.from_dict(self.effect_form, orient='index').T
        asset_inputs = pd.DataFrame.from_dict(assets_inputs_effect, orient='index').T

        self.effect_outputs, self.write_logs = run_effect_strategy(strategy_inputs, asset_inputs)











