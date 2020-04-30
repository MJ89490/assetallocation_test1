from app.data_import.import_data_from_excel import ChartsDataFromExcel
from app.data_import.charts_data_computations import ChartsDataComputations

import sys




def main():
    obj_charts_data = ChartsDataFromExcel()
    obj_charts_data.path_file = r'C:\Users\AJ89720\PycharmProjects\assetallocation_arp\assetallocation_UI\app\arp_dashboard_charts.xlsm'
    obj_charts_data.import_data()
    obj_charts_data.data_processing()
    obj_charts_data.date_processing()
    obj_charts_data.columns_names_processing()
    obj_charts_data.start_date_chart = "2018-09-06"
    obj_charts_data.end_date_chart = "2019-10-24"
    obj_charts_data.data_charts()

    data = obj_charts_data.data_charts()

    obj_charts_comp = ChartsDataComputations(times_signals=data['times_signals'],
                                             times_positions=data['times_positions'],
                                             times_returns=data['times_returns'])

    signal_off = ChartsDataComputations.signals_dates_off.__get__(obj_charts_comp)
    returns_off = ChartsDataComputations.returns_dates_off.__get__(obj_charts_comp)
    positions_off = ChartsDataComputations.positions_dates_off.__get__(obj_charts_comp)
    returns_weekly_off = ChartsDataComputations.returns_dates_weekly_off.__get__(obj_charts_comp)

    obj_charts_comp.end_year_date = '2018-12-31'

    data_comp = obj_charts_comp.data_computations(signal_off=signal_off, returns_off=returns_off, positions_off=positions_off,
                                                  returns_weekly_off=returns_weekly_off)

    data_comp_sum = obj_charts_comp.data_computations_sum(times_returns_ytd=data_comp['times_returns_ytd'],
                                                          times_positions_comp=data_comp['times_positions_comp'],
                                                          times_returns=data_comp['times_returns_comp'])

    return data['times_returns'], data['times_positions'], data['times_signals']


if __name__ == "__main__":
    sys.exit(main())


# def run_times():
#     obj_charts_data = ChartsDataFromExcel()
#     obj_charts_data.path_file = r'C:\Users\AJ89720\PycharmProjects\assetallocation_arp\assetallocation_UI\app\arp_dashboard_charts.xlsm'
#     obj_charts_data.import_data()
#     obj_charts_data.data_processing()
#     obj_charts_data.date_processing()
#     obj_charts_data.columns_names_processing()
#     obj_charts_data.start_date_chart = "2018-09-06"
#     obj_charts_data.end_date_chart = "2019-10-24"
#     obj_charts_data.data_charts()
#
#     data = obj_charts_data.template_data_charts()
#
#     # obj_charts_comp = ChartsDataComputations(times_signals=data['times_signals'],
#     #                                          times_positions=data['times_positions'],
#     #                                          times_returns=data['times_returns'])
#     #
#     # obj_charts_comp.end_year_date = '2018-12-31'
#     # data_comp = obj_charts_comp.data_computations()
#     # data_comp_sum = obj_charts_comp.data_computations_sum(times_returns_ytd=data_comp['times_returns_ytd'])
#
#     return data['times_returns'], data['times_positions'], data['times_signals']



    #
    # return data['times_returns'], data['times_positions'], data['times_signals'], data_comp['times_signals_comp'], \
    #        data_comp['times_positions_comp'], data_comp['times_returns_comp'], data_comp_sum['sum_positions_equities'],\
    #        data_comp_sum['sum_positions_bonds'], data_comp_sum['sum_positions_fx'], data_comp_sum['sum_performance_weekly_equities'], \
    #        data_comp_sum['sum_performance_weekly_bonds'], data_comp_sum['sum_performance_weekly_fx'], data_comp_sum['sum_performance_ytd_equities'], \
    #        data_comp_sum['sum_performance_ytd_bonds'], data_comp_sum['sum_performance_ytd_fx']