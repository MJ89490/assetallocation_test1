"""
Created on Fri Nov  15 17:27:51 2019
TIMES
@author: SN69248
"""
from typing import List, Tuple

import numpy as np
import pandas as pd
from pandas.tseries.offsets import BDay

from assetallocation_arp.common_libraries.dal_enums.strategy import Leverage
from assetallocation_arp.models import portfolio_construction as pc
from assetallocation_arp.models import arp_signals as arp
from assetallocation_arp.data_etl.dal.data_models.asset import TimesAssetInput
from assetallocation_arp.data_etl.dal.data_frame_converter import DataFrameConverter


def calculate_signals_returns_r_positioning(times: 'Times') -> \
        Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """return signals, returns, r, positioning with columns of asset subcategory"""
    asset_inputs, future_assets, signal_assets = get_asset_data_as_data_frames(times.asset_inputs)
    future_assets = future_assets.pct_change()

    signals = arp.momentum(signal_assets, times)

    future_leverage = asset_inputs[['future_ticker', 's_leverage']].set_index('future_ticker')['s_leverage']
    leverage_data = pc.apply_leverage(future_assets, times.leverage_type, future_leverage)
    leverage_data[asset_inputs['s_leverage'].index[asset_inputs['s_leverage'].isnull()]] = np.nan
    index_df = future_assets.append(pd.DataFrame(index=future_assets.iloc[[-1]].index + BDay(2)), sort=True).index
    leverage_data = leverage_data.shift(periods=times.time_lag_in_days, freq='D', axis=0).reindex(index_df,
                                                                                                  method='pad')

    # calculate leveraged positions and returns
    cost = asset_inputs[['cost', 'future_ticker']].set_index('future_ticker')['cost']

    if times.leverage_type == Leverage.s:
        returns, r, positioning = pc.return_ts(signals, future_assets, leverage_data, cost, False)
    elif times.leverage_type == Leverage.n.name:
        (returns, r, positioning) = pc.return_ts(signals, future_assets, leverage_data, cost, True)
    else:
        returns, r, positioning = pc.return_ts(signals, future_assets, leverage_data, cost, True)
        returns, r, positioning = pc.rescale(returns, positioning, 0.01)

    # Replace inf values with nan values
    # Replacing infinite with nan
    positioning.replace([np.inf, -np.inf], np.nan, inplace=True)

    return signals, returns, r, positioning


def get_asset_data_as_data_frames(
        asset_inputs: List[TimesAssetInput]
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Return asset inputs, future assets and signal assets
    where future and signal assets have columns of asset_inputs[asset_subcategory]
    """
    signal_assets, future_assets = [], []

    for i in asset_inputs:
        signal_assets.append((i.future_asset.ticker, i.signal_asset))
        future_assets.append((i.future_asset.ticker, i.future_asset))

    signal_assets = DataFrameConverter.assets_to_df(signal_assets)
    future_assets = DataFrameConverter.assets_to_df(future_assets)
    asset_inputs = DataFrameConverter.times_asset_inputs_to_df(asset_inputs)

    return asset_inputs, future_assets, signal_assets


