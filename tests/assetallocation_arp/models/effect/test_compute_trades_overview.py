import os
import pytest
import numpy as np
import pandas as pd

from assetallocation_arp.models.effect.compute_profit_and_loss_overview import ComputeProfitAndLoss
from assetallocation_arp.models.effect.compute_trades_overview import compute_trades_overview
from assetallocation_arp.models.effect.compute_currencies import ComputeCurrencies
from data_etl.inputs_effect.compute_inflation_differential import ComputeInflationDifferential
from assetallocation_arp.models.effect.compute_signals_overview import ComputeSignalsOverview

"""
Notes: 
    TrendIndicator: Total Return
    Short-term: 4
    Long-term: 16 
    Incl Shorts: Yes
    Cut-off long: 2.0% 
    Cut-off short: 0.0% 
    Real/Nominal: real
    Realtime Inflation F'cast: Yes
    Threshold for closing: 0.25%
    Risk-weighting: 1/N
    STDev window (weeks): 52
    Bid-ask spread (bp): 10
    Position size: 3%
"""


@pytest.mark.parametrize("trades_overview_origin, trades_overview_results",
                         [("trades_overview_one_origin.csv", "trades_overview_one_results.csv"),
                          ("trades_overview_two_origin.csv", "trades_overview_two_results.csv")])
def test_compute_trades_overview(trades_overview_origin, trades_overview_results):
    all_data = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "all_date.csv")), sep=',', engine='python')
    all_data = all_data.set_index(pd.to_datetime(all_data.Date, format='%Y-%m-%d'))
    del all_data['Date']
    obj_import_data = ComputeCurrencies(asset_inputs=pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "asset_inputs.csv")), sep=',', engine='python'),
                                        bid_ask_spread=10,
                                        frequency_mat='weekly',
                                        end_date_mat='23/09/2020',
                                        signal_day_mat='WED',
                                        all_data=all_data)
    obj_import_data.process_all_data_effect()

    obj_import_data.start_date_calculations = pd.to_datetime('12-01-2000', format='%d-%m-%Y')

    # Inflation differential calculations
    obj_inflation_differential = ComputeInflationDifferential(dates_index=obj_import_data.dates_index)
    realtime_inflation_forecast, imf_data_update = 'Yes', False
    inflation_differential, currency_logs = obj_inflation_differential.compute_inflation_differential(
                                                                realtime_inflation_forecast,
                                                                obj_import_data.all_currencies_spot,
                                                                obj_import_data.currencies_spot['currencies_spot_usd'],
                                                                imf_data_update=imf_data_update)

    # Inputs
    trend_inputs = {'short_term': 4, 'long_term': 16, 'trend': 'total return'}
    carry_inputs = {'type': 'real', 'inflation': inflation_differential}
    combo_inputs = {'cut_off': 2, 'incl_shorts': 'Yes', 'cut_off_s': 0.00, 'threshold': 0.25}

    currencies_calculations = obj_import_data.run_compute_currencies(carry_inputs, trend_inputs, combo_inputs)

    obj_compute_profit_and_loss = ComputeProfitAndLoss(latest_date=pd.to_datetime('23-09-2020', format='%d-%m-%Y'),
                                                       position_size_attribution=0.03,
                                                       index_dates=obj_import_data.dates_origin_index,
                                                       frequency='weekly')

    obj_compute_signals_overview = ComputeSignalsOverview(latest_signal_date=pd.to_datetime('23-09-2020', format='%d-%m-%Y'),
                                                          size_attr=0.03,
                                                          window=52,
                                                          next_latest_date=obj_import_data)

    p_and_l_combo = obj_compute_profit_and_loss.compute_profit_and_loss_combo(currencies_calculations['combo_curr'])
    signals_combo_overview = obj_compute_signals_overview.compute_signals_trend(currencies_calculations['combo_curr'])

    trades = compute_trades_overview(p_and_l_combo, signals_combo_overview)

    assert trades.item() == 0
