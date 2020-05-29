from data_etl.import_data_times import extract_inputs_and_mat_data as data_matlab_effect
from common_libraries.models_names import Models

import pandas as pd


class ImportDataEffect:

    def __init__(self):
        self.data_currencies = pd.DataFrame()

    def import_data_matlab(self):
        self.data_currencies = data_matlab_effect(model_type=Models.effect.name, mat_file=None,
                                                  input_file=None, date=None)