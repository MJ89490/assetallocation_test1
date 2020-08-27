from assetallocation_UI.aa_web_app.data_import.import_data_from_excel import ChartsDataFromExcel
from assetallocation_UI.aa_web_app.data_import.charts_data_computations import ChartsDataComputations

import os
import sys


def main_data(times_version: int):
    """
    Function main to run the ChartsDataFromExcel class
    :return: dictionary with all the data needed for the Front-End
    """
    obj_charts_data = ChartsDataFromExcel()
    obj_charts_data.path_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "arp_dashboard_charts.xlsm"))

    obj_charts_data.import_data()
    obj_charts_data.data_processing()

    obj_charts_data.start_date_chart = "2018-09-06"  # default start date
    obj_charts_data.end_date_chart = "2019-11-28"    # default end date
    obj_charts_data.data_charts()

    data = obj_charts_data.data_charts()

    print('times_signals', data['times_signals'].head())
    print('times_positions', data['times_positions'].head())
    print('times_returns', data['times_returns'].head())

    obj_charts_comp = ChartsDataComputations(times_signals=data['times_signals'],
                                             times_positions=data['times_positions'],
                                             times_returns=data['times_returns'])

    obj_charts_comp.end_year_date = '2018-12-31'
    data_comp = obj_charts_comp.data_computations()
    data_comp_sum = obj_charts_comp.data_computations_sum()

    # use map, map data to values: first way
    # json: second way
    # meta classes : third way
    # collections : fourth way
    template_data = {"times_data": data, "times_sum": data_comp_sum, "times_data_comp": data_comp}

    return template_data


if __name__ == "__main__":
    sys.exit(main_data())
