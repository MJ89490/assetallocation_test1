import os
import pytest
import pandas as pd
from assetallocation_arp.data_etl.inputs_effect.import_data_effect import ImportDataEffect

path_all_data = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "all_date.csv"))
all_data = pd.read_csv(path_all_data, sep=',', engine='python')

end_date_mat, start_date_mat, frequency, signal_day_mat, all_data = '23/09/2020', '06/01/1999', 'weekly', 'WED', all_data

obj_import_data_effect = ImportDataEffect(end_date_mat, start_date_mat, frequency, signal_day_mat, all_data)


@pytest.mark.parametrize("last_date_origin, last_date_expected, freq",
                         [("15-09-2020", "22-09-2020", "weekly"),
                          ("16-09-2020", "23-09-2020", "weekly"),
                          ("25-09-2020", "02-10-2020", "weekly"),
                          ("24-09-2020", "25-09-2020", "daily"),
                          ("25-09-2020", "28-09-2020", "daily"),
                          ("30-09-2020", "01-10-2020", "daily"),
                          ("30-09-2020", "30-10-2020", "monthly"),
                          ("31-12-2020", "29-01-2021", "monthly")])
def test_add_next_date(last_date_origin, last_date_expected, freq):
    last_date = obj_import_data_effect.add_next_date(freq, pd.to_datetime(last_date_origin, format='%d-%m-%Y'))
    assert last_date == pd.to_datetime(last_date_expected, format='%d-%m-%Y')
