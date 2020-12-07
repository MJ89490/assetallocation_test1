import sys

from assetallocation_UI.aa_web_app.data_import.compute_charts_data import TimesChartsDataComputations
from assetallocation_arp.data_etl.dal.arp_proc_caller import TimesProcCaller
from assetallocation_arp.common_libraries.dal_enums.strategy import Name
from assetallocation_arp.common_libraries.dal_enums.fund_strategy import Signal, Performance
from assetallocation_arp.data_etl.dal.data_frame_converter import DataFrameConverter


# def main_data(fund_name: str, times_version: int, strategy_weight: float, obj_received_data_times: object):
def main_data(fund_name: str, obj_received_data_times: object):
    """
    Function main to run the TimesChartsDataComputations class
    :return: dictionary with all the data needed for the Front-End
    """

    apc = TimesProcCaller()
    fs = apc.select_fund_strategy_results(fund_name, Name.times, obj_received_data_times.version_strategy)
    weight_df = DataFrameConverter.fund_strategy_asset_weights_to_df(fs.asset_weights)
    analytic_df = DataFrameConverter.fund_strategy_asset_analytics_to_df(fs.analytics)

    data = {'times_signals': analytic_df.xs(Signal.momentum, level='analytic_subcategory'),
            'times_returns': analytic_df.xs(Performance['excess return'], level='analytic_subcategory'),
            'times_positions': weight_df}

    obj_charts_comp = TimesChartsDataComputations(times_signals=data['times_signals'],
                                                  times_positions=data['times_positions'],
                                                  times_returns=data['times_returns'])

    signal_as_off = obj_charts_comp.signal_as_off

    weekly_performance_all_currencies, names_weekly_perf, weekly_perf_dict, category_name = obj_charts_comp.compute_weekly_performance_all_assets_overview()
    ytd_performance_all_currencies, names_ytd_perf, ytd_perf_dict, category_name = obj_charts_comp.compute_ytd_performance_all_assets_overview()
    positions, dates_pos, names_pos, sparklines_pos = obj_charts_comp.process_data_from_a_specific_date(data['times_positions'])
    mom_signals = obj_charts_comp.compute_mom_signals_all_assets_overview()
    previous_positions = obj_charts_comp.compute_previous_positions_all_assets_overview(obj_received_data_times.strategy_weight)
    new_positions = obj_charts_comp.compute_new_positions_all_assets_overview(obj_received_data_times.strategy_weight)
    delta_positions = obj_charts_comp.compute_delta_positions_all_assets_overview(previous_positions, new_positions)
    trade_positions = obj_charts_comp.compute_trade_positions_all_assets_overview(delta_positions)

    weekly_overall = obj_charts_comp.compute_weekly_ytd_overall_performance_all_assets_overview(weekly_performance_all_currencies, names_weekly_perf, category_name)
    ytd_overall = obj_charts_comp.compute_weekly_ytd_overall_performance_all_assets_overview(ytd_performance_all_currencies, names_ytd_perf, category_name)

    results_performance = {"category_name": category_name,
                           "names_weekly_perf": names_weekly_perf,
                           "mom_signals": mom_signals,
                           "prev_positions": previous_positions,
                           "new_positions": new_positions,
                           "delta_positions": delta_positions,
                           "trade_positions": trade_positions,
                           "weekly_performance_all_currencies": weekly_performance_all_currencies,
                           "ytd_performance_all_currencies": ytd_performance_all_currencies,
                           }

    results_weekly_ytd_overall = {"category_name": ['Equities', 'FX', 'Bonds'], "weekly_overall": weekly_overall,
                                  "ytd_overall": ytd_overall}

    zip_results_perf = obj_charts_comp.zip_results_performance_all_assets_overview(results_performance)
    zip_results_weekly_ytd_overall = obj_charts_comp.zip_results_performance_all_assets_overview(results_weekly_ytd_overall)

    template_data = {"positions": positions, "dates_pos": dates_pos, "names_pos": names_pos,
                     "sparklines_pos": sparklines_pos, "weekly_overall": weekly_overall,
                     "signal_as_off": signal_as_off}

    return template_data, zip_results_perf, zip_results_weekly_ytd_overall


if __name__ == "__main__":
    main_data('f1', 509)
