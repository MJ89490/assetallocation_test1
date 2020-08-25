from typing import List, Union, Optional
from datetime import datetime
from os import environ
from json import loads

from assetallocation_arp.data_etl.dal.db import Db
from assetallocation_arp.data_etl.dal.data_models.strategy import Times, Effect
from assetallocation_arp.data_etl.dal.data_models.fund_strategy import (FundStrategy, FundStrategyAssetAnalytic,
                                                                        FundStrategyAssetWeight)
from assetallocation_arp.data_etl.dal.type_converter import ArpTypeConverter
from assetallocation_arp.data_etl.dal.data_models.asset import TimesAssetInput, EffectAsset, Asset
from common_libraries.dal_enums.strategy import Name
from assetallocation_arp.data_etl.dal.data_models.app_user import AppUser


class ArpProcCaller(Db):
    def __init__(self):
        """ArpProcCaller class to interact with ARP database through calling stored procedures"""
        config = loads(environ.get('DATABASE', '{}'))
        user = config.get('USER')
        password = config.get('PASSWORD')
        host = config.get('HOST')
        port = config.get('PORT')
        database = config.get('DATABASE')

        super().__init__(f'postgresql://{user}:{password}@{host}:{port}/{database}')

    def insert_app_user(self, app_user: AppUser) -> bool:
        self.call_proc('arp.insert_app_user', [app_user.user_id, app_user.name, app_user.email])
        return True

    def insert_effect(self, effect: Effect, user_id: str) -> int:
        """Insert data from an instance of Effect into database"""
        e_version = self._insert_effect_strategy(effect, user_id)
        if effect.assets:
            self._insert_effect_assets(e_version, effect.assets)

        return e_version

    def _insert_effect_strategy(self, effect: Effect, user_id: str) -> int:
        """Insert data from an instance of Effect into database"""
        res = self.call_proc('arp.insert_effect_strategy',
                             [effect.description, user_id, effect.carry_type.name, effect.closing_threshold,
                              effect.cost, effect.day_of_week.value, effect.frequency.name, effect.include_shorts,
                              effect.inflation_lag_interval, effect.interest_rate_cut_off_long,
                              effect.interest_rate_cut_off_short, effect.moving_average_long_term,
                              effect.moving_average_short_term, effect.is_realtime_inflation_forecast,
                              effect.trend_indicator.name])

        return res[0]['e_version']

    def _insert_effect_assets(self, effect_version: int, effect_assets: List[EffectAsset]) -> bool:
        """Insert asset data for a version of Effect"""
        effect_assets = ArpTypeConverter.effect_assets_to_composite(effect_assets)
        res = self.call_proc('arp.insert_effect_assets', [effect_version, effect_assets])
        asset_ids = res[0].get('asset_ids')
        return bool(asset_ids)

    def select_effect(self, effect_version) -> Optional[Effect]:
        """Select strategy and asset data for a version of effect"""
        effect = self._select_effect_strategy(effect_version)

        if effect is not None:
            effect.assets = self._select_effect_assets(effect_version)

        return effect

    def _select_effect_strategy(self, effect_version) -> Optional[Effect]:
        """Select strategy data for a version of Effect"""
        res = self.call_proc('arp.select_effect_strategy', [effect_version])
        if not res:
            return

        row = res[0]
        e = Effect(row['carry_type'], row['closing_threshold'], row['cost'], row['day_of_week'], row['frequency'],
                   row['include_shorts'], -ArpTypeConverter.month_interval_to_int(row['inflation_lag']),
                   row['interest_rate_cut_off_long'], row['interest_rate_cut_off_short'],
                   row['moving_average_long_term'], row['moving_average_short_term'],
                   row['is_realtime_inflation_forecast'], row['trend_indicator'])
        e.version = effect_version
        e.description = row['description']
        return e

    def _select_effect_assets(self, effect_version) -> Optional[List[EffectAsset]]:
        """Select asset data for a version of times"""
        res = self.call_proc('arp.select_times_assets', [effect_version])

        if not res:
            return

        effect_assets = []
        for r in res:
            e = EffectAsset(r['ticker'], r['category'], r['country'], r['currency'], r['name'], r['asset_type'],
                           r['ndf_code'], r['spot_code'], r['position_size'])
            e.description = r['description']
            e.is_tr = r['is_tr']

            effect_assets.append(e)

        return effect_assets

    def select_effect_with_asset_analytics(self, effect_version, business_datetime) -> Optional[Effect]:
        """Select strategy, assets and asset analytics data for a version of effect, as at business_datetime"""
        effect = self._select_effect_strategy(effect_version)

        if effect is not None:
            effect.assets = self.select_effect_assets_with_analytics(effect_version, business_datetime)

        return effect

    def select_effect_assets_with_analytics(self, effect_version, business_datetime) -> Optional[List[EffectAsset]]:
        """Select assets and asset analytics data for a version of times, as at business_datetime"""
        res = self.call_proc('arp.select_effect_assets_with_analytics', [effect_version, business_datetime])

        if not res:
            return

        effect_assets = []
        for r in res:
            e = EffectAsset(r['ticker'], r['category'], r['country'], r['currency'], r['name'], r['asset_type'],
                            r['ndf_code'], r['spot_code'], r['position_size'])
            e.description = r['description']
            e.is_tr = r['is_tr']
            e.asset_analytics = ArpTypeConverter.asset_analytics_str_to_objects(r['ticker'], r['asset_analytics'])

            effect_assets.append(e)

        return effect_assets

    def insert_times(self, times: Times, user_id: str) -> int:
        """Insert data from an instance of Times into database. Return strategy version."""
        t_version = self._insert_times_strategy(times, user_id)
        if times.asset_inputs:
            self._insert_times_assets(t_version, times.asset_inputs)

        return t_version

    def _insert_times_strategy(self, times: Times, user_id: str) -> int:
        """Insert data from an instance of Times into database"""
        res = self.call_proc('arp.insert_times_strategy',
                             [times.description, user_id, times.time_lag_interval, times.leverage_type.name,
                              times.volatility_window, times.short_signals, times.long_signals, times.frequency.name,
                              times.day_of_week.value])

        return res[0]['t_version']

    def _insert_times_assets(self, times_version: int, times_assets: List[TimesAssetInput]) -> bool:
        """Insert asset data for a version of times"""
        times_assets = ArpTypeConverter.times_assets_to_composite(times_assets)
        self.call_proc('arp.insert_times_assets', [times_version, times_assets])
        return True

    def select_times(self, times_version) -> Optional[Times]:
        """Select strategy and asset data for a version of times"""
        times = self._select_times_strategy(times_version)

        if times is not None:
            times.assets = self._select_times_assets(times_version)

        return times

    def _select_times_strategy(self, times_version) -> Optional[Times]:
        """Select strategy data for a version of times"""
        res = self.call_proc('arp.select_times_strategy', [times_version])
        if not res:
            return

        row = res[0]
        t = Times(row['day_of_week'], row['frequency'], row['leverage_type'], row['long_signals'], row['short_signals'],
                  -ArpTypeConverter.month_interval_to_int(row['time_lag']), row['volatility_window'])
        t.version = times_version
        t.description = row['description']
        return t

    def _select_times_assets(self, times_version) -> Optional[List[TimesAssetInput]]:
        """Select asset data for a version of times"""
        res = self.call_proc('arp.select_times_assets', [times_version])

        if not res:
            return

        times_assets = []
        for r in res:
            t = self._construct_times_asset_input(r)

            times_assets.append(t)

        return times_assets

    def select_times_with_asset_analytics(self, times_version, business_datetime) -> Optional[Times]:
        """Select strategy, assets and asset analytics data for a version of times, as at business_datetime"""
        times = self._select_times_strategy(times_version)

        if times is not None:
            times.assets = self.select_times_assets_with_analytics(times_version, business_datetime)

        return times

    def select_times_assets_with_analytics(self, times_version, business_datetime) -> Optional[List[TimesAssetInput]]:
        """Select assets and asset analytics data for a version of times, as at business_datetime"""
        res = self.call_proc('arp.select_times_assets_with_analytics', [times_version, business_datetime])

        if not res:
            return

        times_assets = []
        for r in res:
            t = self._construct_times_asset_input(r)

            t.signal_asset.asset_analytics = ArpTypeConverter.asset_analytics_str_to_objects(r['signal_ticker'],
                                                                                             r['signal_asset_analytics'])
            t.future_asset.asset_analytics = ArpTypeConverter.asset_analytics_str_to_objects(r['future_ticker'],
                                                                                             r['future_asset_analytics'])

            times_assets.append(t)

        return times_assets

    @staticmethod
    def _construct_times_asset_input(row) -> TimesAssetInput:
        t = TimesAssetInput(row['s_leverage'], row['signal_ticker'], row['future_ticker'], row['cost'])
        t.signal_asset = Asset(row['signal_ticker'], row['signal_name'])
        t.future_asset = Asset(row['future_ticker'], row['future_name'])
        return t

    def insert_fund_strategy_results(self, fund_strategy: FundStrategy, user_id: str) -> bool:
        """Insert data from an instance of FundStrategy into database"""
        ticker_weights = ArpTypeConverter.weights_to_composite(fund_strategy.asset_weights)
        ticker_analytics = ArpTypeConverter.analytics_to_composite(fund_strategy.asset_analytics)

        res = self.call_proc('arp.insert_fund_strategy_results',
                             [fund_strategy.fund_name, fund_strategy.output_is_saved,
                              fund_strategy.strategy_name.name, fund_strategy.strategy_version, fund_strategy.weight,
                              user_id, fund_strategy.python_code_version, ticker_weights, ticker_analytics])
        fund_strategy_id = res[0].get('fund_strategy_id')

        return fund_strategy_id is not None

    def select_fund_strategy_results(self, fund_name: str, strategy_name: Union[str, Name],
                                     business_datetime: datetime = datetime.today(),
                                     system_datetime: datetime = datetime.today()) -> Optional[FundStrategy]:
        """Select the most recent FundStrategy data for a strategy as at business_datetime and system_datetime"""
        strategy_name = strategy_name.name if isinstance(strategy_name, Name) else Name[strategy_name].name

        res = self.call_proc('arp.select_fund_strategy_results',
                             [fund_name, strategy_name, business_datetime, system_datetime])

        if not res:
            return

        fund_strategy = FundStrategy(fund_name, strategy_name, res[0]['strategy_version'], res[0]['weight'])
        fund_strategy.business_datetime = res[0]['business_datetime']
        fund_strategy.output_is_saved = res[0]['output_is_saved']
        fund_strategy.python_code_version = res[0]['python_code_version']

        for row in res:
            aw = FundStrategyAssetWeight(row['asset_ticker'], row['strategy_weight'])
            aw.implemented_weight = row['implemented_weight']
            fund_strategy.add_fund_strategy_asset_weight(aw)

            # asset_analytics is a str of the format
            # '{"(category1,subcategory1,valu1e)",..."(categoryN,subcategoryN,valueN)"}'
            for i in row['asset_analytics'][2:-2].split('","'):
                category, subcategory, value = (i[1: -1].split(','))
                value = float(value)
                fund_strategy.add_fund_strategy_asset_analytic(
                    FundStrategyAssetAnalytic(row['asset_ticker'], category, subcategory, value))

        return fund_strategy


if __name__ == '__main__':
    from datetime import datetime

    d = ArpProcCaller()

    t1 = Times(0, 'weekly', 'e', [], [], 0, 0)
    t_v = d._insert_times_strategy(t1, 'JS89275')

    ta1 = TimesAssetInput('test_ticker1', 'Equity', 'US', 'EUR', 'test_name', 'b', 2, 'f', 'g', float(1))
    ta2 = TimesAssetInput('test_ticker1', 'FX', 'US', 'EUR', 'test_name', 'b', 2, 'f', 'g', float(1))

    ins = d._insert_times_assets(t_v, [ta1])
    print(ins)

    ins = d._insert_times_assets(t_v, [ta2])
    print(ins)