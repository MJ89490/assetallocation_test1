from assetallocation_arp.arp_strategies import run_effect_strategy


class ReceivedDataEffect:
    def __init__(self):
        self.effect_outputs = {}
        self.effect_form = {}
        self.write_logs = {}

    @property
    def effect_data_form(self):
        return self.effect_form

    def received_data_effect(self, form_data):
        effect_form = {}
        for idx, val in enumerate(form_data):
            if idx > 1:
                effect_form[val.split('=', 1)[0]] = val.split('=', 1)[1]

        # Process date under format '12%2F09%2F2000 to 12/09/2000
        effect_form['input_user_date_effect'] = '/'.join(effect_form['input_user_date_effect'].split('%2F'))
        effect_form['input_signal_date_effect'] = '/'.join(effect_form['input_signal_date_effect'].split('%2F'))

        if 'Total' and 'return' in effect_form['input_trend_indicator_effect']:
            effect_form['input_trend_indicator_effect'] = ' '.join(effect_form['input_trend_indicator_effect'].split('%20'))

        if 'inverse' in effect_form['input_risk_weighting']:
            effect_form['input_risk_weighting'] = ' '.join(effect_form['input_risk_weighting'].split('%20'))
        else:
            effect_form['input_risk_weighting'] = '/'.join(effect_form['input_risk_weighting'].split('%2F'))

        print(effect_form)
        self.effect_form = effect_form
        return effect_form

    def call_run_effect(self):

        self.effect_outputs, self.write_logs = run_effect_strategy()

        # p = self.effect_outputs['profit_and_loss']



        print()






