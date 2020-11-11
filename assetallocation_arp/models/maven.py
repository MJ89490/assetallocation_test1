"""
Created on Tue May  26 15:58:00 2020
FICA
@author: WK68945
"""

import numpy as np
import pandas as pd

from assetallocation_arp.models import portfolio_construction as pc
from assetallocation_arp.data_etl.dal.data_models.strategy import Maven
from assetallocation_arp.common_libraries.dal_enums.strategy import Frequency
from assetallocation_arp.data_etl.dal.data_frame_converter import DataFrameConverter


def format_data(strategy: Maven) -> pd.DataFrame:
    """creating dataframe with asset return index series
    :param Maven strategy: parameter choices and asset data for the model
    :return: dataframe with formatted asset return series
    """
    # choosing between excess and total returns, adjusting the credit excess return series
    if strategy.er_tr == 'excess':
        bbg_ticker = 'bbg_er_ticker'
        analytics = [(ai.bbg_er_asset.ticker, analytic) for ai in strategy.asset_inputs for analytic in
                  ai.bbg_er_asset.asset_analytics]
        analytics = DataFrameConverter.asset_analytics_to_df(analytics)
        excess_cols = [ai.bbg_er_asset.ticker for ai in strategy.asset_inputs if ai.true_excess]
        analytics.loc[:, excess_cols] = 1 + analytics.loc[:, excess_cols] / 100

    else:
        bbg_ticker = 'bbg_tr_ticker'
        analytics = [(ai.bbg_tr_asset.ticker, analytic) for ai in strategy.asset_inputs for analytic in
                     ai.bbg_tr_asset.asset_analytics]
        analytics = DataFrameConverter.asset_analytics_to_df(analytics)

    # choosing between weekly or monthly data, splitting up assets and cash
    cash_cols, asset_cols = [], []
    for ai in strategy.asset_inputs:
        (cash_cols if ai.asset_class == 'CASH' else asset_cols).append(getattr(ai, bbg_ticker))

    # calculate average cash rate over the period
    if strategy.frequency == Frequency.monthly:
        assets = analytics.loc[:, asset_cols].asfreq('BM')
        cash = analytics.loc[:, cash_cols].resample('BM', label='right', closed='right').mean()
    else:
        assets = analytics.loc[:, asset_cols].asfreq('W-' + strategy.day_of_week.name)
        cash = analytics.loc[:, cash_cols].resample(
            'W-' + strategy.day_of_week.name, label='right', closed='right'
        ).mean()

    # removing last data point as the resample with label='right' creates one beyond the chosen data period
    cash = cash.loc[analytics.index[0]:analytics.index[-1]].round(4)
    # transforming cash rates into cash index returns with cash ticker headers
    days = [np.array((cash.index - cash.index.shift(-1)).days)] * len(cash_cols)
    days = pd.DataFrame(data=np.transpose(days), columns=cash.columns, index=cash.index)
    cash = (1 + (days * cash) / 36500).cumprod()
    # merging both dataframes
    asset_returns = pd.merge(assets, cash, right_index=True, left_index=True)
    return asset_returns


def calculate_excess_returns(strategy: Maven, asset_returns: pd.DataFrame):
    """Creating dataframe with maven's excess return index series
    :param Maven strategy: parameter choices and asset data for the model
    :param pd.DataFrame asset_returns: formatted asset return series
    :return: pd.DataFrame with formatted return series for maven assets
    """
    # selecting maven assets and corresponding tickers
    bbg = 'bbg_er_ticker' if strategy.er_tr == 'excess' else 'bbg_tr_ticker'
    bbg_tickers = []
    bbg_ticker_subcategory = {}
    asset_weights = {}
    for ai in strategy.asset_inputs:
        if ai.asset_weight != 0:
            bbg_tickers.append(getattr(ai, bbg))
            bbg_ticker_subcategory[getattr(ai, bbg)] = ai.asset_subcategory
            asset_weights[getattr(ai, bbg)] = ai.asset_weight

    # creating asset excess returns
    assets = asset_returns[bbg_tickers]
    cash = pd.DataFrame(1, index=assets.index, columns=bbg_tickers)
    if strategy.er_tr != 'excess':
        excess_cols = [(getattr(ai, bbg), ai.cash_ticker) for ai in strategy.asset_inputs if ai.true_excess and getattr(ai, bbg) in bbg_tickers]
        cash.loc[:, [i[0] for i in excess_cols]] = asset_returns[[i[1] for i in excess_cols]].to_numpy()

    # rename asset columns after subcategory
    asset_excess = (assets / assets.shift()) / (cash / cash.shift())
    asset_unique = asset_excess * asset_weights
    asset_unique.rename(columns=bbg_ticker_subcategory, inplace=True)
    asset_unique = asset_unique.groupby(asset_unique.columns, axis=1).sum()

    # replacing 0 with start index value of 100
    asset_unique.iloc[0, :] = 100
    maven_returns = asset_unique.cumprod()
    return maven_returns


def calculate_signals(strategy: Maven, maven_returns):
    """creating DataFrames with value and momentum scores, and the top/bottom countries on the combination score
    :param Maven strategy: parameter choices and asset data for the model
    :param pd.DataFrame maven_returns: formatted return series for maven assets
    :return: DataFrames with momentum and value scores, volatility matrix, and long and short signals
    """
    # transforming to returns and returns^2
    maven_prc = maven_returns.pct_change()
    maven_sqr = maven_returns.pct_change() ** 2
    # getting inputs for rolling volatility and momentum score calculations
    if strategy.frequency == Frequency.monthly:
        n = 12      # 12months
        a = 12      # 12 sets of 1 month
    else:
        n = 52      # 52 weeks
        a = 13      # 13 sets of 4 weeks
    m = int(strategy.val_period_months / 12 * n)      # look-back period for value
    base = int(strategy.val_period_base / 12 * n)     # period around look-back point
    # calculating rolling volatility
    vol1 = 0
    vol2 = 0
    for i in range(0, len(strategy.volatility_weights)):
        vol1 = vol1 + strategy.volatility_weights[i] * maven_sqr.shift(i * n).rolling(n).mean()
        vol2 = vol2 + strategy.volatility_weights[i] * maven_prc.shift(i * n).rolling(n).mean()
    volatility = n ** 0.5 * (vol1 / sum(strategy.volatility_weights) - (vol2 / sum(strategy.volatility_weights)) ** 2) ** 0.5
    # calculating momentum signal
    mom = 1
    for i in range(0, len(strategy.momentum_weights)):
        mom = mom * (maven_returns.shift(int(i * n / a)) / maven_returns.shift(int((i + 1) * n / a))) ** strategy.momentum_weights[i]
    momentum = (mom ** (a / sum(strategy.momentum_weights)) - 1) / volatility
    # calculating the value scores
    value = ((maven_returns / maven_returns.shift(int(m - base / 2)).rolling(base + 1).mean()) ** (n / m) - 1) / volatility
    # shorting the dataframes
    start_date = value.first_valid_index()
    value = value[start_date:]
    momentum = momentum[start_date:]
    n = len(value)
    value_last = value.iloc[n - 1, :]
    momentum_last = momentum.iloc[n - 1, :].rename('momentum')
    # sorting last observation on momentum and applying value filter for charting purposes
    filter1 = ((value_last > strategy.long_cutoff) * momentum_last).rename('too expensive')
    filter2 = ((value_last < strategy.short_cutoff) * momentum_last).rename('too cheap')
    momentum_last = pd.concat([momentum_last, filter1, filter2], axis=1)
    momentum_last = momentum_last.sort_values(by=['momentum'])
    momentum_last['momentum'] = momentum_last['momentum'] - momentum_last['too expensive'] - momentum_last['too cheap']
    # determine signals based on a combination of momentum and value scores: value filter results in -999 scores
    drop_value = (value > strategy.long_cutoff) * -999
    keep_momentum = (value <= strategy.long_cutoff) * momentum
    long_signals = drop_value + keep_momentum
    drop_value = (value < strategy.short_cutoff) * -999
    keep_momentum = (value >= strategy.short_cutoff) * -momentum
    short_signals = drop_value + keep_momentum
    # ranking signals
    long_signals_rank = long_signals.rank(axis=1, method='first', ascending=False)
    short_signals_rank = short_signals.rank(axis=1, method='first', ascending=False)

    # filtering and getting names of top assets
    long_signals_name = pd.DataFrame(np.ones((n, strategy.asset_count)), index=value.index)
    short_signals_name = pd.DataFrame(np.ones((n, strategy.asset_count)), index=value.index)
    for i in range(0, strategy.asset_count):
        long_signals_name.iloc[:, i] = long_signals_rank.apply(lambda x: x[x == i + 1].idxmin(), axis=1)
        short_signals_name.iloc[:, i] = short_signals_rank.apply(lambda x: x[x == i + 1].idxmin(), axis=1)
    return momentum, value, long_signals, short_signals, volatility


def run_performance_stats(strategy: Maven, maven_returns, volatility, long_signals, short_signals):
    """
    creating dataframes with maven return series, and benchmarks, asset class exposures and contributions
    :param Maven strategy: parameter choices and asset data for the model
    :param pd.DataFrame maven_returns: formatted return series for maven assets
    :param pd.DataFrame volatility: volatility matrix
    :param pd.DataFrame long_signals: asset long signals
    :param pd.DataFrame short_signals: asset short signals
    :return: dataframes with maven return series, asset class exposures and contributions
    """
    # reading inputs and aligning dataframes
    if strategy.frequency == Frequency.monthly:
        w_m = 1
    else:
        w_m = 4
    m = len(maven_returns.columns)  # number of assets
    n = len(long_signals)           # number of observations
    number_signals = strategy.asset_count
    maven_returns = maven_returns.tail(n)
    volatility = volatility.tail(n)
    # determining equal weights and equal volatility weights
    equal_notional = pd.DataFrame((1 / m) * np.ones((n, m)), index=long_signals.index, columns=long_signals.columns)
    equal_risk = ((1 / volatility).T / (1 / volatility).sum(axis=1)).T
    # determining benchmark returns, fully invested across all assets
    returns_en = maven_returns.pct_change() * equal_notional.shift().rolling(w_m).mean()
    returns_er = maven_returns.pct_change() * equal_risk.shift().rolling(w_m).mean()
    returns_en.iloc[0, :] = 0
    returns_er.iloc[0, :] = 0
    returns_en_cum = (1 + returns_en.sum(axis=1)).cumprod() * 100
    returns_er_cum = (1 + returns_er.sum(axis=1)).cumprod() * 100
    returns_maven = pd.DataFrame({'equal notional': returns_en_cum, 'equal volatility': returns_er_cum})
    # calculating maven long and short weights
    long_exposures = long_signals.rank(axis=1, method='first', ascending=False) <= number_signals
    short_exposures = short_signals.rank(axis=1, method='first', ascending=False) <= number_signals
    vol_long = long_exposures * (1 / volatility)
    vol_short = short_exposures * (1 / volatility)
    # capping asset weight to 50%
    equal_risk_long = pc.cap_and_redistribute((vol_long.T / vol_long.sum(axis=1)).T, 0.5).rolling(w_m).mean()
    equal_risk_short = pc.cap_and_redistribute((vol_short.T / vol_short.sum(axis=1)).T, 0.5).rolling(w_m).mean()
    # calculating turnover

    assets, costs, asset_class = [], [], []
    for i in strategy.asset_inputs:
        if i.asset_subcategory in equal_risk.columns and i.asset_subcategory not in assets:
            costs.append(i.transaction_cost)
            assets.append(i.asset_subcategory)
            asset_class.append(i.asset_class)

    sub_equal_risk_long = equal_risk_long - equal_risk_long.shift()
    sub_equal_risk_short = equal_risk_short - equal_risk_short.shift()
    turnover_cost_long = sub_equal_risk_long.abs().mul(costs, axis=1).sum(axis=1) / 10000
    turnover_cost_short = sub_equal_risk_short.abs().mul(costs, axis=1).sum(axis=1) / 10000
    # calculating maven long and short returns, gross and net
    returns_maven_long = maven_returns.pct_change() * equal_risk_long.shift()
    returns_maven_short = maven_returns.pct_change() * -equal_risk_short.shift()
    returns_maven_long.iloc[0, :] = 0
    returns_maven_short.iloc[0, :] = 0
    returns_maven['maven long gross'] = (1 + returns_maven_long.sum(axis=1)).cumprod() * 100
    returns_maven['maven short gross'] = (1 + returns_maven_short.sum(axis=1)).cumprod() * 100
    returns_maven['maven long net'] = (1 + returns_maven_long.sum(axis=1) - turnover_cost_long).cumprod() * 100
    returns_maven['maven short net'] = (1 + returns_maven_short.sum(axis=1) - turnover_cost_short).cumprod() * 100
    # determining asset class contributions
    asset_contribution_long = pd.DataFrame(data=returns_maven_long.T)
    asset_contribution_long.index = asset_class
    asset_contribution_short = pd.DataFrame(data=returns_maven_short.T)
    asset_contribution_short.index = asset_class
    asset_contribution_long = asset_contribution_long.groupby(asset_contribution_long.index).sum().T
    asset_contribution_short = asset_contribution_short.groupby(asset_contribution_short.index).sum().T

    return returns_maven, asset_contribution_long, asset_contribution_short


def contributions_to_weights(contribution_short: pd.DataFrame, contribution_long: pd.DataFrame) -> pd.DataFrame:
    """
    :param contribution_short: values of assets, index of dates
    :param contribution_long: values of assets, index of dates
    :return: DataFrame with columns of assets and index of dates, values of contributions
    """
    def count_per_row(df):
        return pd.concat([df.T[i].value_counts() for i in df.index], axis=1, sort=False).T

    long = count_per_row(contribution_long) * 1 / contribution_long.shape[1]
    short = count_per_row(contribution_short) * -1 / contribution_short.shape[1]

    return short.add(long, fill_value=0).fillna(0)
