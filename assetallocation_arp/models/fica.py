"""
Created on Thu Feb  13 17:39:00 2020
FICA
@author: WK68945 & AB12345
"""

import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline

from assetallocation_arp.common_libraries.dal_enums.fica_asset_input import Category
from assetallocation_arp.data_etl.dal.data_frame_converter import DataFrameConverter


def format_data(strategy: 'Fica'):
    """Select curve data for sovereign tickers if curve == sovereign else swap
    tickers
    :return: dataframe with historical yield curves per country
    """
    # selecting which yield curve to use
    curve_category = Category.sovereign if strategy.curve == Category.sovereign.name else Category.swap
    analytics = [
        (asset.ticker, analytic) for group in strategy.grouped_asset_inputs for asset in
        group.fica_asset_inputs for analytic in asset.asset_analytics if asset.input_category == curve_category
    ]

    curve = DataFrameConverter.asset_analytics_to_df(analytics)
    return curve.asfreq('BM')


def calculate_carry_roll_down(strategy: 'Fica', curve: pd.DataFrame):
    """
    creating dataframe with carry + roll down and return calculations
    :param Fica strategy: Fica object with strategy inputs
    :param pd.DataFrame curve: dataframe with historical yield curves per country
    :return: dataframe with historical carry and roll down and return calculations per country
    """
    # reading inputs
    tenor = strategy.tenor
    coupon = strategy.coupon
    countries = [group.asset_subcategory.name for group in strategy.grouped_asset_inputs]
    n = len(curve)
    m = len(countries)
    # creating cash flows (semi-annually until expiration) and corresponding cash flow dates
    nodes = np.arange(0.5, tenor + 0.5, 0.5)
    nodes_curve = np.arange(11)
    nodes_curve = np.append(nodes_curve, [15, 20, 30])
    cash_flows = [coupon * 100 / 2] * tenor * 2
    cash_flows[tenor * 2 - 1] = cash_flows[tenor * 2 - 1] + 100
    # calculating discount factors looping over countries, history and cash flow dates, using cubic spline
    # calculating present value, carry and return series
    df = pd.DataFrame(np.array([np.arange(tenor * 2)] * 2).T)
    pv = pd.DataFrame(np.array([np.arange(m)] * n).T)
    pv1m = pd.DataFrame(np.array([np.arange(m)] * n).T)
    carry_roll = pd.DataFrame(np.array([np.arange(m)] * n).T, columns=curve.index)
    country_returns = pd.DataFrame(np.array([np.arange(m)] * n).T, columns=curve.index)
    for i in range(m):
        for k in range(n):
            cs = CubicSpline(nodes_curve, curve.iloc[k, i * 14:i * 14 + 14])
            df.iloc[:, 0] = 1 / (1 + cs(nodes) / 100) ** nodes
            df.iloc[:, 1] = 1 / (1 + cs(nodes - 1 / 12) / 100) ** (nodes - 1 / 12)
            pv.iloc[i, k] = sum(cash_flows * df.iloc[:, 0])
            pv1m.iloc[i, k] = sum(cash_flows * df.iloc[:, 1])
            carry_roll.iloc[i, k] = (pv1m.iloc[i, k] / pv.iloc[i, k]) ** 12 * 100 - 100 - curve.iloc[k, i * 14 + 1]
            if k > 0:
                country_returns.iloc[i, k] = np.log((pv1m.iloc[i, k] / pv.iloc[i, k - 1])) * 100 \
                                           - curve.iloc[k - 1, i * 14 + 1] / 12
    # transposing and adding column names
    carry_roll = carry_roll.T
    carry_roll.columns = countries
    country_returns = country_returns.T
    country_returns.iloc[0, :] = np.NaN
    country_returns.columns = countries
    return carry_roll, country_returns


def calculate_signals_and_returns(strategy: 'Fica', carry_roll, country_returns):
    """"
    creating dataframe with country signals and contributions and overall model performances
    :param Fica strategy: Fica object with strategy inputs
    :param pd.DataFrame carry_roll: historical carry and roll down calculations per country
    :param pd.DataFrame country_returns: historical return calculations per country
    :return: dataframes with monthly model signals, cumulative country contributions and model returns
    """
    # reading inputs
    returns = pd.DataFrame()
    m = len(carry_roll.columns)
    n = len(carry_roll)
    # ranking the countries
    rank = carry_roll.T.rank()
    signals = rank.T
    # determining country weights
    for i in range(m):
        signals = signals.replace(i + 1, strategy.strategy_weights[m - i - 1])
    # calculating country performance contributions
    contribution = country_returns.sub(country_returns.mean(axis=1), axis=0) * signals.shift()
    cum_contribution = contribution.cumsum()
    contribution['Return'] = contribution.sum(axis=1)
    cum_contribution['Return'] = cum_contribution.sum(axis=1)
    # calculating returns, starting return index series with 100
    sub_signals = signals - signals.shift()
    returns['Costs'] = sub_signals.abs().sum(axis=1) * strategy.trading_cost / 100
    returns['Net_Return'] = cum_contribution['Return'] - returns['Costs'].cumsum()
    returns['Arithmetic'] = (1 + returns['Net_Return'] / 100) * 100
    returns['Geometric'] = 100
    for k in range(1, n):
        returns.iloc[k, 3] = (1 + (contribution.iloc[k, m] - returns.iloc[k, 0]) / 100) * returns.iloc[k - 1, 3]
    return signals, cum_contribution, returns


# TODO refactor for performance
def run_daily_attribution(strategy, signals):
    """
    performing the daily attributions and inputs for the charts
    :param Fica strategy: Fica object with strategy inputs
    :param pd.DataFrame signals: monthly model signals
    :return: dataframes with daily carry and roll down and return calculations
    """
    future_tickers, futures = [], []
    swap_cr_tickers, swap_crs = [], []
    for group in strategy.grouped_asset_inputs:
        for asset in group.fica_asset_inputs:
            if asset.input_category == Category.future and group.asset_subcategory.name in ('EUR', 'GBP', 'USD'):
                future_tickers.append(asset.ticker)
                for analytic in asset.asset_analytics:
                    futures.append((asset.ticker, analytic))
            elif asset.input_category == Category.swap_cr:
                swap_cr_tickers.append(asset.ticker)
                for analytic in asset.asset_analytics:
                    swap_crs.append((asset.ticker, analytic))

    futures = DataFrameConverter.asset_analytics_to_df(futures)[future_tickers]
    curve_ox = DataFrameConverter.asset_analytics_to_df(swap_crs)[swap_cr_tickers]

    # reading inputs and shortening data
    carry_daily = pd.DataFrame()
    return_daily = pd.DataFrame()
    countries = [group.asset_subcategory.name for group in strategy.grouped_asset_inputs]
    m = len(countries)
    n = len(curve_ox)
    # creating carry & return dataframe for three country proxy

    for i in range(m):
        carry_daily[countries[i]] = 10 * curve_ox.iloc[:, 3+i*4] - 9 * curve_ox.iloc[:, 2+i*4] - curve_ox.iloc[:, i*4]
        return_daily[countries[i]] = -7.5 * (curve_ox.iloc[:, 3+i*4] - curve_ox.iloc[:, 3+i*4].shift())
    # creating daily signals from monthly signals
    signal_daily = signals.resample('B').ffill()
    # creating FICA and G3 carry & return series
    carry_daily['fica_10y_carry'] = carry_daily.mul(signal_daily.shift()).sum(axis=1)
    carry_daily['fica_10y_carry_cum'] = carry_daily['fica_10y_carry'].cumsum() / 250
    carry_daily['G3_10y_carry'] = (carry_daily['EUR'] + carry_daily['GBP'] + carry_daily['USD']) / 3
    return_daily['fica_10y_spot'] = return_daily.mul(signal_daily.shift()).sum(axis=1)
    return_daily['fica_10y_spot_cum'] = return_daily['fica_10y_spot'].cumsum()
    return_daily['fica_10y_return'] = 100
    return_daily['G3_10y_return'] = 100
    for k in range(1, n):
        return_daily.iloc[k, m + 2] = return_daily.iloc[k - 1, m + 2] * \
                (1 + return_daily.iloc[k, m] / 100) * (1 + carry_daily.iloc[k, m] / 25000)
        return_daily.iloc[k, m + 3] = return_daily.iloc[k - 1, m + 3] * \
                futures.iloc[k, :].div(futures.iloc[k-1, :]).mean()
    return_daily['fica_10y_return%'] = return_daily['fica_10y_return'].pct_change()
    return_daily['G3_10y_return%'] = return_daily['G3_10y_return'].pct_change()
    return_daily['correlation'] = return_daily['fica_10y_return%'].rolling(64).corr(return_daily['G3_10y_return%'])
    return_daily['beta'] = return_daily['fica_10y_return%'].rolling(64).cov(return_daily['G3_10y_return%']) / \
                            return_daily['G3_10y_return%'].rolling(64).var()
    return carry_daily, return_daily