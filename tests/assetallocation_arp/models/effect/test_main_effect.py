import os
import pandas as pd
import datetime as dt

from assetallocation_arp.models.effect.main_effect import run_effect
from assetallocation_arp.data_etl.dal.data_models.strategy import Effect
from assetallocation_arp.common_libraries.dal_enums.strategy import DayOfWeek, Frequency, TrendIndicator, CarryType, \
    RiskWeighting
from assetallocation_arp.data_etl.dal.data_models.asset import EffectAssetInput

all_data = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "all_date.csv")), sep=',', engine='python')
all_data = all_data.set_index(pd.to_datetime(all_data.Date, format='%Y-%m-%d'))
del all_data['Date']

asset_inputs = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "all_asset_inputs.csv")), sep=',', engine='python')

strategy_inputs = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "strategy_inputs.csv")), sep=',', engine='python')


def test_runs_through():
    e = Effect(strategy_inputs['input_update_imf_effect'].item() == 'TRUE',
        dt.datetime.strptime(strategy_inputs['input_user_date_effect'].item(), '%d/%m/%Y').date(),
        dt.datetime.strptime(strategy_inputs['input_signal_date_effect'].item(), '%d/%m/%Y').date(),
        strategy_inputs['input_position_size_effect'].item(),
        RiskWeighting[strategy_inputs['input_risk_weighting'].item()], strategy_inputs['input_window_effect'].item(),
        strategy_inputs['input_bid_ask_effect'].item(),
        CarryType[strategy_inputs['input_real_nominal_effect'].item().lower()],
        strategy_inputs['input_threshold_effect'].item(), DayOfWeek[strategy_inputs['input_signal_day_effect'].item()],
        Frequency[strategy_inputs['input_frequency_effect'].item()],
               strategy_inputs['input_include_shorts_effect'].item() == 'Yes',
        strategy_inputs['input_cut_off_long'].item(), strategy_inputs['input_cut_off_short'].item(),
        strategy_inputs['input_long_term_ma'].item(), strategy_inputs['input_short_term_ma'].item(),
               strategy_inputs['input_real_time_inf_effect'].item() == 'Yes',
        TrendIndicator[strategy_inputs['input_trend_indicator_effect'].item().lower()])

    dict_asset_input = asset_inputs.T.to_dict(orient='index')
    e.asset_inputs = [EffectAssetInput(h, h, i, j, k, float(l), m, n) for h, i, j, k, l, m, n in
                           zip(dict_asset_input['currency'].values(), dict_asset_input['input_implied'].values(),
                               dict_asset_input['input_spot_ticker'].values(), dict_asset_input['input_carry_ticker'].values(),
                               dict_asset_input['input_weight_usd'].values(), dict_asset_input['input_usd_eur'].values(),
                               dict_asset_input['input_region'].values())]

    run_effect(e, all_data)

