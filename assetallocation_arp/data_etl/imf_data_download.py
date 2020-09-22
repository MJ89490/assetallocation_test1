"""Download IMF data
Documentation:
"""

import argparse
import logging
import os
import sys
import requests
import pandas as pd
import chardet

from datetime import date
from pathlib import Path

IMF_API_BASE_URL = "http://dataservices.imf.org/REST/SDMX_JSON.svc"
local_proxy = 'http://zsvzen:80'
os.environ['http_proxy'] = local_proxy
os.environ['HTTP_PROXY'] = local_proxy
os.environ['https_proxy'] = local_proxy
os.environ['HTTPS_PROXY'] = local_proxy

args = None
log = logging.getLogger(__name__)

# filter those attributes for the columns for eg. if columnname is Subject Descriptor filter for
filter_attributes = {'Subject Descriptor': 'Inflation, end of period consumer prices', 'Units': 'Index'}

# it turns out the xls (url_2014) is in fact a tsv file ...
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "data", "imf_data"))

# Specifying the locale of the source
import locale

locale.setlocale(locale.LC_NUMERIC, 'English')  # 'English_United States.1252'


def build_weo_data(date_value):
    """WEO is a particular case of 2 datasets provided as Excel files.
    Its URL change according to the release date.
    """
    if date_value.month < 4:
        year = date_value.year - 1
        release_number = "02"
        file_base_name = "WEO{month_name}{year}all".format(month_name="Oct", year=year)
    elif date_value.month == 9:
        year = date_value.year
        release_number = "02"
        file_base_name = "WEO{month_name}{year}all".format(month_name="Sep", year=year)
    elif date_value.month >= 4 and date_value.month < 9:
        year = date_value.year
        release_number = "01"
        file_base_name = "WEO{month_name}{year}all".format(month_name="Apr", year=year)
    else:
        assert date_value.month >= 10, date_value
        year = date_value.year
        release_number = "02"
        file_base_name = "WEO{month_name}{year}all".format(month_name="Oct", year=year)

    return year, release_number, file_base_name


def build_weo_url_by_dataset_code(date_value):
    """
    WEO is a particular case of 2 datasets provided as Excel files.
    Its URL change according to the release date.
    WEO = data per country
    WEOAGG = data per country group
    """
    year, release_number, file_base_name = build_weo_data(date_value=date_value)
    base_url = "https://www.imf.org/external/pubs/ft/weo/{year}/{release_number}/weodata/".format(
        release_number=release_number, year=year)

    return {
            "WEO": "{base_url}{file_base_name}.xls".format(base_url=base_url, file_base_name=file_base_name),
            "WEOAGG": "{base_url}{file_base_name}a.xls".format(base_url=base_url, file_base_name=file_base_name),
           }


def get_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())

    return result


def get_footer_of_csv_file(file_path):
    """
    IMF weo data file contains a fppter with name of the dataset and year month
    :param file_path:
    :return:
    """
    with open(file_path, 'rb') as f:
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
        footer = f.readline().decode()
    return footer


def print_all_columns_in_dataframe(df, number_of_rows=3):
    """
    print all the columns in the dataframe
    :param df: dataframe to be printed
    :param number_of_rows: number of rows to be printed
    :return:
    """
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified
        log.info(df.tail(number_of_rows))


def extract_required_fields(downloaded_file, target_dir):
    """
    Extract only those fields required for asset allocation project
    :param downloaded_file: fully downloaded files for per country and group countrry
    :param target_dir: target directory where the file goes to
    :return:
    """

    INFLATION_KEY = 'Inflation, end of period consumer prices'

    # ----------------------------------- Country group data -----------------------------------
    country_group_file_path = os.path.abspath(os.path.join(target_dir, downloaded_file[1]))
    country_group_data_path = os.path.dirname(country_group_file_path)
    country_group_fields = ['Country Group Name', 'Subject Descriptor']
    country_group_columns = pd.read_csv(country_group_file_path, sep="\t", nrows=1).columns.tolist()

    # Get last 8 years only
    last_8_years = country_group_columns[-9:-1]
    country_group_fields.extend(last_8_years)

    log.info('Starting extraction of data from: %s' % country_group_file_path)
    country_group_result = get_encoding(country_group_file_path)

    country_group_data = pd.read_csv(country_group_file_path, sep="\t", usecols=country_group_fields, encoding=country_group_result['encoding'])
    print_all_columns_in_dataframe(country_group_data, 4)
    country_group_footer = get_footer_of_csv_file(country_group_file_path)

    # Write the footer separately
    with open(country_group_file_path, "a+") as wp:
        wp.write("\n")
        wp.write(country_group_footer)
        wp.write("\n")

    # Select only 'Inflation, end of period consumer price' and 'Euro area' in country group data
    country_key = 'Euro area'

    # Remove whitespaces in the Country Group Name
    country_group_data['Country Group Name'] = country_group_data['Country Group Name'].str.strip()

    country_group_inflation = country_group_data.loc[(country_group_data['Subject Descriptor'] == INFLATION_KEY) & (country_group_data['Country Group Name'] == country_key)]

    country_group_imf_file = os.path.abspath(os.path.join(country_group_data_path, f"data_imf_eur_{downloaded_file[1]}"))
    country_group_inflation.to_csv(country_group_imf_file, index=False)

    # ----------------------------------- Country data -----------------------------------
    country_file_path = os.path.abspath(os.path.join(target_dir, downloaded_file[0]))
    country_data_path = os.path.dirname(country_file_path)
    country_fields = ['Country', 'Subject Descriptor', 'Subject Notes', 'Units']
    available_columns = pd.read_csv(country_file_path, sep="\t", nrows=1).columns.tolist()

    # Get last 8 years only
    last_8_years = available_columns[-9:-1]
    country_fields.extend(last_8_years)

    log.info('Starting extraction of data from: %s' % country_file_path)
    result = get_encoding(country_file_path)

    country_data = pd.read_csv(country_file_path, sep="\t", usecols=country_fields, encoding=result['encoding'])
    print_all_columns_in_dataframe(country_data, 4)
    country_footer = get_footer_of_csv_file(country_file_path)

    # Write the footer separately
    with open(country_file_path, "a+") as wp:
        wp.write("\n")
        wp.write(country_footer)
        wp.write("\n")

    # Select only the data for 'Inflation, end of period consumer price'
    country_inflation = country_data.loc[country_data['Subject Descriptor'] == INFLATION_KEY]
    country_inflation = country_inflation.loc[
        (country_inflation['Units'] == 'Annual percent change') | (country_inflation['Units'] == 'Percent change')]

    country_imf_file = os.path.abspath(os.path.join(country_data_path, f"data_imf_{downloaded_file[0]}"))
    country_inflation.to_csv(country_imf_file, index=False)

    return True


def download_weo_data_from_imf_website(date_arg):
    """
    downloads the data from imf weo website
    :param date_arg: date argument in string format, if not given, today's date is taken as input by default
    :return: name of the dataset downloaded
    """
    try:
        date_list = date_arg.split("-")
        date_value = date(year=int(date_list[2]), month=int(date_list[1]), day=int(date_list[0]))
    except IndexError:
        raise Exception("Invalid Input type")

    # Get WEO datasets
    weo_url_by_dataset_code = build_weo_url_by_dataset_code(date_value=date_value)

    dataset_names = []

    # Get the data per country
    for dataset_code, dataset_url in sorted(weo_url_by_dataset_code.items()):
        log.info('Fetching %r - %s', dataset_code, dataset_url)
        weo_response = requests.get(dataset_url, timeout=200, verify=False)
        dataset_name = os.path.basename(dataset_url)
        dataset_name = dataset_name.split(".")[0]+".csv"
        dataset_names.append(dataset_name)
        file_name = args.target_dir / dataset_name
        with (file_name).open("w") as f:
            f.write(weo_response.content.decode('latin1'))

    return dataset_names


def parser_data():
    """
    set the arguments for the parser
    :return: tuple of arguments (target_dir, date, log)
    """
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('--target_dir', type=Path, help='path of target directory containing data as provided by IMF')
    parser.add_argument('--date', type=str, help='date when the imf data is required, it should be in the format dd-mm-yyyy.'
                                                 ' eg: if you want data for imf oct 2014 enter the date as 01-10-2014')
    parser.add_argument('--log', default='INFO', help='level of logging messages')
    args = parser.parse_args()
    target_value = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data_effect', 'data_imf'))
    args.target_dir = Path(target_value)

    if args.date is None:
        today = date.today()
        args.date = today.strftime("%d-%m-%Y")

    return args.target_dir, args.date, args.log


def scrape_imf_data():
    args_target, args_date, args_log = parser_data()
    numeric_level = getattr(logging, args_log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: {}'.format(args_log))
    logging.basicConfig(
        format="%(levelname)s:%(name)s:%(asctime)s:%(message)s",
        level=numeric_level,
        stream=sys.stdout,
    )
    logging.getLogger("urllib3").setLevel(logging.INFO)
    # Download IMF WEO datasets.
    log.info("Download IMF WEO Dataset")
    downloaded_file = download_weo_data_from_imf_website(args_date)
    # Extract only those fields required for Asset allocation.
    log.info("Extract only those fields required for Asset allocation")
    print(log)
    extract_required_fields(downloaded_file, args_target)

    return 0


if __name__ == '__main__':
    sys.exit(scrape_imf_data())
