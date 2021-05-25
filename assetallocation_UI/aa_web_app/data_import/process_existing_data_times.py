import pandas as pd
import datetime as dt

from assetallocation_arp.common_libraries.dal_enums.strategy import Name
from assetallocation_arp.data_etl.dal.arp_proc_caller import TimesProcCaller


class ProcessExistingDataTimes:
    def __init__(self):
        pass

    @staticmethod
    def preprocess_strategy_existing_data(assets, inputs_existing_versions):
        assets_split, inputs_split = assets.split(','), inputs_existing_versions.split(',')
        asset_tmp = []
        inputs_tmp = {}

        for val in range(0, len(assets_split), 5):
            tmp = assets_split[val:val + 5]
            asset_tmp.append(tmp)

        for val in range(0, len(inputs_split), 2):
            tmp = inputs_split[val: val + 2]
            inputs_tmp[tmp[0]] = tmp[1]

        return asset_tmp, inputs_tmp

    @staticmethod
    def check_in_date_to_existing_version(fund_name, version_strategy, selected_date: str) -> bool:
        apc = TimesProcCaller()
        date_to = dt.datetime.strptime(selected_date, '%d/%m/%Y').date()
        result_dates = apc.select_all_fund_strategy_result_dates()
        result_dates = result_dates[(result_dates['fund_name'] == fund_name) & (result_dates['strategy_version'] ==
                                                                                version_strategy)]
        return dt.date(date_to.year, date_to.month, date_to.day) in result_dates['business_date_to'].values

    @staticmethod
    def receive_data_latest_version_dashboard(fund_name: str):
        apc = TimesProcCaller()
        version_strategy = max(apc.select_strategy_versions(Name.times))
        strategy_weight = apc.select_fund_strategy_weight(fund_name, Name.times, version_strategy)

        return strategy_weight

    @staticmethod
    def receive_data_sidebar_dashboard(fund_name: str, version_strategy: int, all_fund_strategy_result_dates: pd.DataFrame):

        data = all_fund_strategy_result_dates

        select_fund = data.loc[data['fund_name'] == fund_name]
        select_version = select_fund.loc[select_fund['strategy_version'] == version_strategy]
        select_date_to = [d.strftime('%d/%m/%Y') for d in
                          select_version.business_date_to.values.tolist()]

        return select_date_to

    @staticmethod
    def receive_data_existing_versions(fund_name, strategy_version, strategy_weight_user, date_to):
        apc = TimesProcCaller()
        strategy = apc.select_strategy(strategy_version)

        # Inputs
        fund_strategy_weight = apc.select_fund_strategy_weight(fund_name, Name.times, strategy_version)
        strategy_weight = fund_strategy_weight or float(strategy_weight_user)

        inputs_existing_versions_times = [
                                          ['fund_name', fund_name],
                                          ['version', strategy_version],
                                          ['input_date_from_times', '2000S01S01'],
                                          ['input_date_to_times', date_to.replace('/', 'S')],
                                          ['input_strategy_weight_times', strategy_weight],
                                          ['input_time_lag_times', strategy.time_lag_in_days],
                                          ['input_leverage_times', strategy.leverage_type.name],
                                          ['input_vol_window_times', strategy.volatility_window],
                                          ['input_frequency_times', strategy.frequency.name],
                                          ['input_weekday_times', strategy.day_of_week.name],
                                          ['input_signal_one_short_times', strategy.short_signals[0]],
                                          ['input_signal_one_long_times', strategy.long_signals[0]],
                                          ['input_signal_two_short_times', strategy.short_signals[1]],
                                          ['input_signal_two_long_times', strategy.long_signals[1]],
                                          ['input_signal_three_short_times', strategy.short_signals[2]],
                                          ['input_signal_three_long_times', strategy.long_signals[2]]]

        # Assets
        assets_names, assets, signal, future, costs, leverage = [], [], [], [], [], []

        for asset in strategy.asset_inputs:
            assets_names.append(asset.asset_subcategory.name)
            signal.append(asset.signal_ticker)
            future.append(asset.future_ticker)
            costs.append(asset.cost)
            leverage.append(asset.s_leverage)
            assets.append([asset.asset_subcategory.name, asset.signal_ticker, asset.future_ticker, asset.cost,
                           asset.s_leverage])

        return assets, inputs_existing_versions_times


