
import pytest
import pandas as pd


@pytest.mark.parametrize('start_date_computations',
                         ['11/01/2000'])
def test_trend_computations(start_date_computations):

    data_trend_spot_to_test = pd.read_csv(r"C:\Users\AJ89720\PycharmProjects\assetallocation_arp\tests\assetallocation_arp\models\resources\effect\trend_spot.csv")
    data_trend_spot_to_test = data_trend_spot_to_test.set_index(data_trend_spot_to_test.Date)
    data_trend_spot_to_test = data_trend_spot_to_test.drop('Date', 1)
    data_trend_spot_to_test = data_trend_spot_to_test[start_date_computations:]

    trend_inputs = {'short_term': 4, 'long_term': 16, 'trend': 'spot'}  # could be Spot or Total Return
    data_trend_spot_origin = obj_import_data.trend_computations(trend_ind=trend_inputs['trend'],
                                                                short_term=trend_inputs['short_term'],
                                                                long_term=trend_inputs['long_term'])
    pd.testing.assert_frame_equal(data_trend_spot_origin,
                                  data_trend_spot_to_test, check_column_type=False, check_names=False, check_dtype=False)
    print()