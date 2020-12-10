import sys

from assetallocation_UI.aa_web_app.data_import.compute_charts_data import TimesChartsDataComputations
from assetallocation_arp.data_etl.dal.arp_proc_caller import TimesProcCaller
from assetallocation_arp.common_libraries.dal_enums.strategy import Name
from assetallocation_arp.common_libraries.dal_enums.fund_strategy import Signal, Performance
from assetallocation_arp.data_etl.dal.data_frame_converter import DataFrameConverter


# def main_data(fund_name: str, times_version: int, strategy_weight: float, obj_received_data_times: object):
def main_data(obj_received_data_times: object):
    """
    Function main to run the TimesChartsDataComputations class
    :return: dictionary with all the data needed for the Front-End
    """

    apc = TimesProcCaller()
    fs = apc.select_fund_strategy_results(obj_received_data_times.fund_name, Name.times, obj_received_data_times.version_strategy)
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

    #TODO to improve
    weekly_overall = obj_charts_comp.compute_overall_performance_all_assets_overview(weekly_performance_all_currencies, names_weekly_perf, category_name)
    ytd_overall = obj_charts_comp.compute_overall_performance_all_assets_overview(ytd_performance_all_currencies, names_ytd_perf, category_name)
    pre_overall = obj_charts_comp.compute_overall_performance_all_assets_overview(previous_positions, names_weekly_perf, category_name)
    new_overall = obj_charts_comp.compute_overall_performance_all_assets_overview(new_positions, names_weekly_perf, category_name)

    size = obj_charts_comp.compute_size_positions_all_assets_overview(new_positions, names_weekly_perf, category_name, new_overall)

    positions_assets_sum = obj_charts_comp.compute_positions_assets_charts(obj_received_data_times.strategy_weight)

    # Percentile 95th
    equities_ninety_five_perc = obj_charts_comp.compute_ninety_fifth_percentile(positions_assets_sum['equities_pos_sum'])
    bonds_ninety_five_perc = obj_charts_comp.compute_ninety_fifth_percentile(positions_assets_sum['bonds_pos_sum'])
    forex_ninety_five_perc = obj_charts_comp.compute_ninety_fifth_percentile(positions_assets_sum['forex_pos_sum'])

    # Percentile 5th
    equities_fifth_perc = obj_charts_comp.compute_fifth_percentile(positions_assets_sum['equities_pos_sum'])
    bonds_fifth_perc = obj_charts_comp.compute_fifth_percentile(positions_assets_sum['bonds_pos_sum'])
    forex_fifth_perc = obj_charts_comp.compute_fifth_percentile(positions_assets_sum['forex_pos_sum'])

    # Build percentile list for positions charts
    equities_ninety_five_percentile = obj_charts_comp.build_percentile_list(equities_ninety_five_perc)
    bonds_ninety_five_percentile = obj_charts_comp.build_percentile_list(bonds_ninety_five_perc)
    forex_ninety_five_percentile = obj_charts_comp.build_percentile_list(forex_ninety_five_perc)

    equities_fifth_percentile = obj_charts_comp.build_percentile_list(equities_fifth_perc)
    bonds_fifth_percentile = obj_charts_comp.build_percentile_list(bonds_fifth_perc)
    forex_fifth_percentile = obj_charts_comp.build_percentile_list(forex_fifth_perc)


    results_positions = {"category_name": category_name,
                         "names_weekly_perf": names_weekly_perf,
                         "mom_signals": mom_signals,
                         "prev_positions": previous_positions,
                         "new_positions": new_positions,
                         "delta_positions": delta_positions,
                         "trade_positions": trade_positions,
                         "size_positions": size}
    results_perf = {"weekly_performance_all_currencies": weekly_performance_all_currencies,
                    "ytd_performance_all_currencies": ytd_performance_all_currencies}

    results_positions_overall = {"category_name": ['Equities', 'FX', 'Bonds', 'Total'],
                                 "pre_overall": pre_overall, "new_overall": new_overall}

    results_perf_overall = {"weekly_overall": weekly_overall, "ytd_overall": ytd_overall}

    zip_results_pos = obj_charts_comp.zip_results_performance_all_assets_overview(results_positions)
    zip_results_pos_overall = obj_charts_comp.zip_results_performance_all_assets_overview(results_positions_overall)
    zip_results_perf = obj_charts_comp.zip_results_performance_all_assets_overview(results_perf)
    zip_results_perf_overall = obj_charts_comp.zip_results_performance_all_assets_overview(results_perf_overall)

    template_data = {"positions": positions, "dates_pos": dates_pos, "names_pos": names_pos,
                     "sparklines_pos": sparklines_pos, "weekly_overall": weekly_overall,
                     "signal_as_off": signal_as_off, "positions_assets_sum": positions_assets_sum,
                     "equities_fifth_percentile": equities_fifth_percentile,
                     "equities_ninety_five_percentile": equities_ninety_five_percentile,
                     "bonds_ninety_five_percentile": bonds_ninety_five_percentile,
                     "bonds_fifth_percentile": bonds_fifth_percentile,
                     "forex_ninety_five_percentile": forex_ninety_five_percentile,
                     "forex_fifth_percentile": forex_fifth_percentile}

    return template_data, zip_results_pos, zip_results_pos_overall, zip_results_perf, zip_results_perf_overall


# if __name__ == "__main__":
#     main_data('f1', 509)
