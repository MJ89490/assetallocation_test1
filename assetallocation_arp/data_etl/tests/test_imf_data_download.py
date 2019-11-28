"""
@author: AJ89720
@email: anais.jeremie@lgim.com
date: 22/11/2019
description: test imf data download file
"""
import pytest
import sys
import os
from assetallocation_arp.data_etl import imf_data_download as imf_data
from datetime import date
from mock import patch

@pytest.mark.parametrize("date_user, expected_year, expected_release_number, expected_file_name",
                          [(date(year=2019, month=11, day=22), 2019, "02", "WEOOct2019all"),
                           (date(year=2019, month=4, day=22), 2019, "01", "WEOApr2019all"),
                           (date(year=2019, month=3, day=2), 2018, "02", "WEOOct2018all"),
                           (date(year=2019, month=1, day=3), 2018, "02", "WEOOct2018all"),
                           (date(year=2019, month=2, day=4), 2018, "02", "WEOOct2018all"),
                           (date(year=2019, month=5, day=10), 2019, "01", "WEOApr2019all")
                           ])
def test_build_weo_data(date_user, expected_year, expected_release_number, expected_file_name):
     """
     :param date_user: str
     :param expected_year: int
     :param expected_release_number: str
     :param expected_file_name: str
     :return: tuple of year, relaease number, file name
     """
     weo_data = imf_data.build_weo_data(date_user)
     data_tuple = (expected_year, expected_release_number, expected_file_name)
     assert weo_data == data_tuple

@pytest.mark.parametrize("date_user, expected_weo_url_dict",
                         [(date(year=2019, month=11, day=22), {"WEO": "https://www.imf.org/external/pubs/ft/weo/2019/02"
                                                                      "/weodata/WEOOct2019all.xls",
                                                               "WEOAGG": "https://www.imf.org/external/pubs/ft/weo/2019"
                                                                         "/02/weodata/WEOOct2019alla.xls"}),
                          (date(year=2019, month=4, day=22),  {"WEO": "https://www.imf.org/external/pubs/ft/weo/2019/01"
                                                                      "/weodata/WEOApr2019all.xls",
                                                               "WEOAGG": "https://www.imf.org/external/pubs/ft/weo/2019"
                                                                         "/01/weodata/WEOApr2019alla.xls"}),
                          (date(year=2019, month=3, day=2),   {"WEO": "https://www.imf.org/external/pubs/ft/weo/2018/02"
                                                                      "/weodata/WEOOct2018all.xls",
                                                               "WEOAGG": "https://www.imf.org/external/pubs/ft/weo/2018"
                                                                         "/02/weodata/WEOOct2018alla.xls"}),
                          (date(year=2019, month=1, day=3),   {"WEO": "https://www.imf.org/external/pubs/ft/weo/2018/02"
                                                                      "/weodata/WEOOct2018all.xls",
                                                               "WEOAGG": "https://www.imf.org/external/pubs/ft/weo/2018"
                                                                         "/02/weodata/WEOOct2018alla.xls"}),
                          (date(year=2019, month=5, day=10),  {"WEO": "https://www.imf.org/external/pubs/ft/weo/2019/01"
                                                                      "/weodata/WEOApr2019all.xls",
                                                               "WEOAGG": "https://www.imf.org/external/pubs/ft/weo/2019"
                                                                         "/01/weodata/WEOApr2019alla.xls"})
                         ])
def test_build_weo_url_by_dataset_code(date_user, expected_weo_url_dict):
    """
    :param date_user: str
    :param expected_weo_url_dict: dict
    :return: dictionary of url
    """
    weo_url = imf_data.build_weo_url_by_dataset_code(date_user)
    assert weo_url == expected_weo_url_dict

@pytest.mark.parametrize("test_args, expected_date",
                         [(["prog", r"C:\Users\AJ89720\PycharmProjects\assetallocation_arp\assetallocation_arp\data\raw"
                            , "--date", "17-11-2019"], "17-11-2019"),
                          (["prog", r"C:\Users\AJ89720\PycharmProjects\assetallocation_arp\assetallocation_arp\data\raw"
                           ], date.today().strftime("%d-%m-%Y"))
                          ])
def test_parser_data(test_args, expected_date):
    """
    :param test_args: list of arguments for the parser (directory to save the files, the date)
    :param expected_date: str
    :return: tuple of target directory, date and log
    """
    expected_target_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "raw"))
    expected_log = "INFO"  # set to default in the parser
    expected_parser_tuple = (expected_target_directory, expected_date, expected_log)

    with patch.object(sys, 'argv', test_args):
        parser = imf_data.parser_data()
        parser_tuple = (os.path.join(parser[0]), parser[1], parser[2])
        assert parser_tuple == expected_parser_tuple

@pytest.mark.parametrize("test_args",
                         [["prog", "--date", "17-11-2019"]])
def test_parse_data_exception(test_args):
    #target_director = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "raw"))
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit) as e:
            assert imf_data.parser_data()
            assert str(e.value) == "usage: prog [-h] [--date DATE] [--log LOG] target_dir " \
                                   "prog: error: the following arguments are required: target_dir"

@pytest.mark.parametrize("date_user, expected_dataset_name",
                         [("17-11-2019",
                           "WEOOct2019all.csv"),
                          ("22-4-2019",
                           "WEOApr2019all.csv"),
                          ("2-3-2019",
                           "WEOOct2018all.csv"),
                          ("3-1-2019",
                           "WEOOct2018all.csv"),
                          ("10-5-2019",
                           "WEOApr2019all.csv")
                         ])
def test_download_weo_data_from_imf_website(date_user, expected_dataset_name):
    """
    :param date_user: str
    :param expected_dataset_name: str
    :return: the name of the csv file we save
    """
    target_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "raw"))
    test_args = ["prog", target_directory]

    with patch.object(sys, 'argv', test_args):
        imf_data.parser_data()
        data_website = imf_data.download_weo_data_from_imf_website(date_user)
        assert data_website == expected_dataset_name

@pytest.mark.parametrize("date_user",
                         ["17-11",
                          "17112019",
                          "@",
                          "word"
                         ])
def test_download_weo_data_from_imf_website_exception(date_user):
    """
    :param date_user: str
    :return: exception raises
    """

    test_args = ["prog", r"C:\Users\AJ89720\PycharmProjects\assetallocation_arp\assetallocation_arp\data\raw",
                 "--date", date_user]

    with patch.object(sys, 'argv', test_args):
        imf_data.parser_data()
        with pytest.raises(Exception) as e:
            assert imf_data.download_weo_data_from_imf_website(date_user)
        assert str(e.value) == "Invalid Input type"








