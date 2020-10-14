from typing import List, Union, Optional
from os import environ
from json import loads

from assetallocation_arp.data_etl.dal.db import Db
from assetallocation_arp.data_etl.dal.data_models.strategy import Times, Effect, Fica
from assetallocation_arp.data_etl.dal.data_models.fund_strategy import (FundStrategy, FundStrategyAssetWeight)
from assetallocation_arp.data_etl.dal.type_converter import ArpTypeConverter
from assetallocation_arp.data_etl.dal.data_models.asset import TimesAssetInput, EffectAssetInput, Asset, FicaAssetInput
from assetallocation_arp.common_libraries.dal_enums.strategy import Name
from assetallocation_arp.data_etl.dal.data_models.app_user import AppUser
from assetallocation_arp.data_etl.dal.proc import Proc, TimesProc, EffectProc, FicaProc


class ArpProcCaller(Db):
    procs = Proc.__members__.keys()

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

    def insert_fund_strategy_results(self, fund_strategy: FundStrategy, user_id: str) -> bool:
        """Insert data from an instance of FundStrategy into database"""
        ticker_weights = ArpTypeConverter.weights_to_composite(fund_strategy.asset_weights)
        ticker_analytics = ArpTypeConverter.analytics_to_composite(fund_strategy.asset_analytics)

        res = self.call_proc('arp.insert_fund_strategy_results',
                             [fund_strategy.fund_name, fund_strategy.output_is_saved, fund_strategy.strategy_name.name,
                              fund_strategy.strategy_version, fund_strategy.weight, user_id,
                              fund_strategy.python_code_version, ticker_weights, ticker_analytics])
        fund_strategy_id = res[0].get('fund_strategy_id')

        return fund_strategy_id is not None

    def select_fund_strategy_results(self, fund_name: str, strategy_name: Union[str, Name], strategy_version: int) -> \
            Optional[FundStrategy]:
        """Select the most recent FundStrategy data for a strategy as at business_datetime and system_datetime"""
        strategy_name = strategy_name.name if isinstance(strategy_name, Name) else Name[strategy_name].name

        res = self.call_proc('arp.select_fund_strategy_results', [fund_name, strategy_name, strategy_version])

        if not res:
            return

        fund_strategy = FundStrategy(fund_name, strategy_name, strategy_version, float(res[0]['weight']))
        fund_strategy.output_is_saved = res[0]['output_is_saved']
        fund_strategy.python_code_version = res[0]['python_code_version']

        for row in res:
            a = Asset(row['asset_ticker'])
            a.category = row['asset_category']
            a.subcategory = row['asset_subcategory']
            fund_strategy.add_asset_if_not_exists(a)

            aw = FundStrategyAssetWeight(row['asset_ticker'], row['business_date'], float(row['strategy_weight']))
            aw.implemented_weight = float(row['implemented_weight'])
            fund_strategy.add_fund_strategy_asset_weight(aw)

            fund_strategy.add_fund_strategy_asset_analytics(
                ArpTypeConverter.fund_strategy_asset_analytics_str_to_objects(row['asset_ticker'], row['business_date'],
                                                                              row['asset_analytics']))

        return fund_strategy

    def select_strategy_versions(self, strategy_name: Union[str, Name]) -> List[int]:
        strategy_name = strategy_name.name if isinstance(strategy_name, Name) else Name[strategy_name].name

        res = self.call_proc('arp.select_strategy_versions', [strategy_name])
        return res[0].get('strategy_versions') or []

    def select_fund_names(self) -> List[str]:
        res = self.call_proc('fund.select_fund_names', [])
        return res[0].get('fund_names') or []


class TimesProcCaller(ArpProcCaller):
    procs = list(Proc.__members__.keys()) + list(TimesProc.__members__.keys())

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
            times.asset_inputs = self._select_times_assets(times_version)

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

        times_asset_inputs = []
        for r in res:
            t = self._construct_times_asset_input(r)

            times_asset_inputs.append(t)

        return times_asset_inputs

    def select_times_with_asset_analytics(self, times_version, business_datetime) -> Optional[Times]:
        """Select strategy, assets and asset analytics data for a version of times, as at business_datetime"""
        times = self._select_times_strategy(times_version)

        if times is not None:
            times.asset_inputs = self.select_times_assets_with_analytics(times_version, business_datetime)

        return times

    def select_times_assets_with_analytics(self, times_version, business_datetime) -> Optional[List[TimesAssetInput]]:
        """Select assets and asset analytics data for a version of times, as at business_datetime"""
        res = self.call_proc('arp.select_times_assets_with_analytics', [times_version, business_datetime])

        if not res:
            return

        times_assets = []
        for r in res:
            t = self._construct_times_asset_input(r)

            t.signal_asset.asset_analytics = ArpTypeConverter.asset_analytics_str_to_objects(r['signal_ticker'], r[
                'signal_asset_analytics'])
            t.future_asset.asset_analytics = ArpTypeConverter.asset_analytics_str_to_objects(r['future_ticker'], r[
                'future_asset_analytics'])

            times_assets.append(t)

        return times_assets

    @staticmethod
    def _construct_times_asset_input(row) -> TimesAssetInput:
        t = TimesAssetInput(row['s_leverage'], row['signal_ticker'], row['future_ticker'], float(row['cost']))
        t.signal_asset = Asset(row['signal_ticker'])
        t.future_asset = Asset(row['future_ticker'])
        return t


class EffectProcCaller(ArpProcCaller):
    procs = list(Proc.__members__.keys()) + list(EffectProc.__members__.keys())

    def insert_effect(self, effect: Effect, user_id: str) -> int:
        """Insert data from an instance of Effect into database"""
        e_version = self._insert_effect_strategy(effect, user_id)
        if effect.asset_inputs:
            self._insert_effect_assets(e_version, effect.asset_inputs)

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

    def _insert_effect_assets(self, effect_version: int, effect_assets: List[EffectAssetInput]) -> bool:
        """Insert asset data for a version of Effect"""
        effect_assets = ArpTypeConverter.effect_assets_to_composite(effect_assets)
        res = self.call_proc('arp.insert_effect_assets', [effect_version, effect_assets])
        asset_ids = res[0].get('asset_ids')
        return bool(asset_ids)

    def select_effect(self, effect_version) -> Optional[Effect]:
        """Select strategy and asset data for a version of effect"""
        effect = self._select_effect_strategy(effect_version)

        if effect is not None:
            effect.asset_inputs = self._select_effect_assets(effect_version)

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

    def _select_effect_assets(self, effect_version) -> Optional[List[EffectAssetInput]]:
        """Select asset data for a version of times"""
        res = self.call_proc('arp.select_effect_assets', [effect_version])

        if not res:
            return

        effect_assets = []
        for r in res:
            e = EffectAssetInput(r['asset_ticker'], r['ndf_code'], r['spot_code'], r['position_size'])
            effect_assets.append(e)

        return effect_assets

    def select_effect_with_asset_analytics(self, effect_version, business_datetime) -> Optional[Effect]:
        """Select strategy, assets and asset analytics data for a version of effect, as at business_datetime"""
        effect = self._select_effect_strategy(effect_version)

        if effect is not None:
            effect.asset_inputs = self.select_effect_assets_with_analytics(effect_version, business_datetime)

        return effect

    def select_effect_assets_with_analytics(self, effect_version, business_datetime) -> Optional[
        List[EffectAssetInput]]:
        """Select assets and asset analytics data for a version of times, as at business_datetime"""
        res = self.call_proc('arp.select_effect_assets_with_analytics', [effect_version, business_datetime])

        if not res:
            return

        effect_assets = []
        for r in res:
            e = EffectAssetInput(r['asset_ticker'], r['ndf_code'], r['spot_code'], r['position_size'])
            e.asset_analytics = ArpTypeConverter.asset_analytics_str_to_objects(r['asset_ticker'], r['asset_analytics'])

            effect_assets.append(e)

        return effect_assets


class FicaProcCaller(ArpProcCaller):
    procs = list(Proc.__members__.keys()) + list(FicaProc.__members__.keys())

    def insert_fica(self, fica: Fica, user_id: str) -> int:
        """Insert data from an instance of Fica into database"""
        f_version = self._insert_fica_strategy(fica, user_id)
        if fica.asset_inputs:
            self._insert_fica_assets(f_version, fica.asset_inputs)

        return f_version

    def _insert_fica_strategy(self, fica: Fica, user_id: str) -> int:
        """Insert data from an instance of Fica into database"""
        res = self.call_proc('arp.insert_fica_strategy',
                             [fica.description, user_id, fica.coupon, fica.curve, fica.business_tstzrange,
                              fica.strategy_weights, fica.tenor, fica.trading_cost])

        return res[0]['f_version']

    def _insert_fica_assets(self, fica_version: int, fica_assets: List[FicaAssetInput]) -> bool:
        """Insert asset data for a version of Fica"""
        fica_assets = ArpTypeConverter.fica_assets_to_composite(fica_assets)
        res = self.call_proc('arp.insert_fica_assets', [fica_version] + fica_assets)
        # todo update database function to return asset ids
        asset_ids = res[0].get('asset_ids')
        return bool(asset_ids)

    def select_fica(self, fica_version) -> Optional[Fica]:
        """Select strategy and asset data for a version of fica"""
        fica = self._select_fica_strategy(fica_version)

        if fica is not None:
            fica.asset_inputs = self._select_fica_assets(fica_version)

        return fica

    def _select_fica_strategy(self, fica_version) -> Optional[Fica]:
        """Select strategy data for a version of fica"""
        res = self.call_proc('arp.select_fica_strategy', [fica_version])
        if not res:
            return

        row = res[0]
        f = Fica(row['coupon'], row['curve'], row['business_tstzrange'], row['strategy_weights'], row['tenor'],
                 row['trading_cost'])
        f.version = fica_version
        f.description = row['description']
        return f

    def _select_fica_assets(self, fica_version) -> Optional[List[FicaAssetInput]]:
        """Select asset data for a version of fica"""
        res = self.call_proc('arp.select_fica_assets', [fica_version])
        if not res:
            return

        fica_assets = []
        for r in res:
            f = FicaAssetInput(r['asset_ticker'], ArpTypeConverter.ticker_str_to_object(r['sovereign_ticker']),
                               ArpTypeConverter.ticker_str_to_object(r['swap_ticker']),
                               ArpTypeConverter.ticker_str_to_object(r['swap_cr_ticker']))
            fica_assets.append(f)

        return fica_assets

    def select_fica_with_asset_analytics(self, fica_version, business_datetime) -> Optional[Fica]:
        """Select strategy, assets and asset analytics data for a version of fica, as at business_datetime"""
        fica = self._select_fica_strategy(fica_version)

        if fica is not None:
            fica.asset_inputs = self.select_fica_assets_with_analytics(fica_version, business_datetime)

        return fica

    def select_fica_assets_with_analytics(self, fica_version, business_datetime) -> Optional[List[FicaAssetInput]]:
        """Select assets and asset analytics data for a version of fica, as at business_datetime"""
        res = self.call_proc('arp.select_fica_assets_with_analytics', [fica_version, business_datetime])

        if not res:
            return

        fica_assets = []
        for r in res:
            f = FicaAssetInput(r['asset_ticker'], ArpTypeConverter.ticker_str_to_object(r['sovereign_ticker']),
                               ArpTypeConverter.ticker_str_to_object(r['swap_ticker']),
                               ArpTypeConverter.ticker_str_to_object(r['swap_cr_ticker']))
            f.asset_analytics = ArpTypeConverter.asset_analytics_str_to_objects(r['asset_ticker'], r['asset_analytics'])

            fica_assets.append(f)

        return fica_assets


if __name__ == '__main__':
    from psycopg2.extras import DateTimeTZRange
    from assetallocation_arp.data_etl.dal.data_models.ticker import Ticker
    import datetime as dt

    f = Fica(2, 'a', DateTimeTZRange(), [1, 2, 3], 1, 1)
    t1 = Ticker('sovereign', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a')
    t2 = Ticker('swap', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a')
    t3 = Ticker('swap_cr', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a')
    fa = FicaAssetInput('EURUSD Curncy', t1, t2, t3)

    f.asset_inputs = [fa]

    fpc = FicaProcCaller()
    f1 = fpc.select_fica_with_asset_analytics(42, dt.datetime(2000, 1, 1))
    print(f1)
    print(f1.coupon)
    print(f1.asset_inputs)

    for asset_input in f1.asset_inputs:
        print(asset_input.name)
        for i in asset_input.asset_analytics:
            print(i.asset_ticker, i.business_datetime, i.value)