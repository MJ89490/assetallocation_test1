"""
Created on Fri Nov  8 17:27:51 2019
DATA IMPORT
@author: SN69248
"""

import scipy.io as spio
import pandas as pd
import openpyxl
import os
import sys
import numpy as np
from datetime import datetime


def matfile_to_dataframe(file_path, model_date):
    """ Reads Matlab file and formats data into dataframe"""
    mat_file_data = spio.loadmat(file_path)

    mat_dates = pd.DataFrame(mat_file_data['dates'])
    mat_dates = mat_dates.iloc[:, 0].apply(lambda x: datetime.fromordinal(datetime(1900, 1, 1).toordinal() + x - 2))
    mat_dates = pd.DataFrame({'Date': mat_dates})

    mat_series_names = mat_file_data['updatedInstruments']
    mat_series_names = pd.DataFrame(mat_series_names)
    mat_series_names = mat_series_names.iloc[:, 2].str.get(0)
    mat_series_names = mat_series_names.tolist()
    mat_series_names = mat_series_names[1:]

    mat_data = pd.DataFrame(mat_file_data['dataTable'])
    mat_data.columns = mat_series_names
    mat_dataframe = pd.concat([mat_data, mat_dates], axis=1, sort=True)
    mat_dataframe.set_index('Date', inplace=True)

    mat_dataframe = mat_dataframe[mat_dataframe.index.dayofweek < 5]        # remove weekends
    mat_dataframe = mat_dataframe[mat_dataframe.index.values < model_date]  # remove data after selected date

    return mat_dataframe


def data_frame_from_xlsx(xlsx_file, range_name, hascolnames):
    """ Get a single rectangular region from the specified file.
    range_name can be a standard Excel reference ('Sheet1!A2:B7') or
    refer to a named region ('my_cells')."""
    wb = openpyxl.load_workbook(xlsx_file, data_only=True, read_only=True)
    if '!' in range_name:
        # passed a worksheet!cell reference
        ws_name, reg = range_name.split('!')
        if ws_name.startswith("'") and ws_name.endswith("'"):
            # optionally strip single quotes around sheet name
            ws_name = ws_name[1:-1]
        region = wb[ws_name][reg]
    else:
        # passed a named range; find the cells in the workbook
        full_range = wb.defined_names[range_name]
        if full_range is None:
            raise ValueError(
                'Range "{}" not found in workbook "{}".'.format(range_name, xlsx_file)
            )
        # convert to list
        destinations = list(full_range.destinations)
        if len(destinations) > 1:
            raise ValueError(
                'Range "{}" in workbook "{}" contains more than one region.'
                    .format(range_name, xlsx_file)
            )
        ws, reg = destinations[0]
        # convert to worksheet object
        if isinstance(ws, str):
            ws = wb[ws]
        region = ws[reg]
    df = pd.DataFrame([cell.value for cell in row] for row in region)

    if hascolnames == 1:
        # make first row as column names
        df.columns = df.iloc[0]
        df = df.drop([0], axis=0)
    wb.close()
    return df


def extract_inputs_and_mat_data(model_type, mat_file=None, input_file=None, model_date=None):

    if sys.platform == "linux2":
        file_path = '/domino/datasets/local/matlab_data.csv'
    else:
        file_path = 'S:/Shared/IT/MultiAsset/Data/Arquive/matlabData.mat'
    # if mat_file is None:
    #     print(sys.platform)
    #     if sys.platform == "Linux":
    #
        # else:
        #     file_path = 'S:/Shared/IT/MultiAsset/Data/Arquive/matlabData.mat'

    if input_file is None:
        input_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "arp_dashboard.xlsm"))
    else:
        input_path = input_file

    if model_date is None:
        model_date = np.datetime64(datetime.today())
    else:
        model_date = model_date

    # load data and inputs
    strategy_inputs = data_frame_from_xlsx(input_path, 'rng_' + model_type + '_inputs', 1)
    asset_inputs = data_frame_from_xlsx(input_path, 'rng_' + model_type + '_assets', 1)
    all_data = matfile_to_dataframe(file_path, model_date)

    return strategy_inputs, asset_inputs, all_data
