import datetime
import pandas as pd
from typing import Tuple
from assetallocation_arp.common_libraries.dal_enums.strategy import Name
from assetallocation_arp.data_etl.dal.arp_proc_caller import TimesProcCaller
from assetallocation_arp.data_etl.dal.data_frame_converter import DataFrameConverter

def call_times_proc_caller(fund_name: str, version_strategy: int, date_to: datetime, date_to_sidebar=None) -> \
        Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Call Times proc caller to grab the data from the db
    :param fund_name: name of the current fund (example: f1, f2,...)
    :param version_strategy: version of the current strategy (version1, version2, ...)
    :param date_to_sidebar: date to sidebar
    :return: None
    """

    if date_to_sidebar is not None:
        date_to = datetime.date(date_to_sidebar.year, date_to_sidebar.month, date_to_sidebar.day)
    else:
        date_to = date_to

    apc = TimesProcCaller()

    fs = apc.select_fund_strategy_results(fund_name, Name.times, version_strategy,
                                          business_date_from=datetime.datetime.strptime('01/01/2000',
                                                                                        '%d/%m/%Y').date(),
                                          business_date_to=date_to
                                          )

    positions = DataFrameConverter.fund_strategy_asset_weights_to_df(fs.asset_weights)
    positions.loc[(positions.asset_subcategory == 'Nominal Bond'), 'asset_subcategory'] = 'Fixed Income'
    positions.index = pd.to_datetime(positions['business_date'])
    analytic_df = DataFrameConverter.fund_strategy_asset_analytics_to_df(fs.analytics)

    signals = analytic_df.loc[analytic_df['analytic_subcategory'] == 'momentum']
    signals.index = pd.to_datetime(signals['business_date'])
    returns = analytic_df.loc[analytic_df['analytic_subcategory'] == 'excess return']
    returns.index = pd.to_datetime(returns['business_date'])

    signals.sort_index()
    returns.sort_index()
    positions.sort_index()

    return signals, returns, positions


def call_times_select_all_fund_strategy_result_dates():
    apc = TimesProcCaller()
    return apc.select_all_fund_strategy_result_dates()
