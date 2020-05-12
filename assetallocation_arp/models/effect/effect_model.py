"""
Created on 12/05/2020
@author: AJ89720
"""

from data_etl.import_data_times import extract_inputs_and_mat_data as data_matlab_effect
from common_libraries.models_names import Models
import pandas as pd

class ImportDataEffect:

    def __init__(self):
        self.data_currencies = pd.DataFrame()

    def import_data_matlab(self):
        self.data_currencies = data_matlab_effect(model_type=Models.effect.name, mat_file=None,input_file=None,model_date=None)

class DataProcessingEffect:

    def __init__(self):
        pass

    #todo : do the same as TIMES model

class CurrencyComputations:
    def __init__(self):
        pass
        # Carry
        # Trend
        # Combo
        # Return
        # Return
        # Spot
        # Spot
        # Inflation
        # Inflation

    #properties = inputs?

if __name__=="__main__":
    obj_import_data = ImportDataEffect()
    obj_import_data.import_data_matlab()

