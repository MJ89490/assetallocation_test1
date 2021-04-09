import os
import pandas as pd
import datetime as dt

from assetallocation_arp.models.effect.main_effect import run_effect
from assetallocation_arp.data_etl.dal.data_models.strategy import Effect, EffectAssetInput, DayOfWeek
from assetallocation_UI.aa_web_app.service.strategy import run_strategy

from assetallocation_arp.common_libraries.dal_enums.strategy import DayOfWeek
from assetallocation_arp.models.effect.read_inputs_effect import read_user_date
from assetallocation_arp.data_etl.dal.data_models.asset_analytic import AssetAnalytic

# TODO add class to another module


class ReceiveDataEffect:
    def __init__(self):
        self.effect_outputs = {}
        self.effect_form = {}
        self.write_logs = {}
        self.version_strategy = None
        self.version_description = None

    @property
    def version_strategy(self):
        return int(self._version_strategy)

    @version_strategy.setter
    def version_strategy(self, value):
        self._version_strategy = value

    @property
    def version_description(self) -> bool:
        return self._version_description

    @version_description.setter
    def version_description(self, x) -> None:
        self._version_description = x

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

        # description of the strategy
        effect.description = self.version_description

        # TODO effect asset_subcategory is set as currency. refactor once database is restructured to link via asset_id!
        effect.asset_inputs = [EffectAssetInput(h, h, i, j, k, float(l), m, n) for h, i, j, k, l, m, n in
            zip(
                assets_inputs_effect['input_currency'], assets_inputs_effect['input_implied'],
                assets_inputs_effect['input_spot_ticker'], assets_inputs_effect['input_carry_ticker'],
                assets_inputs_effect['input_weight_usd'], assets_inputs_effect['input_usd_eur'],
                assets_inputs_effect['input_region']
            )
        ]

        # run the strategy
        fund_strategy = run_strategy("test_fund",
                                     0.46,
                                     effect,
                                     os.environ.get('USERNAME'),
                                     dt.date(2000, 1, 1),
                                     dt.date(2020, 8, 12),
                                     True
                                     )

        # strategy version
        self.version_strategy = fund_strategy.strategy_version

        return fund_strategy



