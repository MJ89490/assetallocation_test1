from assetallocation_UI.aa_web_app.data_import.read_data_from_excel import ReadDataFromExcel
from assetallocation_UI.aa_web_app.data_import.assets_names import Assets
from assetallocation_UI.aa_web_app.data_import import constant
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

        self.times_signals = self.data.loc[:, constant.TIMES_SIGNALS: 'GBP']
        self.times_returns = self.data.loc[:, constant.TIMES_RETURNS: 'GBP.1']
        self.times_positions = self.data.loc[:, constant.TIMES_POSITIONS: 'GBP.2']

        # Dates processing
        dates_signals = self.times_signals.loc[:, constant.TIMES_SIGNALS]
        dates_returns = self.times_returns.loc[:, constant.TIMES_RETURNS]
        dates_positions = self.times_positions.loc[:, constant.TIMES_POSITIONS]

        del self.times_signals[constant.TIMES_SIGNALS]
        del self.times_returns[constant.TIMES_RETURNS]
        del self.times_positions[constant.TIMES_POSITIONS]

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
