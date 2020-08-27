import sys

from assetallocation_UI.aa_web_app.data_import.charts_data_computations import TimesChartsDataComputations
from assetallocation_arp.data_etl.dal.arp_proc_caller import ArpProcCaller
from assetallocation_arp.common_libraries.dal_enums.strategy import Name
from assetallocation_arp.common_libraries.dal_enums.fund_strategy import Signal, Performance
from assetallocation_arp.data_etl.dal.data_frame_converter import DataFrameConverter


def main_data(fund_name: str, times_version: int):
    """
    Function main to run the TimesChartsDataComputations class
    :return: dictionary with all the data needed for the Front-End
    """
    apc = ArpProcCaller()
    fs = apc.select_fund_strategy_results(fund_name, Name.times, times_version)
    weight_df = DataFrameConverter.fund_strategy_asset_weights_to_df(fs.asset_weights)
    analytic_df = DataFrameConverter.fund_strategy_asset_analytics_to_df(fs.asset_analytics)

    data = {'times_signals': analytic_df.xs(Signal.momentum, level='subcategory'),
            'times_returns': analytic_df.xs(Performance['excess return'], level='subcategory'),
            'times_positions': weight_df}

    obj_charts_comp = TimesChartsDataComputations(times_signals=data['times_signals'],
                                                  times_positions=data['times_positions'],
                                                  times_returns=data['times_returns'])

    data_comp = obj_charts_comp.data_computations()
    data_comp_sum = obj_charts_comp.data_computations_sum()

    template_data = {"times_data": data, "times_sum": data_comp_sum, "times_data_comp": data_comp}

    return template_data


if __name__ == "__main__":
    sys.exit(main_data())
