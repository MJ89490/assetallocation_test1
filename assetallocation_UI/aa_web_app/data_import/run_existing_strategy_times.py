import datetime as dt

from assetallocation_UI.aa_web_app.service.strategy import run_strategy
from assetallocation_arp.data_etl.dal.arp_proc_caller import TimesProcCaller


def run_existing_strategy(inputs_existing_versions_times, username):
    apc = TimesProcCaller()
    strategy = apc.select_strategy(inputs_existing_versions_times['version'])

    fund_strategy = run_strategy(inputs_existing_versions_times['fund_name'],
                                 float(inputs_existing_versions_times['input_strategy_weight_times']),
                                 strategy,
                                 username,
                                 dt.datetime.strptime(
                                     inputs_existing_versions_times['input_date_from_times'].replace('S', '/'),
                                     '%Y/%m/%d').date(),
                                 dt.datetime.strptime(
                                     inputs_existing_versions_times['input_date_to_times'].replace('S', '/'),
                                     '%d/%m/%Y').date(),
                                 is_new_strategy=False
                                 )

    return fund_strategy
