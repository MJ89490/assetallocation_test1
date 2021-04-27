from assetallocation_UI.aa_web_app.data_import.compute_data_dashboard_times import ComputeDataDashboardTimes


def main_compute_data_dashboard_times(obj_charts_data: ComputeDataDashboardTimes, strategy_weight: float,
                                      start_date_sum: None, start_date: None, end_date: None):
    """
    Function main to run the TimesChartsDataComputations class
    :return: dictionary with all the data needed for the Front-End
    """

    # Performances
    weekly_performance, weekly_performance_lst = obj_charts_data.compute_weekly_performance_each_asset()
    ytd_performance, ytd_performance_lst = obj_charts_data.compute_ytd_performance_each_asset()

    # Positions
    mom_signals = obj_charts_data.compute_mom_signals_each_asset()
    position_1y, dates_pos, position_1y_per_asset, position_1y_lst = obj_charts_data.compute_positions_position_1y_each_asset(strategy_weight,
                                                                                                       start_date,
                                                                                                       end_date)

    previous_positions, previous_positions_lst = obj_charts_data.compute_previous_positions_each_asset(strategy_weight)

    new_positions, new_positions_lst = obj_charts_data.compute_new_positions_each_asset(strategy_weight)

    delta_positions = obj_charts_data.compute_delta_positions_each_asset(previous_positions_lst,
                                                                         new_positions_lst)

    trade_positions = obj_charts_data.compute_trade_positions_each_asset(previous_positions, new_positions)

    # Positions per category
    new_positions_per_category = obj_charts_data.compute_positions_performance_per_category(new_positions)

    previous_positions_per_category = obj_charts_data.compute_positions_performance_per_category(previous_positions)

    size_positions = obj_charts_data.compute_size_positions_each_asset(new_positions, new_positions_per_category)

    # Performance per category
    weekly_performance_per_category = obj_charts_data.compute_positions_performance_per_category(weekly_performance, True)

    ytd_performance_per_category = obj_charts_data.compute_positions_performance_per_category(ytd_performance, True)

    # Sum of the assets
    sum_positions_per_category = obj_charts_data.sum_positions_each_asset_into_category(position_1y)

    # Percentile
    ninety_fifth_percentile_per_category = obj_charts_data.compute_percentile_per_category(
                                           sum_positions_per_category, percentile=95)

    fifth_percentile_per_category = obj_charts_data.compute_percentile_per_category(
                                    sum_positions_per_category, percentile=5)

    ninety_fifth_percentile_per_category_lst = obj_charts_data.build_percentile_list(ninety_fifth_percentile_per_category, len(dates_pos))
    fifth_percentile_per_category_lst = obj_charts_data.build_percentile_list(fifth_percentile_per_category, len(dates_pos))

    titles_ids = {}

    tmp_cat_positions = []

    for cat in sorted(set(obj_charts_data.get_asset_names_per_category_sorted)):
        tmp_cat_positions.append(sum_positions_per_category[cat])
        tmp_cat_positions.append(ninety_fifth_percentile_per_category_lst[cat])
        tmp_cat_positions.append(fifth_percentile_per_category_lst[cat])
        tmp_cat_positions.append(dates_pos)

        titles_ids[cat] = tmp_cat_positions
        tmp_cat_positions = []

    # Create a zip to build performance and positions tables in dashboard
    pos_keys = ["category_name", "names_weekly_perf", "mom_signals", "prev_positions", "new_positions",
                "delta_positions", "trade_positions", "size_positions", "imp_weight"]
    perf_keys = ["names_assets", "weekly_performance_all_currencies", "ytd_performance_all_currencies"]
    pos_overall_keys = ["category_name",  "pre_overall", "new_overall"]
    perf_overall_keys = ["weekly_overall", "ytd_overall"]

    results_positions = obj_charts_data.build_dict_ready_for_zip(obj_charts_data.get_asset_names_per_category_sorted,
                                                                 obj_charts_data.get_asset_names,
                                                                 mom_signals,
                                                                 previous_positions_lst,
                                                                 new_positions_lst,
                                                                 delta_positions,
                                                                 trade_positions,
                                                                 size_positions,
                                                                 new_positions_lst,
                                                                 keys=pos_keys)

    results_perf = obj_charts_data.build_dict_ready_for_zip(obj_charts_data.get_asset_names,
                                                            weekly_performance_lst,
                                                            ytd_performance_lst,
                                                            keys=perf_keys)

    results_positions_overall = obj_charts_data.build_dict_ready_for_zip(
                                                            sorted(set(obj_charts_data.get_asset_names_per_category_sorted)) + ['Total'],
                                                            previous_positions_per_category.values(),
                                                            new_positions_per_category.values(),
                                                            keys=pos_overall_keys)

    results_perf_overall = obj_charts_data.build_dict_ready_for_zip(weekly_performance_per_category.values(),
                                                                    ytd_performance_per_category.values(),
                                                                    keys=perf_overall_keys)

    zip_results_pos = obj_charts_data.zip_results_performance_all_assets_overview(results_positions)

    zip_results_pos_overall = obj_charts_data.zip_results_performance_all_assets_overview(results_positions_overall)
    zip_results_perf = obj_charts_data.zip_results_performance_all_assets_overview(results_perf)
    zip_results_perf_overall = obj_charts_data.zip_results_performance_all_assets_overview(results_perf_overall)

    # Dictionary containing results needed for dashboard
    template_data = {"positions": position_1y_lst,
                     "position_1y_per_asset": position_1y_per_asset,
                     "dates_pos": dates_pos,
                     "names_pos": obj_charts_data.get_asset_names,
                     "weekly_overall": weekly_performance_per_category,
                     "signal_as_off": obj_charts_data.get_signal_as_off,
                     "mom_signals": mom_signals,
                     "prev_positions": previous_positions_lst,
                     "new_positions": new_positions_lst,
                     "assets_names": obj_charts_data.get_asset_names,
                     "weekly_performance_all_currencies": weekly_performance_lst,
                     "ytd_performance_all_currencies": ytd_performance_lst,
                     "pre_overall": previous_positions_per_category,
                     "zip_results_pos": zip_results_pos,
                     "zip_results_pos_overall": zip_results_pos_overall,
                     "zip_results_perf": zip_results_perf,
                     "zip_results_perf_overall": zip_results_perf_overall,
                     "titles_ids": titles_ids
                     }

    return template_data
