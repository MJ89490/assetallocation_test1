from datetime import date

import mock
import pandas as pd
from numpy import nan

from assetallocation_arp.data_etl.dal.data_frame_converter import DataFrameConverter, FundStrategyAssetWeight, \
    FundStrategyAssetAnalytic


def mock_fund_strategy_asset_weights(asset_ticker: str, business_date: date, strategy_weight: float, implemented_weight: float):
    MockFundStrategyAssetWeight = mock.create_autospec(FundStrategyAssetWeight)
    mock_fsaw = MockFundStrategyAssetWeight(asset_ticker, business_date, strategy_weight)
    mock_fsaw.business_date = business_date
    mock_fsaw.asset_ticker = asset_ticker
    mock_fsaw.strategy_weight = strategy_weight
    mock_fsaw.implemented_weight = implemented_weight
    return mock_fsaw


def mock_fund_strategy_asset_analytic(asset_ticker: str, business_date: date, category: str, subcategory: str, value: float):
    MockFundStrategyAssetAnalytic = mock.create_autospec(FundStrategyAssetAnalytic)
    mock_fsaa = MockFundStrategyAssetAnalytic(asset_ticker, business_date, category, subcategory, value)
    mock_fsaa.asset_ticker = asset_ticker
    mock_fsaa.business_date = business_date
    mock_fsaa.category = category
    mock_fsaa.subcategory = subcategory
    mock_fsaa.value = value
    return mock_fsaa


def test_fund_strategy_asset_analytics_to_df_returns_expected():
    mock_fsaa1 = mock_fund_strategy_asset_analytic('a', date(2020, 1, 2), 'b', 'c', float(1))
    mock_fsaa2 = mock_fund_strategy_asset_analytic('d', date(2020, 1, 3), 'e', 'f', float(2))

    expected = pd.DataFrame([[float(1), nan], [nan, float(2)]],
                            columns=['a', 'd'],
                            index=pd.MultiIndex(levels=[
                                pd.DatetimeIndex(['2020-01-02', '2020-01-03'], dtype='datetime64[ns]'), ['c', 'f']],
           codes=[[0, 1], [0, 1]],
           names=['business_date', 'subcategory']))

    returns = DataFrameConverter.fund_strategy_asset_analytics_to_df([], [mock_fsaa1, mock_fsaa2])

    pd.testing.assert_frame_equal(expected, returns, check_names=False)


def test_fund_strategy_asset_weights_to_df_returns_expected_value():
    mock_fsaw1 = mock_fund_strategy_asset_weights('a', date(2020, 1, 2), float(1), float(2))
    mock_fsaw2 = mock_fund_strategy_asset_weights('c', date(2020, 1, 3), float(4), float(3))

    expected = pd.DataFrame([[float(1), nan], [nan, float(4)]], columns=['a', 'c'], index=[date(2020, 1, 2), date(2020, 1, 3)])

    returns = DataFrameConverter.fund_strategy_asset_weights_to_df([], [mock_fsaw1, mock_fsaw2])

    pd.testing.assert_frame_equal(expected, returns, check_names=False)
