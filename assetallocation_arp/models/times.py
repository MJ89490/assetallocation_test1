"""
Created on Fri Nov  15 17:27:51 2019
TIMES
@author: SN69248
"""
from typing import List, Tuple, Union

import numpy as np
import pandas as pd
from pandas.tseries.offsets import BDay

from assetallocation_arp.common_libraries.dal_enums.strategy import Leverage, Name
from assetallocation_arp.models import portfolio_construction as pc
from assetallocation_arp.models import arp_signals as arp
from assetallocation_arp.data_etl.dal.data_models.strategy import Times
from assetallocation_arp.data_etl.dal.data_models.asset import TimesAssetInput
from assetallocation_arp.data_etl.dal.data_frame_converter import DataFrameConverter
from assetallocation_arp.data_etl.dal.data_models.fund_strategy import FundStrategy, FundStrategyAssetAnalytic, FundStrategyAssetWeight
from assetallocation_arp.common_libraries.dal_enums.fund_strategy import Category, Signal, Performance


def format_data_and_calc(times_inputs, asset_inputs, all_data):
    # Remove the index below in the dashboard: they are not in the all_data col
    # "['RX1 R:00_0_R Comdty', 'CN1 R:00_0_R Comdty', 'G 1 R:00_0_R Comdty'] not in index"

    # format data and inputs
    asset_inputs_t = asset_inputs.set_index('asset').T
    all_data = all_data[all_data.index.values > np.datetime64(times_inputs['date_from'].item())]
    times_data = all_data[asset_inputs.signal_ticker]
    futures_data = all_data[asset_inputs.future_ticker].pct_change()
    times_data.columns = asset_inputs.asset
    futures_data.columns = asset_inputs.asset
    #
    costs = asset_inputs_t.loc['costs']
    leverage = asset_inputs_t.loc['s_leverage']
    leverage_type = times_inputs['leverage_type'].item()

    # calculate signals
    signals = arp.momentum(times_data, times_inputs, times_inputs['week_day'].item())
    # apply leverage
    leverage_data = pc.apply_leverage(futures_data, leverage_type, leverage)
    leverage_data[leverage.index[leverage.isnull()]] = np.nan
    index_df = futures_data.append(pd.DataFrame(index=futures_data.iloc[[-1]].index + BDay(2)), sort=True).index
    leverage_data = leverage_data.shift(periods=times_inputs['time_lag'].item(), freq='D', axis=0).reindex(index_df,
                                                                                                           method='pad')
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

    signals = arp.momentum(signal_assets, times)

    leverage_data = pc.apply_leverage(future_assets, times.leverage_type, asset_inputs['s_leverage'])
    leverage_data[asset_inputs['s_leverage'].index[asset_inputs['s_leverage'].isnull()]] = np.nan
    index_df = future_assets.append(pd.DataFrame(index=future_assets.iloc[[-1]].index + BDay(2)), sort=True).index
    leverage_data = leverage_data.shift(periods=times.time_lag_in_months, freq='D', axis=0).reindex(index_df,
                                                                                                    method='pad')

    # calculate leveraged positions and returns
    cost = pd.Series(asset_inputs['cost'], index=asset_inputs['signal_ticker'])
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


def create_times_asset_analytics(signals: pd.DataFrame, returns: pd.DataFrame,
                                 r: pd.DataFrame) -> List[FundStrategyAssetAnalytic]:
    """
    :param signals: columns named after tickers, index of dates
    :param returns: columns named after tickers, index of dates
    :param r: columns named after tickers, index of dates
    :return:
    """
    asset_analytics = []

    asset_analytics.extend(df_to_asset_analytics(signals, Category.signal, Signal.momentum))
    asset_analytics.extend(df_to_asset_analytics(returns, Category.performance, Performance["excess return"]))
    asset_analytics.extend(df_to_asset_analytics(r, Category.performance, Performance["excess return index"]))

    return asset_analytics


def df_to_asset_analytics(analytics: pd.DataFrame, category: Union[str, Category],
                          subcategory: Union[str, Performance, Signal]) -> List[FundStrategyAssetAnalytic]:
    """Transform DataFrame with index of business_date and columns of asset tickers to list of
    FundStrategyAssetAnalytics
    """
    return [FundStrategyAssetAnalytic(ticker, index, category, subcategory, float(val)) for ticker, data in
            analytics.items() for index, val in data.iteritems()]


def df_to_asset_weights(positioning: pd.DataFrame) -> List[FundStrategyAssetWeight]:
    """Transform DataFrame with index of business_date and columns of asset tickers to list of FundStrategyAssetWeights
    """
    return [FundStrategyAssetWeight(ticker, index, float(val)) for ticker, data in positioning.items() for index, val in
            data.iteritems()]
