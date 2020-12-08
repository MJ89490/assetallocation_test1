import os
import pandas as pd

from assetallocation_arp.models.effect.main_effect import run_effect
from assetallocation_arp.data_etl.dal.data_models.strategy import Effect
from assetallocation_arp.common_libraries.dal_enums.strategy import DayOfWeek, Frequency, TrendIndicator, CarryType, \
    RiskWeighting

all_data = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "all_date.csv")), sep=',', engine='python')
all_data = all_data.set_index(pd.to_datetime(all_data.Date, format='%Y-%m-%d'))
del all_data['Date']

asset_inputs = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "all_asset_inputs.csv")), sep=',', engine='python')

strategy_inputs = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "strategy_inputs.csv")), sep=',', engine='python')

def test_runs_through():
    e = Effect(strategy_inputs['input_update_imf_effect'].item() == 'TRUE',
        pd.to_datetime(strategy_inputs['input_user_date_effect'].item(), format='%d/%m/%Y'),
        pd.to_datetime(strategy_inputs['input_signal_date_effect'].item(), format='%d/%m/%Y'),
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
        TrendIndicator[strategy_inputs['input_trend_indicator_effect'].item().lower()], )

    run_effect(e, asset_inputs, all_data)

