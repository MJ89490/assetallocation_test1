from app.data_import.read_data_from_excel import ReadDataFromExcel
from app.data_import.assets_names import Assets

import pandas as pd


class CleaningDataFromExcel(ReadDataFromExcel):
    """
        Class cleaning up data
    """
    def __init__(self):
        super().__init__()
        self.times_signals = pd.DataFrame()
        self.times_returns = pd.DataFrame()
        self.times_positions = pd.DataFrame()

    def data_processing(self):
        """
        Function performing data processing
        Firstly, we split up the data into Signals, Returns and Positions
        Secondly, we are doing the dates processing for Signals, Returns and Positions
        Finally, we name the columns of each dataFrame
        """

        self.times_signals = self.data.loc[:, 'TIMES Signals': 'GBP']
        self.times_returns = self.data.loc[:, 'TIMES Returns': 'GBP.1']
        self.times_positions = self.data.loc[:, 'TIMES Positions': 'GBP.2']

        # Dates processing
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

        # Columns processing

        assets = [asset.name for asset in Assets]

        self.times_signals.columns = assets
        self.times_positions.columns = assets
        self.times_returns.columns = assets
