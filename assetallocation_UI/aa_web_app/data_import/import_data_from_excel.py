from assetallocation_UI.aa_web_app.data_import.cleaning_data_from_excel import CleaningDataFromExcel
import pandas as pd


class ChartsDataFromExcel(CleaningDataFromExcel):
    """
        Class gathering Signals, Returns and Positions data for the dashboard
    """
    def __init__(self):
        super().__init__()
        self.start_date = ""  # default start date
        self.end_date = ""    # default end_date
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
        """
        Function gathering Signals, Positions and Returns data
        :return: dictionary with Signals, Positions and Returns
        """

        return {"times_returns": self.times_returns[self.start_date:self.end_date],
                "times_positions": self.times_positions[self.start_date:self.end_date],
                "times_signals": self.times_signals[self.start_date:self.end_date]}
    #
    # def date_charts(self):
    #
    #
    #     d = self.times_returns[self.start_date:self.end_date].index.values
    #     
    #     p =
    #     for date in d:
    #         pd.to_datetime(d[date]).date()
    #
    #     date = [pd.to_datetime(d[date]).date() for date in d]
    #
    #     return{"times_returns_dates": d }