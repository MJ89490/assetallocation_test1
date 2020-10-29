import pdblp
import xlwings as xw
import numpy as np
from datetime import datetime
from assetallocation_arp.data_etl import import_data_from_excel_matlab as gd
import pandas


def get_bloomberg_data(tickers, fields, start_date, end_date):
    bbg = pdblp.BCon(debug=True, port=8194, timeout=5000)
    bbg.start()
    elms = [("periodicitySelection", "DAILY"), ("nonTradingDayFillOption", "ALL_CALENDAR_DAYS"),
            ("nonTradingDayFillMethod", "PREVIOUS_VALUE")]
    bbg_data = bbg.bdh(tickers, fields, start_date, end_date, elms, ovrds=[], longdata=False)
    bbg.stop()
    return bbg_data


def main(file):
    inputs = gd.data_frame_from_xlsx(file, "rng_assets_list", 1)
    tickers = inputs['Ticker']
    fields = inputs.Field.unique()
    start_date = inputs['HISTORY_START_DT']
    end_date = np.datetime64(datetime.today())

    return inputs


if __name__ == "__main__":
    main(file=r'H:\Python\assetallocation_arp\assetallocation_arp\arp_dashboard.xlsm')

