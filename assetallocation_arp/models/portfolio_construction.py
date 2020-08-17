"""
Created on Fri Nov  15 17:27:51 2019
PORTFOLIO CONSTRUCTION
@author: SN69248
"""
import math
import pandas as pd

from pandas.tseries.offsets import BDay

from common_libraries.dal_enums.strategy import Leverage


def apply_leverage(futures_data, leverage_type, leverage):
    # leverage_type: Equal(e) / Normative(n) / Volatility(v) / Standalone(s)
    if leverage_type == Leverage.e.name or leverage_type == Leverage.s.name:
        leverage_data = 0 * futures_data + 1
        leverage_data[leverage.index[leverage > 0]] = 1
    elif leverage_type == Leverage.n.name:
        leverage_data = 0 * futures_data + leverage
    elif leverage_type == Leverage.v.name:
        leverage_data = 1 / futures_data.ewm(alpha=1/150, min_periods=10).std()
    else:
        raise Exception('Invalid entry')
    return leverage_data


def rescale(ret, r, positioning, column, vol):
    # Calibrate series to a target volatility, uses full historic time series
    m_return = r[column].diff(periods=21)
    return_scaled = ret/(m_return.std()*math.sqrt(12))*vol
    positioning_scaled = positioning/(m_return.std()*math.sqrt(12))*vol
    r_scaled = return_scaled.cumsum()
    return return_scaled, r_scaled, positioning_scaled


def return_ts(sig, future, leverage, costs, cummul):
    # Implement trading signal in a time-series context and as standalone for every series
    returns = pd.DataFrame()
    r = pd.DataFrame()
    sig = sig.reindex(future.append(pd.DataFrame(index=future.iloc[[-1]].index + BDay(2)), sort=True).index, method='pad') 
    if cummul == 1:
        positioning = sig.divide(future.multiply(leverage).count(axis=1), axis=0)
        positioning.iloc[-1:] = sig.iloc[-1:]/sig.iloc[-1].multiply(leverage.iloc[-1]).count()
    else:
        positioning = sig
    for column in sig:
        positioning[column] = leverage[column]*positioning[column]
        returns[column] = future[column]*positioning[column]
        # Trading costs
        returns[column].iloc[1:] = returns[column].iloc[1:]-costs[column]*pd.DataFrame.abs(positioning[column].diff(periods=1))
        r[column] = returns[column].cumsum()
    returns['Total'] = returns.sum(axis=1)
    r['Total'] = returns['Total'].cumsum()
    return returns, r, positioning


