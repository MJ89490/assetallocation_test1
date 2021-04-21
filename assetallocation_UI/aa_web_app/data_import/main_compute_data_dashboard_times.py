from assetallocation_UI.aa_web_app.data_import.compute_data_dashboard_times import ComputeDataDashboardTimes


def main_compute_data_dashboard_times(obj_charts_data: ComputeDataDashboardTimes, strategy_weight: float,
                                      start_date_sum: None, start_date: None, end_date: None):
    """
    Function main to run the TimesChartsDataComputations class
    :return: dictionary with all the data needed for the Front-End
    """

    # Performances
    weekly_all_perf = obj_charts_data.compute_weekly_performance_each_asset()
    ytd_all_perf = obj_charts_data.compute_ytd_performance_each_asset()

    # Positions
    mom_signals = obj_charts_data.compute_mom_signals_each_asset()
    positions, dates_pos = obj_charts_data.compute_positions_position_1y_each_asset(strategy_weight,
                                                                                    start_date,
                                                                                    end_date)

    previous_positions = obj_charts_data.compute_previous_positions_each_asset(strategy_weight)
    new_positions = obj_charts_data.compute_new_positions_each_asset(strategy_weight)
    delta_positions = obj_charts_data.compute_delta_positions_each_asset(previous_positions,
                                                                         new_positions)
















    # Category
    category = obj_charts_data.classify_assets_by_category()

    # Positions







    trade_positions = obj_charts_data.compute_trade_positions_all_assets_overview(delta_positions)

    # Performance overall
    weekly_overall = obj_charts_data.compute_overall_performance_all_assets_overview(
                                                                   weekly_all_perf['weekly_performance_all_currencies'])

    ytd_overall = obj_charts_data.compute_overall_performance_all_assets_overview(
                                                                   ytd_all_perf['ytd_performance_all_currencies'])

    # Positions overall
    pre_overall = obj_charts_data.compute_overall_performance_all_assets_overview(previous_positions)

    new_overall = obj_charts_data.compute_overall_performance_all_assets_overview(implemented_weight)

    # Size
    size_pos = obj_charts_data.compute_size_positions_all_assets_overview(implemented_weight, new_overall)

    positions_assets_sum = obj_charts_data.compute_sum_positions_assets_charts(strategy_weight, start_date_sum)

    # Percentile
    titles_ids = {}

    tmp_cat_positions = []

    for cat in category:
        ninety_fifth_percentile = obj_charts_data.compute_ninety_fifth_percentile(positions_assets_sum[cat])
        percentile_fifth_percentile = obj_charts_data.compute_fifth_percentile(positions_assets_sum[cat])

        percentile_ninety_five_perc = obj_charts_data.build_percentile_list(ninety_fifth_percentile)
        percentile_fifth_perc = obj_charts_data.build_percentile_list(percentile_fifth_percentile)

        tmp_cat_positions.append(positions_assets_sum[cat])
        tmp_cat_positions.append(percentile_ninety_five_perc)
        tmp_cat_positions.append(percentile_fifth_perc)
        tmp_cat_positions.append(positions_assets_sum['dates_positions_assets'])

        titles_ids[cat] = tmp_cat_positions

    # Create a zip to build performance and positions tables in dashboard
    pos_keys = ["category_name", "names_weekly_perf", "mom_signals", "prev_positions", "new_positions",
                "delta_positions", "trade_positions", "size_positions", "imp_weight"]
    perf_keys = ["weekly_performance_all_currencies", "ytd_performance_all_currencies"]
    pos_overall_keys = ["category_name",  "pre_overall", "new_overall"]
    perf_overall_keys = ["weekly_overall", "ytd_overall"]

    results_positions = obj_charts_data.build_dict_ready_for_zip(category,
                                                                 weekly_all_perf['assets'],
                                                                 mom_signals,
                                                                 previous_positions,
                                                                 implemented_weight,
                                                                 delta_positions,
                                                                 trade_positions,
                                                                 size_pos,
                                                                 implemented_weight,
                                                                 keys=pos_keys)

    results_perf = obj_charts_data.build_dict_ready_for_zip(weekly_all_perf['weekly_performance_all_currencies'],
                                                            ytd_all_perf['ytd_performance_all_currencies'],
                                                            keys=perf_keys)

    results_positions_overall = obj_charts_data.build_dict_ready_for_zip(
                                                            category + ['Total'],
                                                            pre_overall,
                                                            new_overall,
                                                            keys=pos_overall_keys)

    results_perf_overall = obj_charts_data.build_dict_ready_for_zip(weekly_overall,
                                                                    ytd_overall,
                                                                    keys=perf_overall_keys)

    zip_results_pos = obj_charts_data.zip_results_performance_all_assets_overview(results_positions)
    zip_results_pos_overall = obj_charts_data.zip_results_performance_all_assets_overview(results_positions_overall)
    zip_results_perf = obj_charts_data.zip_results_performance_all_assets_overview(results_perf)
    zip_results_perf_overall = obj_charts_data.zip_results_performance_all_assets_overview(results_perf_overall)

    # Dictionary containing results needed for dashboard
    template_data = {"positions": positions,
                     "dates_pos": dates_pos,
                     "names_pos": obj_charts_data.get_names_assets,
                     "weekly_overall": weekly_overall,
                     "signal_as_off": obj_charts_data.get_signal_as_off,
                     "mom_signals": mom_signals,
                     "prev_positions": previous_positions,
                     "new_positions": implemented_weight,
                     "assets_names": weekly_all_perf['assets'],
                     "weekly_performance_all_currencies": weekly_all_perf['weekly_performance_all_currencies'],
                     "ytd_performance_all_currencies": ytd_all_perf['ytd_performance_all_currencies'],
                     "pre_overall": pre_overall,
                     "zip_results_pos": zip_results_pos,
                     "zip_results_pos_overall": zip_results_pos_overall,
                     "zip_results_perf": zip_results_perf,
                     "zip_results_perf_overall": zip_results_perf_overall,
                     "titles_ids": titles_ids
                     }

    return template_data
