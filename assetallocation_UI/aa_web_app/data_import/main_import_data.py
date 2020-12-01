import sys

from assetallocation_UI.aa_web_app.data_import.charts_data_computations import TimesChartsDataComputations
from assetallocation_arp.data_etl.dal.arp_proc_caller import TimesProcCaller
from assetallocation_arp.common_libraries.dal_enums.strategy import Name
from assetallocation_arp.common_libraries.dal_enums.fund_strategy import Signal, Performance
from assetallocation_arp.data_etl.dal.data_frame_converter import DataFrameConverter


def main_data(fund_name: str, times_version: int):
    """
    Function main to run the TimesChartsDataComputations class
    :return: dictionary with all the data needed for the Front-End
    """
    apc = TimesProcCaller()
    fs = apc.select_fund_strategy_results(fund_name, Name.times, times_version)
    weight_df = DataFrameConverter.fund_strategy_asset_weights_to_df(fs.asset_weights)
    analytic_df = DataFrameConverter.fund_strategy_asset_analytics_to_df(fs.analytics)

    data = {'times_signals': analytic_df.xs(Signal.momentum, level='analytic_subcategory'),
            'times_returns': analytic_df.xs(Performance['excess return'], level='analytic_subcategory'),
            'times_positions': weight_df}

    obj_charts_comp = TimesChartsDataComputations(times_signals=data['times_signals'],
                                                  times_positions=data['times_positions'],
                                                  times_returns=data['times_returns'])

    data_comp = obj_charts_comp.data_computations()
    data_comp_sum = obj_charts_comp.data_computations_sum()
    positions, names_pos, dates_pos = obj_charts_comp.process_data_from_a_specific_date(data['times_positions'])

    # template_data = {"times_data": data, "times_sum": data_comp_sum, "times_data_comp": data_comp}
    template_data = {"positions": positions, "names_pos": names_pos, "dates_pos": dates_pos}

    return template_data


if __name__ == "__main__":
    main_data('f1', 509)
