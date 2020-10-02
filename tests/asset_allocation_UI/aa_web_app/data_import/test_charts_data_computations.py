import pandas as pd
from numpy import nan
import mock

from assetallocation_UI.aa_web_app.data_import import main_import_data as main_in
from assetallocation_arp.common_libraries.dal_enums.fund_strategy import Signal, Performance


@mock.patch("assetallocation_UI.aa_web_app.data_import.main_import_data.TimesProcCaller")
def test_main_data_throws_no_errors_valid_inputs(mock_times_proc_caller):
    weights_df = pd.DataFrame([[float(1), nan], [nan, float(4)]],
                              columns=pd.MultiIndex(levels=[['a', 'c'], ['US_Equities', 'US_10_y_Bonds']],
                                                    codes=[[0, 1], [1, 0]], names=['ticker', 'asset_subcategory']),
                              index=pd.DatetimeIndex(['2020-01-02', '2020-01-09'], dtype='datetime64[ns]',
                                                     name='business_date'))

    analytic_df = pd.DataFrame(
        [[float(1), nan], [nan, float(2)], [float(3), nan], [nan, float(4)], [float(5), nan], [nan, float(6)]],
        columns=pd.MultiIndex(levels=[['a', 'd'], ['US_Equities', 'US_10_y_Bonds']], codes=[[0, 1], [1, 0]],
                              names=['ticker', 'asset_subcategory']), index=pd.MultiIndex(
            levels=[pd.DatetimeIndex(['2019-12-31', '2020-01-02', '2020-01-09'], dtype='datetime64[ns]'),
                    [Signal.momentum, Performance['excess return']]], codes=[[0, 0, 1, 1, 2, 2], [0, 1, 0, 1, 0, 1]],
            names=['business_date', 'analytic_subcategory']))

    with mock.patch.object(main_in.DataFrameConverter, 'fund_strategy_asset_weights_to_df') as mock_weights:
        mock_weights.return_value = weights_df
        with mock.patch.object(main_in.DataFrameConverter, 'fund_strategy_asset_analytics_to_df') as mock_analytics:
            mock_analytics.return_value = analytic_df

            main_in.main_data('f1', 1)
