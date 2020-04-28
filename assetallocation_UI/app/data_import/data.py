import pandas as pd

import enum
#todo put one class per module
#todo move to a module.py but issue to import module in the data.py
class Assets(enum.Enum):
    US_Equities = 0
    EU_Equities = 1
    JP_Equities = 2
    HK_Equities = 3
    US_10_y_Bonds = 4
    UK_10_y_Bonds = 5
    EU_10_y_Bonds = 6
    CA_10_y_Bonds = 7
    JPY = 8
    EUR = 9
    AUD = 10
    CAD = 11
    GBP = 12


class ReadDataFromExcel:
    def __init__(self):
        self.data = pd.DataFrame()
        self.path = ""

    @property
    def path_file(self):
        return self.path

    @path_file.setter
    def path_file(self, value):
        self.path = value

    def import_data(self):
        self.data = pd.read_excel(self.path, sheet_name="times_output")


class CleaningDataFromExcel(ReadDataFromExcel):
    def __init__(self):
        super().__init__()
        self.times_signals = pd.DataFrame()
        self.times_returns = pd.DataFrame()
        self.times_positions = pd.DataFrame()

    def data_processing(self):

        self.times_signals = self.data.loc[:, 'TIMES Signals': 'GBP']
        self.times_returns = self.data.loc[:, 'TIMES Returns': 'GBP.1']
        self.times_positions = self.data.loc[:, 'TIMES Positions': 'GBP.2']

    def date_processing(self):

        dates_signals = self.times_signals.loc[:, 'TIMES Signals']
        dates_returns = self.times_returns.loc[:, 'TIMES Returns']
        dates_positions = self.times_positions.loc[:, 'TIMES Positions']

        del self.times_signals['TIMES Signals']
        del self.times_returns['TIMES Returns']
        del self.times_positions['TIMES Positions']

        self.times_signals = self.times_signals.set_index(dates_signals)
        self.times_returns = self.times_returns.set_index(dates_returns)
        self.times_positions = self.times_positions.set_index(dates_positions)

        last_valid_dates_times_signals = self.times_signals.last_valid_index()
        last_valid_dates_times_returns = self.times_returns.last_valid_index()
        last_valid_dates_times_positions = self.times_positions.last_valid_index()

        self.times_signals = self.times_signals.loc[:last_valid_dates_times_signals]
        self.times_returns = self.times_returns.loc[:last_valid_dates_times_returns]
        self.times_positions = self.times_positions.loc[:last_valid_dates_times_positions]

    def columns_names_processing(self):

        assets = [asset.name for asset in Assets]

        self.times_signals.columns = assets
        self.times_positions.columns = assets
        self.times_returns.columns = assets


class ChartsDataFromExcel(CleaningDataFromExcel):
    def __init__(self):
        super().__init__()
        self.start_date = "" # default start date
        self.end_date = ""   # default end_date
        self.times_positions_dates = pd.DataFrame()
        self.times_returns_dates = pd.DataFrame()
        self.times_signals_dates = pd.DataFrame()

    @property
    def start_date_chart(self):
        return self.start_date

    @start_date_chart.setter
    def start_date_chart(self, value):
        self.start_date = value

    @property
    def end_date_chart(self):
        return self.end_date

    @end_date_chart.setter
    def end_date_chart(self, value):
        self.end_date = value

    def data_charts(self):

        self.times_positions_dates = self.times_positions[self.start_date:self.end_date]
        self.times_signals_dates = self.times_signals[self.start_date:self.end_date]
        self.times_returns_dates = self.times_returns[self.start_date:self.end_date]

    def template_data_charts(self):

        return {"times_returns":self.times_returns_dates,
                "times_positions": self.times_positions_dates,
                "times_signals": self.times_signals_dates}


# if __name__ == "__main__":
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
#     d = obj_charts_data.template_data_charts()


#todo put in a main module
def run_times():
    obj_charts_data = ChartsDataFromExcel()
    obj_charts_data.path_file = r'C:\Users\AJ89720\PycharmProjects\assetallocation_arp\assetallocation_UI\app\arp_dashboard_charts.xlsm'
    obj_charts_data.import_data()
    obj_charts_data.data_processing()
    obj_charts_data.date_processing()
    obj_charts_data.columns_names_processing()
    obj_charts_data.start_date_chart = "2018-09-06"
    obj_charts_data.end_date_chart = "2019-10-24"
    obj_charts_data.data_charts()

    data = obj_charts_data.template_data_charts()

    return data['times_returns'], data['times_positions'], data['times_signals']






