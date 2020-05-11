import pandas as pd


class ReadDataFromExcel:
    """
        Class reading the data from Excel
    """
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
        """
        Function reading data from Excel
        """
        self.data = pd.read_excel(self.path, sheet_name="times_output")
