
import pytest
import pandas as pd


def test_trend_computations():

    data_trend_to_test = pd.read_csv(r"C:\Users\AJ89720\PycharmProjects\assetallocation_arp\tests\assetallocation_arp\models\resources\effect\outputs_to_test\trend_spot_to_test.csv", index_col=0)

    data_trend_origin = pd.read_csv(r"C:\Users\AJ89720\PycharmProjects\assetallocation_arp\tests\assetallocation_arp\models\resources\effect\outputs_origin\trend_spot_origin.csv", index_col=0)

    # Python is very precise regarding the decimals
    # Compare each numbers up to 9 decimals
    data_trend_origin = data_trend_origin.apply(lambda x: round(x, 9))

    pd.testing.assert_frame_equal(data_trend_origin.reset_index(drop=True),
                                  data_trend_to_test.reset_index(drop=True),
                                  check_names=False,
                                  check_dtype=False)
