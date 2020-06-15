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
# 'Inflation, end of period consumer prices'
filter_attributes = {'Subject Descriptor' : 'Inflation, end of period consumer prices', 'Units' : 'Index'}

# it turns out the xls (url_2014) is in fact a tsv file ...
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw", "imf_data"))

# Specifying the locale of the source
import locale

locale.setlocale(locale.LC_NUMERIC, 'English')  # 'English_United States.1252'
#region build the weo data
def build_weo_data(date):
    """WEO is a particular case of 2 datasets provided as Excel files.
    Its URL change according to the release date.
    """
    if date.month < 4:
        year = date.year - 1
        release_number = "02"
        file_base_name = "WEO{month_name}{year}all".format(month_name="Oct", year=year)
    elif date.month >= 4 and date.month < 10:
        year = date.year
        release_number = "01"
        file_base_name = "WEO{month_name}{year}all".format(month_name="Apr", year=year)
    else:
        assert date.month >= 10, date
        year = date.year
        release_number = "02"
        file_base_name = "WEO{month_name}{year}all".format(month_name="Oct", year=year)
    return (year, release_number, file_base_name)
#endregion


#region build the weo url by the dataset code
def build_weo_url_by_dataset_code(date):
    """WEO is a particular case of 2 datasets provided as Excel files.
    Its URL change according to the release date.
    """
    year, release_number, file_base_name = build_weo_data(date)
    base_url = "https://www.imf.org/external/pubs/ft/weo/{year}/{release_number}/weodata/".format(
        release_number=release_number, year=year)
    print(base_url)
    return {
        "WEO": "{base_url}{file_base_name}.xls".format(base_url=base_url, file_base_name=file_base_name),
        "WEOAGG": "{base_url}{file_base_name}a.xls".format(base_url=base_url, file_base_name=file_base_name),
    }
#endregion


#region get the encoding
def get_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return (result)
#endregion


#region get the footer of the csv file
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
    return (footer)
#endregion


#region print all the columns in the dataframe
def print_all_columns_in_dataframe(df, number_of_rows=3):
    """
    print all the columns in the dataframe
    :param df: dataframe to be printed
    :param number_of_rows: number of rows to be printed
    :return:
    """
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified
        log.info(df.tail(number_of_rows))
#endregion

#region extract the required fields
def extract_required_fields(downloaded_file, target_dir):
    """
    Extract only those fields required for asset allocation project
    :param downloaded_file: fully downloaded file
    :param target_dir: target directory where the file goes to
    :return:
    """
    file_path = os.path.abspath(os.path.join(target_dir, downloaded_file))
    data_path = os.path.dirname(file_path)
    "https://www.imf.org/external/Pubs/FT/weo/2006/01/data/weorept.aspx?pr.x=78&pr.y=17&sy=2000&ey=2007&scsm=1&ssd=1&sort=country&ds=.&br=1&c=512%2C668%2C914%2C672%2C612%2C946%2C614%2C137%2C311%2C962%2C213%2C674%2C911%2C676%2C193%2C548%2C122%2C556%2C912%2C678%2C313%2C181%2C419%2C867%2C513%2C682%2C316%2C684%2C913%2C273%2C124%2C868%2C339%2C921%2C638%2C948%2C514%2C943%2C218%2C686%2C963%2C688%2C616%2C518%2C223%2C728%2C516%2C558%2C918%2C138%2C748%2C196%2C618%2C278%2C624%2C692%2C522%2C694%2C622%2C142%2C156%2C449%2C626%2C564%2C628%2C565%2C228%2C283%2C924%2C853%2C233%2C288%2C632%2C293%2C636%2C566%2C634%2C964%2C238%2C182%2C662%2C453%2C960%2C968%2C423%2C922%2C935%2C714%2C128%2C862%2C611%2C135%2C321%2C716%2C243%2C456%2C248%2C722%2C469%2C942%2C253%2C718%2C642%2C724%2C643%2C576%2C939%2C936%2C644%2C961%2C819%2C813%2C172%2C199%2C132%2C733%2C646%2C184%2C648%2C524%2C915%2C361%2C134%2C362%2C652%2C364%2C174%2C732%2C328%2C366%2C258%2C734%2C656%2C144%2C654%2C146%2C336%2C463%2C263%2C528%2C268%2C923%2C532%2C738%2C944%2C578%2C176%2C537%2C534%2C742%2C536%2C866%2C429%2C369%2C433%2C744%2C178%2C186%2C436%2C925%2C136%2C869%2C343%2C746%2C158%2C926%2C439%2C466%2C916%2C112%2C664%2C111%2C826%2C298%2C542%2C927%2C967%2C846%2C443%2C299%2C917%2C582%2C544%2C474%2C941%2C754%2C446%2C698%2C666&s=PCPIPCH&grp=0&a="
    "https://www.imf.org/external/pubs/ft/weo/2019/01/weodata/weorept.aspx?pr.x=89&pr.y=10&sy=2017&ey=2024&scsm=1&ssd=1&sort=country&ds=.&br=1&c=512%2C668%2C914%2C672%2C612%2C946%2C614%2C137%2C311%2C546%2C213%2C674%2C911%2C676%2C314%2C548%2C193%2C556%2C122%2C678%2C912%2C181%2C313%2C867%2C419%2C682%2C513%2C684%2C316%2C273%2C913%2C868%2C124%2C921%2C339%2C948%2C638%2C943%2C514%2C686%2C218%2C688%2C963%2C518%2C616%2C728%2C223%2C836%2C516%2C558%2C918%2C138%2C748%2C196%2C618%2C278%2C624%2C692%2C522%2C694%2C622%2C962%2C156%2C142%2C626%2C449%2C628%2C564%2C228%2C565%2C924%2C283%2C233%2C853%2C632%2C288%2C636%2C293%2C634%2C566%2C238%2C964%2C662%2C182%2C960%2C359%2C423%2C453%2C935%2C968%2C128%2C922%2C611%2C714%2C321%2C862%2C243%2C135%2C248%2C716%2C469%2C456%2C253%2C722%2C642%2C942%2C643%2C718%2C939%2C724%2C734%2C576%2C644%2C936%2C819%2C961%2C172%2C813%2C132%2C726%2C646%2C199%2C648%2C733%2C915%2C184%2C134%2C524%2C652%2C361%2C174%2C362%2C328%2C364%2C258%2C732%2C656%2C366%2C654%2C144%2C336%2C146%2C263%2C463%2C268%2C528%2C532%2C923%2C944%2C738%2C176%2C578%2C534%2C537%2C536%2C742%2C429%2C866%2C433%2C369%2C178%2C744%2C436%2C186%2C136%2C925%2C343%2C869%2C158%2C746%2C439%2C926%2C916%2C466%2C664%2C112%2C826%2C111%2C542%2C298%2C967%2C927%2C443%2C846%2C917%2C299%2C544%2C582%2C941%2C474%2C446%2C754%2C666%2C698&s=PCPIE&grp=0&a="

    "https://www.imf.org/external/pubs/ft/weo/2006/01/weodata/WEOApr2006all.xls"
    "https://www.imf.org/external/pubs/ft/weo/2019/01/weodata/WEOApr2019all.xls"



    # aa_required_fields = ['Country', 'Subject Descriptor', 'Subject Notes', 'Units', 'Scale', 'Country/Series-specific Notes', 'Estimates Start After']
    aa_required_fields = ['Country', 'Subject Descriptor', 'Subject Notes', 'Units']
    available_columns = pd.read_csv(file_path, sep="\t", nrows=1).columns.tolist()
    # get last 8 years only
    last_8_years = available_columns[-9:-1]
    aa_required_fields.extend(last_8_years)

    log.info('Starting extraction of data from: %s' % file_path)
    result = get_encoding(file_path)
    print(available_columns)
    # Dataframe (imf_required_data) with the data and required fields
    imf_required_data = pd.read_csv(file_path, sep="\t", usecols=aa_required_fields, encoding=result['encoding'])
    print_all_columns_in_dataframe(imf_required_data, 4)
    footer = get_footer_of_csv_file(file_path)

    # Select only the data for 'Inflation, end of period consumer price'
    # key_sentence = ' Annual percentages of end of period consumer prices are year-on-year changes.'
    key_sentence = 'Inflation, end of period consumer prices'

    imf_required_data_inflation = imf_required_data.loc[imf_required_data['Subject Descriptor'] == key_sentence]
    imf_required_data_inflation = imf_required_data_inflation.loc[(imf_required_data_inflation['Units'] == 'Annual percent change') | (imf_required_data_inflation['Units'] == 'Percent change')]


    # write the dataFrame to a file
    aa_imf_file = os.path.abspath(os.path.join(data_path, f"aa-{downloaded_file}"))
    data_imf_file = os.path.abspath(os.path.join(data_path, f"data_imf_{downloaded_file}"))
    imf_required_data_inflation.to_csv(data_imf_file, index=False)
    imf_required_data.to_csv(aa_imf_file, index=False, sep="\t")
    # write the footer separately
    with open(aa_imf_file, "a+") as wp:
        wp.write("\n")
        wp.write(footer)
        wp.write("\n")

    return True
#endregion

#region download weo data from the imf website
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
        dataset_name = dataset_name.split(".")[0]+".csv"
        file_name = args.target_dir / dataset_name
        with (file_name).open("w") as f:
            f.write(weo_response.content.decode('latin1'))
        return(dataset_name)
#endregion

#region parse the data from the command line
def parser_data():
    """
    set the arguments for the parser
    :return: tuple of arguments (target_dir, date, log)
    """
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('target_dir', type=Path, help='path of target directory containing data as provided by IMF')
    parser.add_argument('--date', type=str, help='date when the imf data is required, it should be in the format dd-mm-yyyy.'
                                                 ' eg: if you want data for imf oct 2014 enter the date as 01-10-2014')
    parser.add_argument('--log', default='INFO', help='level of logging messages')
    args = parser.parse_args()

    date_value = '06-10-2015'
    args.date = date_value
    print(args.date)
    # if args.date is None:
    #     today = date.today()
    #     args.date = today.strftime("%d-%m-%Y")

    return args.target_dir, args.date, args.log
#endregion

#region scrape the imf data
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
    # extract only those fields required for Asset allocation.
    log.info("Extract only those fields required for Asset allocation")
    print(log)
    extract_required_fields(downloaded_file, args_target)

    return 0
#endregion

if __name__ == '__main__':
    sys.exit(scrape_imf_data())
