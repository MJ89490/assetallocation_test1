"""
Created on 12/11/2019
Author: AJ89720
email: Anais.Jeremie@lgim.com
"""

import pytest
import os
import pandas as pd

from assetallocation_arp.models.times import calculate_signals_returns_r_positioning, format_data_and_calc
from assetallocation_arp.common_libraries.dal_enums.strategy import Leverage, DayOfWeek
from assetallocation_arp.data_etl.dal.data_models.strategy import Times, TimesAssetInput
from assetallocation_arp.data_etl.dal.data_models.asset import Asset
from assetallocation_arp.data_etl.dal.data_models.asset_analytic import AssetAnalytic


CURRENT_PATH = os.path.dirname(__file__)

"""
time_lag: 2	
volatility_window: 90	
sig1_short: 15	
sig1_long: 30	
sig2_short: 30	
sig2_long: 60	
sig3_short: 60	
sig3_long: 120	
frequency: weekly	
week_day: TUE	
date_to: 15/09/2020
date_from: 01/01/2000
"""


@pytest.mark.parametrize("leverage_type, signals_output, returns_output, positioning_output, r_output",
                         [(Leverage.v.name, "signals_leverage_v.csv", "returns_leverage_v.csv", "positioning_leverage_v.csv", "r_leverage_v.csv"),
                          (Leverage.e.name, "signals_leverage_e.csv", "returns_leverage_e.csv", "positioning_leverage_e.csv", "r_leverage_e.csv"),
                          (Leverage.n.name, "signals_leverage_n.csv", "returns_leverage_n.csv", "positioning_leverage_n.csv", "r_leverage_n.csv"),
                          (Leverage.s.name, "signals_leverage_s.csv", "returns_leverage_s.csv", "positioning_leverage_s.csv", "r_leverage_s.csv")])
def test_format_data_and_calc(leverage_type, signals_output, returns_output, positioning_output, r_output):
    """
    Function which tests the format_data_and_calc function in order to know if it returns th correct results
    (e.g signals, r, returns, positioning)
    :param leverage_type: types of leverage available: Equal(e) / Normative(n) / Volatility(v) / Standalone(s)
    :param signals_path: name of the file signals for the signals path
    :param returns_path: name of the file returns for the returns path
    :param r_path: name of the file r for the r path
    :param positioning_path: name of the file positioning for the positioning path
    :return: assertion error if the two compared dataframes are not equal
    """

    times_inputs_data = f'strategy_inputs_leverage_{leverage_type}.csv'
    times_inputs = pd.read_csv(os.path.abspath(os.path.join(CURRENT_PATH, "resources", "times", "inputs_leverages_origin",
                                                            times_inputs_data)), index_col=0)

    asset_inputs_data = pd.read_csv(os.path.abspath(os.path.join(CURRENT_PATH, "resources", "times", "inputs_leverages_origin",
                                                                 "asset_inputs.csv")), index_col=0)

    all_data = pd.read_csv(os.path.abspath(os.path.join(CURRENT_PATH, "resources", "times", "inputs_leverages_origin",
                                                        "all_data.csv")), index_col=0)

    index_all_data = [pd.Timestamp(date) for date in all_data.index.values]

    all_data = all_data.reindex(index_all_data)# reset the dates of the index to Timestamp

    signals_origin, returns_origin, r_origin, positioning_origin = format_data_and_calc(times_inputs=times_inputs, asset_inputs=asset_inputs_data, all_data=all_data)

    signals = pd.read_csv(os.path.abspath(os.path.join(CURRENT_PATH, "resources", "times", "outputs_leverages_to_test", signals_output)), index_col=0)
    returns = pd.read_csv(os.path.abspath(os.path.join(CURRENT_PATH, "resources", "times", "outputs_leverages_to_test", returns_output)), index_col=0)
    positioning = pd.read_csv(os.path.abspath(os.path.join(CURRENT_PATH, "resources", "times", "outputs_leverages_to_test", positioning_output)), index_col=0)
    r = pd.read_csv(os.path.abspath(os.path.join(CURRENT_PATH, "resources", "times", "outputs_leverages_to_test", r_output)), index_col=0)

    pd.testing.assert_frame_equal(signals_origin.reset_index(drop=True),
                                  signals.reset_index(drop=True), check_column_type=False)
    pd.testing.assert_frame_equal(returns_origin.reset_index(drop=True),
                                  returns.reset_index(drop=True), check_column_type=False)
    pd.testing.assert_frame_equal(positioning_origin.reset_index(drop=True),
                                  positioning.reset_index(drop=True), check_column_type=False)
    pd.testing.assert_frame_equal(r_origin.reset_index(drop=True),
                                  r.reset_index(drop=True), check_column_type=False)


"""
Module test_times.py: tests the Times model (times.py) in order to know if it returns the correct following outputs:
    - signals
    - returns
    - r
    - positioning
"""


@pytest.mark.parametrize("leverage_type, signals_output, returns_output, positioning_output, r_output",
                         [(Leverage.v.name, "signals_leverage_v.csv", "returns_leverage_v.csv", "positioning_leverage_v.csv", "r_leverage_v.csv"),
                          (Leverage.e.name, "signals_leverage_e.csv", "returns_leverage_e.csv", "positioning_leverage_e.csv", "r_leverage_e.csv"),
                          (Leverage.n.name, "signals_leverage_n.csv", "returns_leverage_n.csv", "positioning_leverage_n.csv", "r_leverage_n.csv"),
                          (Leverage.s.name, "signals_leverage_s.csv", "returns_leverage_s.csv", "positioning_leverage_s.csv", "r_leverage_s.csv")]
                         )
def test_calculate_signals_returns_r_positioning(leverage_type, signals_output, returns_output, positioning_output, r_output):
    """
    Function which tests the format_data_and_calc function in order to know if it returns th correct results
    (e.g signals, r, returns, positioning)
    :param leverage_type: types of leverage available: Equal(e) / Normative(n) / Volatility(v) / Standalone(s)
    :param signals_path: name of the file signals for the signals path
    :param returns_path: name of the file returns for the returns path
    :param r_path: name of the file r for the r path
    :param positioning_path: name of the file positioning for the positioning path
    :return: assertion error if the two compared dataframes are not equal
    """
    t = setup_times(leverage_type)

    signals_origin, returns_origin, r_origin, positioning_origin = calculate_signals_returns_r_positioning(t)

    positioning, r, returns, signals = get_expected_outputs(positioning_output, r_output, returns_output, signals_output)

    pd.testing.assert_frame_equal(signals_origin.reset_index(drop=True),
                                  signals.reset_index(drop=True), check_column_type=False, check_like=True)
    pd.testing.assert_frame_equal(positioning_origin.reset_index(drop=True),
                                  positioning.reset_index(drop=True), check_column_type=False, check_like=True)
    pd.testing.assert_frame_equal(r_origin.reset_index(drop=True),
                                  r.reset_index(drop=True), check_column_type=False, check_like=True)
    pd.testing.assert_frame_equal(returns_origin.reset_index(drop=True),
                                  returns.reset_index(drop=True), check_column_type=False, check_like=True)


def get_expected_outputs(positioning_output, r_output, returns_output, signals_output):
    signals = pd.read_csv(
        os.path.abspath(os.path.join(CURRENT_PATH, "resources", "times", "outputs_leverages_to_test", signals_output)),
        index_col=0)
    returns = pd.read_csv(
        os.path.abspath(os.path.join(CURRENT_PATH, "resources", "times", "outputs_leverages_to_test", returns_output)),
        index_col=0)
    positioning = pd.read_csv(os.path.abspath(
        os.path.join(CURRENT_PATH, "resources", "times", "outputs_leverages_to_test", positioning_output)), index_col=0)
    r = pd.read_csv(
        os.path.abspath(os.path.join(CURRENT_PATH, "resources", "times", "outputs_leverages_to_test", r_output)),
        index_col=0)

    asset_inputs_data = pd.read_csv(
        os.path.abspath(os.path.join(CURRENT_PATH, "resources", "times", "inputs_leverages_origin", "asset_inputs.csv")),
        index_col=0)

    cat_ticker = dict(zip(asset_inputs_data['asset'], asset_inputs_data['signal_ticker']))

    signals.columns = [cat_ticker[i] for i in signals.columns]
    returns.columns = [cat_ticker.get(i, i) for i in returns.columns]
    positioning.columns = [cat_ticker.get(i, i) for i in positioning.columns]
    r.columns = [cat_ticker.get(i, i) for i in r.columns]

    return positioning, r, returns, signals


def setup_times(leverage_type):
    times_inputs_data = f'strategy_inputs_leverage_{leverage_type}.csv'
    times_inputs = pd.read_csv(
        os.path.abspath(os.path.join(CURRENT_PATH, "resources", "times", "inputs_leverages_origin", times_inputs_data)),
        index_col=0)
    asset_inputs_data = pd.read_csv(
        os.path.abspath(os.path.join(CURRENT_PATH, "resources", "times", "inputs_leverages_origin", "asset_inputs.csv")),
        index_col=0)
    all_data = pd.read_csv(
        os.path.abspath(os.path.join(CURRENT_PATH, "resources", "times", "inputs_leverages_origin", "all_data.csv")),
        index_col=0)
    index_all_data = [pd.Timestamp(date) for date in all_data.index.values]
    all_data = all_data.reindex(index_all_data)  # reset the dates of the index to Timestamp
    t = Times(DayOfWeek[times_inputs['week_day'].iat[0]], times_inputs['frequency'].iat[0],
              times_inputs['leverage_type'].iat[0],
              [times_inputs['sig1_long'].iat[0], times_inputs['sig2_long'].iat[0], times_inputs['sig3_long'].iat[0]],
              [times_inputs['sig1_short'].iat[0], times_inputs['sig2_short'].iat[0], times_inputs['sig3_short'].iat[0]],
              times_inputs['time_lag'].iat[0], times_inputs['volatility_window'].iat[0])
    t_asset_inputs = []
    for i in asset_inputs_data.itertuples():
        ta = TimesAssetInput(i.s_leverage, i.signal_ticker, i.future_ticker, i.costs)

        for ticker, data in all_data.items():
            if ticker in (ta.signal_ticker, ta.future_ticker):
                a = Asset(ticker, ticker)
                for index, val in data.iteritems():
                    a.add_analytic(AssetAnalytic(ticker, 'PX_LAST', index, float(val)))

                if ticker == ta.signal_ticker:
                    ta.signal_asset = a
                if ticker == ta.future_ticker:
                    ta.future_asset = a

        t_asset_inputs.append(ta)
    t.asset_inputs = t_asset_inputs
    return t

