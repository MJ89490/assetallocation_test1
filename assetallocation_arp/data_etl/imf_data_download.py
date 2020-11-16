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
import locale

IMF_API_BASE_URL = "http://dataservices.imf.org/REST/SDMX_JSON.svc"
local_proxy = 'http://zsvzen:80'
os.environ['http_proxy'] = local_proxy
os.environ['HTTP_PROXY'] = local_proxy
os.environ['https_proxy'] = local_proxy
os.environ['HTTPS_PROXY'] = local_proxy

args = None
log = logging.getLogger(__name__)

# filter those attributes for the columns for eg. if columnname is Subject Descriptor filter for
# 'Inflation, end of period consumer prices'
filter_attributes = {'Subject Descriptor': 'Inflation, end of period consumer prices', 'Units': 'Index'}

# it turns out the xls (url_2014) is in fact a tsv file ...
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw", "imf_data"))

# Specifying the locale of the source

locale.setlocale(locale.LC_NUMERIC, 'English')  # 'English_United States.1252'


# region build the weo data
def build_weo_data(date):
    """WEO is a particular case of 2 datasets provided as Excel files.
    Its URL change according to the release date.
    """
    if date.month < 4:
        year = date.year - 1
        release_number = "02"
        file_base_name = "WEO{month_name}{year}all".format(month_name="Oct", year=year)
    elif 4 <= date.month < 10:
        year = date.year
        release_number = "01"
        file_base_name = "WEO{month_name}{year}all".format(month_name="Apr", year=year)
    else:
        assert date.month >= 10, date
        year = date.year
        release_number = "02"
        file_base_name = "WEO{month_name}{year}all".format(month_name="Oct", year=year)
    return year, release_number, file_base_name


# endregion

# region build the weo url by the dataset code
def build_weo_url_by_dataset_code(date):
    """WEO is a particular case of 2 datasets provided as Excel files.
    Its URL change according to the release date.
    """
    year, release_number, file_base_name = build_weo_data(date)
    base_url = "https://www.imf.org/external/pubs/ft/weo/{year}/{release_number}/weodata/".format(
        release_number=release_number, year=year)
    return {"WEO": "{base_url}{file_base_name}.xls".format(base_url=base_url, file_base_name=file_base_name),
            "WEOAGG": "{base_url}{file_base_name}a.xls".format(base_url=base_url, file_base_name=file_base_name), }


# endregion

# region get the encoding
def get_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result


# endregion

# region get the footer of the csv file
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


# endregion

# region print all the columns in the dataframe
def print_all_columns_in_dataframe(df, number_of_rows=3):
    """
    print all the columns in the dataframe
    :param df: dataframe to be printed
    :param number_of_rows: number of rows to be printed
    :return:
    """
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified
        log.info(df.tail(number_of_rows))


# endregion

# region extract the required fields
def extract_required_fields(downloaded_file, target_dir):
    """
    Extract only those fields required for asset allocation project
    :param downloaded_file: fully downloaded file
    :param target_dir: target directory where the file goes to
    :return:
    """
    file_path = os.path.abspath(os.path.join(target_dir, downloaded_file))
    data_path = os.path.dirname(file_path)

    aa_required_fields = ['Country', 'Subject Descriptor', 'Subject Notes', 'Units', 'Scale',
                          'Country/Series-specific Notes', 'Estimates Start After']
    available_columns = pd.read_csv(file_path, sep="\t", nrows=1).columns.tolist()
    # get last 8 years only
    last_8_years = available_columns[-9:-1]
    aa_required_fields.extend(last_8_years)

    log.info('Starting extraction of data from: %s' % file_path)
    result = get_encoding(file_path)

    imf_required_data = pd.read_csv(file_path, sep="\t", usecols=aa_required_fields, encoding=result['encoding'])
    print_all_columns_in_dataframe(imf_required_data, 4)
    footer = get_footer_of_csv_file(file_path)

    for key, val in filter_attributes.items():
        imf_required_data = imf_required_data.loc[(imf_required_data[key] == val)]

    # write the dataframe to a file TODO later change this to database
    aa_imf_file = os.path.abspath(os.path.join(data_path, f"aa-{downloaded_file}"))
    imf_required_data.to_csv(aa_imf_file, index=False, sep="\t")
    # write the footer separately
    with open(aa_imf_file, "a+") as wp:
        wp.write("\n")
        wp.write(footer)
        wp.write("\n")

    return True


# endregion

# region download weo data from the imf website
def download_weo_data_from_imf_website(date_arg):
    """
    downloads the data from imf weo website
    :param date_arg: date argument in string format, if not given, today's date is taken as input by default
    :return: name of the dataset downloaded
    """
    try:
        date_list = date_arg.split("-")
        date_val = date(year=int(date_list[2]), month=int(date_list[1]), day=int(date_list[0]))
    except IndexError:
        raise Exception("Invalid Input type")

    # get WEO datasets
    weo_url_by_dataset_code = build_weo_url_by_dataset_code(date_val)
    for dataset_code, dataset_url in sorted(weo_url_by_dataset_code.items()):
        log.info('Fetching %r - %s', dataset_code, dataset_url)
        weo_response = requests.get(dataset_url, timeout=200, verify=False)
        dataset_name = os.path.basename(dataset_url)
        dataset_name = dataset_name.split(".")[0] + ".csv"
        file_name = args.target_dir / dataset_name
        with file_name.open("w") as f:
            f.write(weo_response.content.decode('latin1'))
        return dataset_name


# endregion

# region parse the data from the command line
def parser_data():
    """
    set the arguments for the parser
    :return: tuple of arguments (target_dir, date, log)
    """
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('target_dir', type=Path, help='path of target directory containing data as provided by IMF')
    parser.add_argument('--date', type=str,
                        help='date when the imf data is required, it should be in the format dd-mm-yyyy.'
                             ' eg: if you want data for imf oct 2014 enter the date as 01-10-2014')
    parser.add_argument('--log', default='INFO', help='level of logging messages')
    args = parser.parse_args()

    if args.date is None:
        today = date.today()
        args.date = today.strftime("%d-%m-%Y")

    return args.target_dir, args.date, args.log


# endregion

# region scrape the imf data
def scrape_imf_data():
    args_target, args_date, args_log = parser_data()
    numeric_level = getattr(logging, args_log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: {}'.format(args_log))
    logging.basicConfig(format="%(levelname)s:%(name)s:%(asctime)s:%(message)s", level=numeric_level,
                        stream=sys.stdout, )
    logging.getLogger("urllib3").setLevel(logging.INFO)
    # Download IMF WEO datasets.
    log.info("Download IMF WEO Dataset")
    downloaded_file = download_weo_data_from_imf_website(args_date)
    # extract only those fields required for Asset allocation.
    log.info("Extract only those fields required for Assect allocation")
    extract_required_fields(downloaded_file, args_target)

    return 0


# endregion

if __name__ == '__main__':
    sys.exit(scrape_imf_data())
