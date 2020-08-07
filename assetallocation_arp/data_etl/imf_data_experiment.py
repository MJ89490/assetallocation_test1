import os
import requests
import pandas as pd
import chardet
# Specifying the locale of the source
import locale


BASE_IMF_URL = "'http://www.imf.org/external/pubs/ft/weo/"

data_needed_years = ['2014']
data_needed_months = []
url_2014 = 'http://www.imf.org/external/pubs/ft/weo/2014/01/weodata/WEOApr2014all.xls'
url_2015 = 'http://www.imf.org/external/pubs/ft/weo/2015/01/weodata/WEOApr2015all.xls'
url_2019_oct = 'http://www.imf.org/external/pubs/ft/weo/2019/02/weodata/WEOOct2019all.xls'
url_2019_apr = 'http://www.imf.org/external/pubs/ft/weo/2019/02/weodata/WEOApr2019all.xls'

url = url_2019_oct

# filter those attributes for the columns for eg. if columnname is Subject Descriptor filter for
# 'Inflation, end of period consumer prices'
filter_attributes = {'Subject Descriptor': 'Inflation, end of period consumer prices', 'Units': 'Index'}

# it turns out the xls (url_2014) is in fact a tsv file ...
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw"))
fp_2014 = 'imf-weo-2014-apr.tsv'
fp_2015 = 'imf-weo-2015-apr.tsv'
fp = fp_2015

locale.setlocale(locale.LC_NUMERIC, 'English')  # 'English_United States.1252'

FILE_PATH = os.path.abspath(os.path.join(root_path, fp))
DATA_PATH = os.path.dirname(FILE_PATH)
local_proxy = 'http://zsvzen:80'
os.environ['http_proxy'] = local_proxy
os.environ['HTTP_PROXY'] = local_proxy
os.environ['https_proxy'] = local_proxy
os.environ['HTTPS_PROXY'] = local_proxy


def download_weo_data_from_imf_website():
    print(DATA_PATH)
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
    print('Source database downloaded to: %s' % FILE_PATH)

    session = requests.Session()
    resp = session.get(url, timeout=200, verify=False)
    with open(FILE_PATH, "wb") as output:
        output.write(resp.content)
    print('Source database downloaded to: %s' % FILE_PATH)
    session.close()


def get_concoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())

    return result


def get_footer_of_csv_file(file_path):
    with open(file_path, 'rb') as f:
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
        footer = f.readline().decode()
    return footer


def print_all_columns_in_dataframe(df, number_of_rows=3):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified
        print(df.tail(number_of_rows))


def extract_required_fields():
    aa_required_fields = ['Country', 'Subject Descriptor', 'Subject Notes', 'Units', 'Scale',
                          'Country/Series-specific Notes', 'Estimates Start After']
    aa_required_years = ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
    aa_required_fields.extend(aa_required_years)
    print('Starting extraction of data from: %s' % FILE_PATH)
    result = get_concoding(FILE_PATH)
    imf_required_data = pd.read_csv(FILE_PATH, sep="\t", usecols=aa_required_fields, encoding=result['encoding'])
    print(imf_required_data.columns)
    print_all_columns_in_dataframe(imf_required_data, 4)
    footer = get_footer_of_csv_file(FILE_PATH)

    for key, val in filter_attributes.items():
        imf_required_data = imf_required_data.loc[(imf_required_data[key] == val)]

    # write the dataframe to a file TODO later change this to database
    aa_imf_file = os.path.abspath(os.path.join(DATA_PATH, f"aa-{fp}"))
    imf_required_data.to_csv(aa_imf_file, index=False, sep=",")
    # write the footer separately
    with open(aa_imf_file, "a+") as wp:
        wp.write("\n")
        wp.write(footer)
        wp.write("\n")

    return True


def scrape_imf_data():
    download_weo_data_from_imf_website()
    extract_required_fields()

# check_indicators()


if __name__ == "__main__":
    scrape_imf_data()
