from datetime import date

import mock
import pandas as pd
from numpy import nan

from assetallocation_arp.data_etl.dal.data_frame_converter import DataFrameConverter, FundStrategyAssetWeight, \
    FundStrategyAssetAnalytic, Asset


def mock_asset(ticker: str, subcategory: str):
    MockAsset = mock.create_autospec(Asset)
    mock_a = MockAsset(ticker)
    mock_a.ticker = ticker
    mock_a.subcategory = subcategory

    return mock_a


def mock_fund_strategy_asset_weights(asset_subcategory: str, business_date: date, strategy_weight: float,
                                     implemented_weight: float, frequency: str):
    MockFundStrategyAssetWeight = mock.create_autospec(FundStrategyAssetWeight)
    mock_fsaw = MockFundStrategyAssetWeight(asset_subcategory, business_date, strategy_weight, frequency)
    mock_fsaw.business_date = business_date
    mock_fsaw.frequency = frequency
    mock_fsaw.asset_subcategory = asset_subcategory
    mock_fsaw.strategy_weight = strategy_weight
    mock_fsaw.implemented_weight = implemented_weight
    return mock_fsaw


def mock_fund_strategy_asset_analytic(asset_subcategory: str, business_date: date, category: str, subcategory: str,
                                      value: float, frequency: str):
    MockFundStrategyAssetAnalytic = mock.create_autospec(FundStrategyAssetAnalytic)
    mock_fsaa = MockFundStrategyAssetAnalytic(asset_subcategory, business_date, category, subcategory, value, frequency)
    mock_fsaa.asset_subcategory = asset_subcategory
    mock_fsaa.business_date = business_date
    mock_fsaa.freqency = frequency
    mock_fsaa.category = category
    mock_fsaa.subcategory = subcategory
    mock_fsaa.value = value
    return mock_fsaa


def test_fund_strategy_asset_analytics_to_df_returns_expected():
    mock_fsaa1 = mock_fund_strategy_asset_analytic('a', date(2020, 1, 2), 'b', 'c', float(1), 'g')
    mock_fsaa2 = mock_fund_strategy_asset_analytic('d', date(2020, 1, 3), 'e', 'f', float(2), 'h')

    expected = pd.DataFrame(
        [[float(1), nan], [nan, float(2)]],
        columns=['a', 'd'],
        index=pd.MultiIndex(
            levels=[pd.DatetimeIndex(['2020-01-02', '2020-01-03'], dtype='datetime64[ns]'), ['c', 'f']],
            codes=[[0, 1], [0, 1]], names=['business_date', 'analytic_subcategory']
        )
    )

    returns = DataFrameConverter.fund_strategy_asset_analytics_to_df([mock_fsaa1, mock_fsaa2])

    pd.testing.assert_frame_equal(expected, returns, check_names=False)


def test_fund_strategy_asset_weights_to_df_returns_expected_value():
    mock_fsaw1 = mock_fund_strategy_asset_weights('a', date(2020, 1, 2), float(1), float(2), 'g')
    mock_fsaw2 = mock_fund_strategy_asset_weights('c', date(2020, 1, 3), float(4), float(3), 'h')

    expected = pd.DataFrame([[float(1), nan], [nan, float(4)]],
                            columns=['a', 'c'],
                            index=pd.DatetimeIndex(['2020-01-02', '2020-01-03'], dtype='datetime64[ns]', name='business_date'))

    returns = DataFrameConverter.fund_strategy_asset_weights_to_df([mock_fsaw1, mock_fsaw2])

    pd.testing.assert_frame_equal(expected, returns, check_names=False)
