"""
Created on Fri Nov  15 17:27:51 2019
TIMES
@author: SN69248
"""
from typing import List, Tuple

import numpy as np
import pandas as pd
from pandas.tseries.offsets import BDay

from assetallocation_arp.common_libraries.dal_enums.strategy import Leverage, DayOfWeek
from assetallocation_arp.models import portfolio_construction as pc
from assetallocation_arp.models import arp_signals as arp
from assetallocation_arp.data_etl.dal.data_models.strategy import Times
from assetallocation_arp.data_etl.dal.data_models.asset import TimesAssetInput
from assetallocation_arp.data_etl.dal.data_frame_converter import DataFrameConverter
from assetallocation_arp.data_etl.dal.data_models.fund_strategy import FundStrategy, FundStrategyAssetAnalytic, FundStrategyAssetWeight
from assetallocation_arp.common_libraries.dal_enums.fund_strategy import Category, Signal, Performance


def format_data_and_calc(times_inputs, asset_inputs, all_data):

    # format data and inputs
    asset_inputs_t = asset_inputs.set_index('asset').T
    # all_data = all_data[all_data.index.values > np.datetime64(times_inputs['date_from'].item())]
    times_data = all_data[asset_inputs.signal_ticker]
    futures_data = all_data[asset_inputs.future_ticker].pct_change()
    times_data.columns = asset_inputs.asset
    futures_data.columns = asset_inputs.asset
    #
    costs = asset_inputs_t.loc['costs']
    leverage = asset_inputs_t.loc['s_leverage']
    leverage_type = times_inputs['leverage_type'].item()

    # apply leverage
    leverage_data = pc.apply_leverage(futures_data, leverage_type, leverage)
    leverage_data[leverage.index[leverage.isnull()]] = np.nan
    index_df = futures_data.append(pd.DataFrame(index=futures_data.iloc[[-1]].index + BDay(2)), sort=True).index
    leverage_data = leverage_data.shift(periods=times_inputs['time_lag'].item(), freq='D', axis=0).reindex(index_df,
                                                                                                           method='pad')
    # calculate signals
    t = Times(DayOfWeek[times_inputs['week_day'].iat[0]], times_inputs['frequency'].iat[0],
              times_inputs['leverage_type'].iat[0],
              [times_inputs['sig1_long'].iat[0], times_inputs['sig2_long'].iat[0], times_inputs['sig3_long'].iat[0]],
              [times_inputs['sig1_short'].iat[0], times_inputs['sig2_short'].iat[0], times_inputs['sig3_short'].iat[0]],
              times_inputs['time_lag'].iat[0], times_inputs['volatility_window'].iat[0])
    signals = arp.momentum(times_data, t)
    # calculate leveraged positions and returns
    if leverage_type == Leverage.s.name:
        (returns, r, positioning) = pc.return_ts(signals, futures_data, leverage_data, costs, False)
    else:
        (returns, r, positioning) = pc.return_ts(signals, futures_data, leverage_data, costs, True)
        (returns, r, positioning) = pc.rescale(returns, r, positioning, "Total", 0.01)

    return signals, returns, r, positioning


def calculate_signals_returns_r_positioning(times: Times) -> \
        Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    asset_inputs, future_assets, signal_assets = get_asset_data_as_data_frames(times.asset_inputs)
    future_assets = future_assets.pct_change()

    signals = arp.momentum(signal_assets, times)

    future_leverage = asset_inputs[['future_ticker', 's_leverage']].set_index('future_ticker')['s_leverage']
    leverage_data = pc.apply_leverage(future_assets, times.leverage_type, future_leverage)
    leverage_data[asset_inputs['s_leverage'].index[asset_inputs['s_leverage'].isnull()]] = np.nan
    index_df = future_assets.append(pd.DataFrame(index=future_assets.iloc[[-1]].index + BDay(2)), sort=True).index
    leverage_data = leverage_data.shift(periods=times.time_lag_in_months, freq='D', axis=0).reindex(index_df,
                                                                                                    method='pad')

    # calculate leveraged positions and returns
    cost = asset_inputs[['cost', 'signal_ticker']].set_index('signal_ticker')['cost']

    fut_sig_ticker = dict(zip(asset_inputs['future_ticker'], asset_inputs['signal_ticker']))
    future_assets.columns = [fut_sig_ticker[i] for i in future_assets.columns]
    leverage_data.columns = [fut_sig_ticker[i] for i in leverage_data.columns]
    if times.leverage_type == Leverage.s:
        returns, r, positioning = pc.return_ts(signals, future_assets, leverage_data, cost, False)

    else:
        returns, r, positioning = pc.return_ts(signals, future_assets, leverage_data, cost, True)
        returns, r, positioning = pc.rescale(returns, r, positioning, "Total", 0.01)

    return signals, returns, r, positioning


def get_asset_data_as_data_frames(asset_inputs: List[TimesAssetInput]) -> Tuple[
    pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    signal_assets, future_assets = [], []

    for i in asset_inputs:
        signal_assets.append(i.signal_asset)
        future_assets.append(i.future_asset)

    signal_assets = DataFrameConverter.assets_to_df(signal_assets)
    future_assets = DataFrameConverter.assets_to_df(future_assets)
    asset_inputs = DataFrameConverter.times_asset_inputs_to_df(asset_inputs)

    return asset_inputs, future_assets, signal_assets


