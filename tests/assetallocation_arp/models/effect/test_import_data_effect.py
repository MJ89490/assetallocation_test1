import os
import pytest
import pandas as pd
from assetallocation_arp.data_etl.inputs_effect.import_data_effect import ImportDataEffect
from assetallocation_arp.common_libraries.dal_enums.strategy import Frequency, DayOfWeek


@pytest.mark.parametrize("last_date_origin, last_date_expected, freq",
                         [("15-09-2020", "22-09-2020", Frequency.weekly),
                          ("16-09-2020", "23-09-2020", Frequency.weekly),
                          ("25-09-2020", "02-10-2020", Frequency.weekly),
                          ("24-09-2020", "25-09-2020", Frequency.daily),
                          ("25-09-2020", "28-09-2020", Frequency.daily),
                          ("30-09-2020", "01-10-2020", Frequency.daily),
                          ("30-09-2020", "30-10-2020", Frequency.monthly),
                          ("31-12-2020", "29-01-2021", Frequency.monthly)])
def test_add_next_date(last_date_origin, last_date_expected, freq):
    all_data = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "all_date.csv")), sep=',', engine='python')
    all_data = all_data.set_index(pd.to_datetime(all_data.Date, format='%Y-%m-%d'))
    del all_data['Date']

    obj_import_data = ImportDataEffect(pd.to_datetime('23/09/2020', format='%d/%m/%Y'), Frequency.weekly, DayOfWeek.WED, all_data)

    last_date = obj_import_data.add_next_date(freq, pd.to_datetime(last_date_origin, format='%d-%m-%Y'))
    assert last_date == pd.to_datetime(last_date_expected, format='%d-%m-%Y')
