from typing import List, Union, Optional, Type
from os import environ
from json import loads
from abc import ABC, abstractmethod
import datetime as dt

import pandas as pd
from psycopg2.extras import DateTimeTZRange

from assetallocation_arp.data_etl.dal.db import Db
from assetallocation_arp.data_etl.dal.data_models.strategy import Times, Effect, Fica, Fx, Strategy
from assetallocation_arp.data_etl.dal.data_models.fund_strategy import (FundStrategy, FundStrategyAssetWeight)
from assetallocation_arp.data_etl.dal.type_converter import ArpTypeConverter
from assetallocation_arp.data_etl.dal.data_models.asset import TimesAssetInput, EffectAssetInput, Asset, \
    FicaAssetInput, FxAssetInput
from assetallocation_arp.common_libraries.dal_enums.strategy import Name
from assetallocation_arp.data_etl.dal.data_models.app_user import AppUser
from assetallocation_arp.data_etl.dal.proc import Proc, TimesProc, EffectProc, FicaProc, FxProc


class StrategyProcCallerFactory:
    @staticmethod
    def get_proc_caller(strategy_name: Name) -> Type['StrategyProcCaller']:
        proc_maps = {
            Name.times: TimesProcCaller,
            Name.effect: EffectProcCaller,
            Name.fica: FicaProcCaller,
            Name.fx: FxProcCaller
        }
        return proc_maps[strategy_name]


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
        asset_weights = ArpTypeConverter.weights_to_composite(fund_strategy.asset_weights)
        analytics = ArpTypeConverter.analytics_to_composite(fund_strategy.analytics)

        res = self.call_proc('arp.insert_fund_strategy_results',
                             [fund_strategy.fund_name, fund_strategy.output_is_saved, fund_strategy.strategy_name.name,
                              fund_strategy.strategy_version, fund_strategy.weight, user_id,
                              fund_strategy.python_code_version, asset_weights, analytics])
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
            if pd.notna(row['strategy_weight']):
                aw = FundStrategyAssetWeight(
                    row['asset_subcategory'], row['business_date'], float(row['strategy_weight']), row['weight_frequency']
                )
                aw.implemented_weight = float(row['implemented_weight'])
                fund_strategy.add_asset_weight(aw)

            fund_strategy.add_analytics(
                ArpTypeConverter.fund_strategy_analytics_str_to_objects(
                    row['asset_subcategory'], row['business_date'], row['analytics']
                )
            )

        return fund_strategy

    def select_strategy_versions(self, strategy_name: Union[str, Name]) -> List[int]:
        strategy_name = strategy_name.name if isinstance(strategy_name, Name) else Name[strategy_name].name

        res = self.call_proc('arp.select_strategy_versions', [strategy_name])
        return res[0].get('strategy_versions') or []

    def select_fund_names(self) -> List[str]:
        res = self.call_proc('fund.select_fund_names', [])
        return res[0].get('fund_names') or []


class StrategyProcCaller(ABC, ArpProcCaller):
    @abstractmethod
    def insert_strategy(self, strategy: Strategy, user_id: str) -> None:
        pass

    @abstractmethod
    def select_strategy_with_asset_analytics(
            self, strategy_version: int, business_datetime: Optional[dt.datetime]
    ) -> Optional[Strategy]:
        pass

    @abstractmethod
    def add_asset_analytics_to_strategy(self, strategy: Strategy, business_datetime: Optional[dt.datetime]) -> None:
        """Add asset analytics to strategy."""
        pass


class TimesProcCaller(StrategyProcCaller):
    procs = list(Proc.__members__.keys()) + list(TimesProc.__members__.keys())

    def add_asset_analytics_to_strategy(self, strategy: Times, business_datetime: Optional[dt.datetime]) -> None:
        """Add asset analytics to strategy."""
        if strategy.asset_inputs:
            strategy.asset_inputs = self.select_times_assets_with_analytics(strategy.version, business_datetime)

    def insert_strategy(self, strategy: Times, user_id: str) -> None:
        """Insert data from an instance of Times into database. Return strategy version."""
        strategy.version = self._insert_times_strategy(strategy, user_id)
        if strategy.asset_inputs:
            self._insert_times_assets(strategy.version, strategy.asset_inputs)

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
        t = Times(row['day_of_week'], row['frequency'], row['leverage_type'], [float(i) for i in row['long_signals']],
                  [float(i) for i in row['short_signals']],
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

    def select_strategy_with_asset_analytics(
            self, strategy_version: int, business_datetime: Optional[dt.datetime]
    ) -> Optional[Times]:
        """Select strategy, assets and asset analytics data for a version of times, as at business_datetime"""
        times = self._select_times_strategy(strategy_version)

        if times is not None:
            times.asset_inputs = self.select_times_assets_with_analytics(strategy_version, business_datetime)

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
        t = TimesAssetInput(
            row['asset_subcategory'], row['s_leverage'], row['signal_ticker'], row['future_ticker'], float(row['cost'])
        )
        t.signal_asset = Asset(row['signal_ticker'])
        t.future_asset = Asset(row['future_ticker'])
        return t


class FxProcCaller(StrategyProcCaller):
    procs = list(Proc.__members__.keys()) + list(FxProc.__members__.keys())

    def add_asset_analytics_to_strategy(self, strategy: Fx, business_datetime: Optional[dt.datetime] = None) -> None:
        """Add asset analytics to strategy."""
        if strategy.asset_inputs:
            strategy.asset_inputs = self.select_fx_assets_with_analytics(strategy.version)

            carry_tickers = FxAssetInput.get_carry_tickers(strategy.asset_inputs)
            strategy.carry_assets = self.select_assets_with_analytics(carry_tickers, strategy.business_tstzrange)

            spot_tickers = FxAssetInput.get_spot_tickers(strategy.asset_inputs)
            strategy.spot_assets = self.select_assets_with_analytics(spot_tickers, strategy.business_tstzrange)

    def insert_strategy(self, strategy: Fx, user_id: str) -> None:
        """Insert data from an instance of Fx into database. Return strategy version."""
        strategy.version = self._insert_fx_strategy(strategy, user_id)
        if strategy.asset_inputs:
            self._insert_fx_assets(strategy.version, strategy.asset_inputs)

    def _insert_fx_strategy(self, fx: Fx, user_id: str) -> int:
        """Insert data from an instance of Fx into database"""
        res = self.call_proc('arp.insert_fx_strategy',
                             [fx.description, user_id, fx.model, fx.business_tstzrange,
                              fx.signal, fx.currency, fx.response_function, fx.exposure,
                              fx.momentum_weights, fx.transaction_cost, fx.top_crosses, fx.vol_window,
                              fx.value_window, fx.sharpe_cutoff, fx.mean_reversion, fx.historical_base])

        return res[0]['f_version']

    def _insert_fx_assets(self, fx_version: int, fx_assets: List[FxAssetInput]) -> bool:
        """Insert asset data for a version of fx"""
        fx_assets = ArpTypeConverter.fx_assets_to_composite(fx_assets)
        self.call_proc('arp.insert_fx_assets', [fx_version, fx_assets])
        return True

    def select_fx(self, fx_version) -> Optional[Fx]:
        """Select strategy and asset data for a version of fx"""
        fx = self._select_fx_strategy(fx_version)

        if fx is not None:
            fx.asset_inputs = self._select_fx_assets(fx_version)

        return fx

    def _select_fx_strategy(self, fx_version) -> Optional[Fx]:
        """Select strategy data for a version of fx"""
        res = self.call_proc('arp.select_fx_strategy', [fx_version])
        if not res:
            return

        r = res[0]

        f = Fx(
            r['model'], r['business_tstzrange'], r['signal'], r['currency'], r['response_function'],
            float(r['exposure']), r['momentum_weights'], float(r['transaction_cost'])
        )
        f.version = fx_version
        f.description = r['description']

        f.top_crosses = r.get('top_crosses')
        f.vol_window = r.get('vol_window')
        f.value_window = r.get('value_window')
        f.sharpe_cutoff = r.get('sharpe_cutoff')
        f.sharpe_cutoff = r.get('sharpe_cutoff')
        f.historical_base = r.get('historical_base')
        f.mean_reversion = r.get('mean_reversion')

        f.version = fx_version
        f.description = r['description']

        return f

    def _select_fx_assets(self, fx_version) -> Optional[List[FxAssetInput]]:
        """Select asset data for a version of fx"""
        res = self.call_proc('arp.select_fx_assets', [fx_version])

        if not res:
            return

        fx_asset_inputs = []
        for r in res:
            t = self._construct_fx_asset_input(r)

            fx_asset_inputs.append(t)

        return fx_asset_inputs

    def select_strategy_with_asset_analytics(
            self, strategy_version: int, business_datetime: Optional[dt.datetime]
    ) -> Optional[Fx]:
        """Select strategy, assets and asset analytics data for a version of fx"""
        fx = self._select_fx_strategy(strategy_version)

        if fx is not None:
            fx.asset_inputs = self.select_fx_assets_with_analytics(strategy_version)

            carry_tickers = FxAssetInput.get_carry_tickers(fx.asset_inputs)
            fx.carry_assets = self.select_assets_with_analytics(carry_tickers, fx.business_tstzrange)

            spot_tickers = FxAssetInput.get_spot_tickers(fx.asset_inputs)
            fx.spot_assets = self.select_assets_with_analytics(spot_tickers, fx.business_tstzrange)

        return fx

    def select_assets_with_analytics(self, tickers: List[str], business_tstzrange: DateTimeTZRange) -> List[Asset]:
        res = self.call_proc('arp.select_assets_with_analytics', [tickers, business_tstzrange])
        assets = []
        for r in res:
            a = Asset(r['ticker'])
            a.asset_analytics = ArpTypeConverter.asset_analytics_str_to_objects(r['ticker'], r['analytics'])

            assets.append(a)

        return assets

    def select_fx_assets_with_analytics(self, fx_version) -> Optional[List[FxAssetInput]]:
        """Select assets and asset analytics data for a version of fx"""
        res = self.call_proc('arp.select_fx_assets_with_analytics', [fx_version])
        if not res:
            return

        fx_assets = []
        for r in res:
            t = self._construct_fx_asset_input(r)

            t.ppp_asset.asset_analytics = ArpTypeConverter.asset_analytics_str_to_objects(
                r['ppp_ticker'], r['ppp_asset_analytics']
            )
            t.cash_rate_asset.asset_analytics = ArpTypeConverter.asset_analytics_str_to_objects(
                r['cash_rate_ticker'], r['cash_rate_asset_analytics']
            )

            fx_assets.append(t)

        return fx_assets

    @staticmethod
    def _construct_fx_asset_input(row) -> FxAssetInput:
        t = FxAssetInput(row['ppp_ticker'], row['cash_rate_ticker'], row['currency'])
        t.ppp_asset = Asset(row['ppp_ticker'])
        t.cash_rate_asset = Asset(row['cash_rate_ticker'])
        return t


class EffectProcCaller(StrategyProcCaller):
    procs = list(Proc.__members__.keys()) + list(EffectProc.__members__.keys())

    def add_asset_analytics_to_strategy(self, strategy: Effect, business_datetime: Optional[dt.datetime]) -> None:
        if strategy.asset_inputs:
            strategy.asset_inputs = self.select_effect_assets_with_analytics(strategy.version, business_datetime)

    def insert_strategy(self, strategy: Effect, user_id: str) -> None:
        """Insert data from an instance of Effect into database"""
        strategy.version = self._insert_effect_strategy(strategy, user_id)
        if strategy.asset_inputs:
            self._insert_effect_assets(strategy.version, strategy.asset_inputs)

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
        """Select asset data for a version of effect"""
        res = self.call_proc('arp.select_effect_assets', [effect_version])

        if not res:
            return

        effect_assets = []
        for r in res:
            e = EffectAssetInput(r['asset_ticker'], r['ndf_code'], r['spot_code'], r['position_size'])
            effect_assets.append(e)

        return effect_assets

    def select_strategy_with_asset_analytics(
            self, strategy_version: int, business_datetime: Optional[dt.datetime]
    ) -> Optional[Effect]:
        """Select strategy, assets and asset analytics data for a version of effect, as at business_datetime"""
        effect = self._select_effect_strategy(strategy_version)

        if effect is not None:
            effect.asset_inputs = self.select_effect_assets_with_analytics(strategy_version, business_datetime)

        return effect

    def select_effect_assets_with_analytics(
            self, effect_version: int, business_datetime: dt.datetime
    ) -> Optional[List[EffectAssetInput]]:
        """Select assets and asset analytics data for a version of effect, as at business_datetime"""
        res = self.call_proc('arp.select_effect_assets_with_analytics', [effect_version, business_datetime])

        if not res:
            return

        effect_assets = []
        for r in res:
            e = EffectAssetInput(r['asset_ticker'], r['ndf_code'], r['spot_code'], r['position_size'])
            e.asset_analytics = ArpTypeConverter.asset_analytics_str_to_objects(r['asset_ticker'], r['asset_analytics'])

            effect_assets.append(e)

        return effect_assets


class FicaProcCaller(StrategyProcCaller):
    procs = list(Proc.__members__.keys()) + list(FicaProc.__members__.keys())

    def add_asset_analytics_to_strategy(self, strategy: Fx, business_datetime: Optional[dt.datetime] = None) -> None:
        """Add asset analytics to strategy."""
        if strategy.grouped_asset_inputs:
            strategy.grouped_asset_inputs = self.select_fica_assets_with_analytics(strategy.version)

    def insert_strategy(self, strategy: Fica, user_id: str) -> None:
        """Insert data from an instance of Fica into database"""
        strategy.version = self._insert_fica_strategy(strategy, user_id)
        if strategy.grouped_asset_inputs:
            self._insert_fica_assets(strategy.version, strategy.grouped_asset_inputs)

    def _insert_fica_strategy(self, fica: Fica, user_id: str) -> int:
        """Insert data from an instance of Fica into database"""
        res = self.call_proc('arp.insert_fica_strategy',
                             [fica.description, user_id, fica.coupon, fica.curve, fica.business_tstzrange,
                              fica.strategy_weights, fica.tenor, fica.trading_cost])

        return res[0]['f_version']

    def _insert_fica_assets(self, fica_version: int, fica_asset_groups: List[List[FicaAssetInput]]) -> None:
        """Insert asset data for a version of Fica"""
        for i in fica_asset_groups:
            asset_tickers, categories, curve_tenors = [], [], []
            for j in i:
                asset_tickers.append(j.ticker)
                categories.append(j.input_category)
                curve_tenors.append(j.curve_tenor)

            self.call_proc('arp.insert_fica_assets', [fica_version, asset_tickers, categories, curve_tenors])

    def select_fica(self, fica_version: int) -> Optional[Fica]:
        """Select strategy and asset data for a version of fica"""
        fica = self._select_fica_strategy(fica_version)

        if fica is not None:
            fica.grouped_asset_inputs = self._select_fica_assets(fica_version)

        return fica

    def _select_fica_strategy(self, fica_version: int) -> Optional[Fica]:
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
            f = FicaAssetInput(r['asset_ticker'], r['fica_asset_category'], r['curve_tenor'])
            fica_assets.append(f)

        return fica_assets

    def select_strategy_with_asset_analytics(
            self, strategy_version: int, business_datetime: Optional[dt.datetime] = None
    ) -> Optional[Fica]:
        """Select strategy, assets and asset analytics data for a version of fica, as at business_datetime"""
        fica = self._select_fica_strategy(strategy_version)

        if fica is not None:
            fica.grouped_asset_inputs = self.select_fica_assets_with_analytics(strategy_version)

        return fica

    def select_fica_assets_with_analytics(self, fica_version) -> Optional[List[FicaAssetInput]]:
        """Select assets and asset analytics data for a version of fica, as at business_datetime"""
        res = self.call_proc('arp.select_fica_assets_with_analytics', [fica_version])

        if not res:
            return

        fica_assets = []
        for r in res:
            f = FicaAssetInput(r['asset_ticker'], r['fica_asset_category'], r['curve_tenor'])
            f.asset_analytics = ArpTypeConverter.asset_analytics_str_to_objects(r['asset_ticker'], r['asset_analytics'])

            fica_assets.append(f)

        return fica_assets


if __name__ == '__main__':
    apc = ArpProcCaller()
    fs = apc.select_fund_strategy_results('f1', 'times', 432)
    print(fs)
