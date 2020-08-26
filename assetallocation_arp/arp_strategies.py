import os
import sys
from typing import Tuple, List

import pandas as pd

from common_libraries.dal_enums.strategy import Name
import assetallocation_arp.data_etl.import_all_data as gd
from assetallocation_arp.data_etl import import_data_from_excel_matlab as gd
from assetallocation_arp.models import times, fica, maven, fxmodels
from assetallocation_arp.models.times import create_times_asset_analytics, df_to_asset_weights,\
    calculate_signals_returns_r_positioning
from assetallocation_arp.data_etl.dal.data_models.fund_strategy import FundStrategyAssetAnalytic, \
    FundStrategyAssetWeight
from assetallocation_arp.data_etl.dal.data_models.strategy import Times

ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
print(ROOT_DIR)
sys.path.insert(0, ROOT_DIR)


def run_model(model_type, mat_file, input_file, model_date=None):
    if model_type == Name.times.name:
        # get inputs from excel and matlab data
        times_inputs, asset_inputs, all_data = gd.extract_inputs_and_mat_data(model_type, mat_file, input_file,
                                                                              model_date)
        # run strategy
        signals, returns, r, positioning = times.format_data_and_calc(times_inputs, asset_inputs, all_data)
        # write results to output sheet
        write_output_to_excel({Name.times.name: (asset_inputs, positioning, r, signals, times_inputs)}, input_file)

    if model_type == Name.maven.name:
        # get inputs from excel and matlab data
        maven_inputs, asset_inputs, all_data = gd.extract_inputs_and_mat_data(model_type, mat_file, input_file,
                                                                              model_date)
        # calculate asset return index series and and maven's excess return index series
        asset_returns = maven.format_data(maven_inputs, asset_inputs, all_data)
        maven_returns = maven.calculate_excess_returns(maven_inputs, asset_inputs, asset_returns)
        # calculate value and momentum scores, and the top/bottom countries on the combination score
        momentum, value, long_signals, short_signals, long_signals_name, short_signals_name, value_last, momentum_last, long_list, short_list, volatility = maven.calculate_signals(
            maven_inputs, maven_returns)
        # calculate maven return series, and benchmarks, asset class exposures and contributions
        returns_maven, asset_class_long, asset_class_short, asset_contribution_long, asset_contribution_short = maven.run_performance_stats(
            maven_inputs, asset_inputs, maven_returns, volatility, long_signals, short_signals)
        # write results to output sheet
        write_output_to_excel({Name.maven.name: (
            momentum, value, long_signals_name, short_signals_name, value_last, momentum_last, long_list, short_list,
            returns_maven, asset_class_long, asset_class_short, asset_contribution_long, asset_contribution_short,
            asset_inputs, maven_inputs)}, input_file)
    if model_type == Name.effect.name:
        print(model_type)

    if model_type == Name.fxmodels.name:
        # get inputs from excel and matlab data
        fxmodels_inputs, asset_inputs, all_data = gd.extract_inputs_and_mat_data(model_type, mat_file, input_file)
        # create the input series for the signal types
        spot, carry, cash, ppp = fxmodels.format_data(fxmodels_inputs, asset_inputs, all_data)
        # calculate signals
        signal, volatility = fxmodels.calculate_signals(fxmodels_inputs, spot, carry, cash, ppp)
        # determine exposures
        fx_model, exposure, exposure_agg = fxmodels.determine_sizing(fxmodels_inputs, asset_inputs, signal, volatility)
        # calculate returns
        base_fx, returns, contribution, carry_base = fxmodels.calculate_returns(fxmodels_inputs, carry, signal,
                                                                                exposure, exposure_agg)
        # write results to output sheet
        write_output_to_excel({Name.fxmodels.name: (
            fx_model, base_fx, signal, exposure, exposure_agg, returns, contribution, carry_base, fxmodels_inputs,
            asset_inputs)}, input_file)
    if model_type == Name.fica.name:
        # get inputs from excel and matlab data
        fica_inputs, asset_inputs, all_data = gd.extract_inputs_and_mat_data(model_type, mat_file, input_file,
                                                                             model_date)
        # create yield curves and calculate carry & roll down
        curve = fica.format_data(fica_inputs, asset_inputs, all_data)
        carry_roll, country_returns = fica.calculate_carry_roll_down(fica_inputs, asset_inputs, curve)
        # run strategy
        signals, cum_contribution, returns = fica.calculate_signals_and_returns(fica_inputs, carry_roll,
                                                                                country_returns)
        # run daily attributions
        carry_daily, return_daily = fica.run_daily_attribution(fica_inputs, asset_inputs, all_data, signals)
        # write results to output sheet
        write_output_to_excel({Name.fica.name: (
            carry_roll, signals, country_returns, cum_contribution, returns, asset_inputs, fica_inputs, carry_daily,
            return_daily)}, input_file)
        print(model_type)
    if model_type == Name.comca.name:
        print(model_type)


# TODO fix strategy_weight and asset_analytic value coming out as NaN!
def run_times(strategy: Times) -> Tuple[List[FundStrategyAssetAnalytic], List[FundStrategyAssetWeight]]:
    """Run times strategy and return FundStrategyAssetAnalytics and FundStrategyAssetWeights"""
    signals, returns, r, positioning = calculate_signals_returns_r_positioning(strategy)
    asset_analytics = create_times_asset_analytics(signals, returns, r)
    asset_weights = df_to_asset_weights(positioning)
    return asset_analytics, asset_weights


def run_model_from_web_interface(model_type, mat_file=None, input_file=None):
    if model_type == Name.times.name:
        # get inputs from excel and matlab data
        times_inputs, asset_inputs, all_data = gd.extract_inputs_and_mat_data(model_type, mat_file, input_file)
        # run strategy
        signals, returns, r, positioning = times.format_data_and_calc(times_inputs, asset_inputs, all_data)

        return asset_inputs, positioning, r, signals, times_inputs


def write_output_to_excel(model_outputs, path_excel_times):
    if Name.times.name in model_outputs.keys():
        print("===models.times.name===", Name.times.name)
        print("=======model output keys===", model_outputs.keys())
        positioning, returns, signals = model_outputs[Name.times.name]
        print("===========current _path, excel path ===========", os.getcwd(), path_excel_times)
        with pd.ExcelWriter(path_excel_times) as writer:
            signals.to_excel(writer, sheet_name='signal', encoding='utf8')
            returns.to_excel(writer, sheet_name='returns', encoding='utf8')
            positioning.to_excel(writer, sheet_name='positioning', encoding='utf8')
            writer.save()


def get_inputs_from_python(model):
    # launch the script from Python
    # launch the script from Python
    mat_file = None
    input_file = None
    models_list = [model.name for model in Name]

    if model in models_list:
        model_type = model
        run_model(model_type, mat_file, input_file)
    else:
        raise NameError("Your input is incorrect.")


def get_input_user():
    model_str = input("Choose a Model: ")
    return model_str


if __name__ == "__main__":
    sys.exit(get_inputs_from_python(get_input_user()))
