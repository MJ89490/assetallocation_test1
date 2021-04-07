from typing import List, Union, Optional, Type, Dict
from os import environ
from json import loads
from abc import ABC, abstractmethod
import datetime as dt

import pandas as pd
from psycopg2.extras import DateTimeTZRange, DateRange

from assetallocation_arp.data_etl.dal.db import Db
from assetallocation_arp.data_etl.dal.data_models.strategy import Times, Effect, Fica, Fx, Strategy, Maven
from assetallocation_arp.data_etl.dal.data_models.fund_strategy import (FundStrategy, FundStrategyAssetWeight,
                                                                        FundStrategyAssetAnalytic, FundStrategyAnalytic)
from assetallocation_arp.data_etl.dal.type_converter import ArpTypeConverter
from assetallocation_arp.data_etl.dal.data_models.asset import TimesAssetInput, EffectAssetInput, Asset, \
    FicaAssetInput, FxAssetInput, FicaAssetInputGroup, MavenAssetInput
from assetallocation_arp.common_libraries.dal_enums.strategy import Name
from assetallocation_arp.common_libraries.dal_enums.fund_strategy import AggregationLevel
from assetallocation_arp.data_etl.dal.data_models.app_user import AppUser
from assetallocation_arp.data_etl.dal.proc import ArpProc, StrategyProcFactory


class StrategyProcCallerFactory:
    @staticmethod
    def get_proc_caller(strategy_name: Name) -> Type['StrategyProcCaller']:
        proc_maps = {
            Name.times: TimesProcCaller,
            Name.effect: EffectProcCaller,
            Name.fica: FicaProcCaller,
            Name.fx: FxProcCaller,
            Name.maven: MavenProcCaller
        }
        return proc_maps[strategy_name]


class ArpProcCaller(Db):
    procs = list(ArpProc.__members__.keys())

    def __init__(self):
        """ArpProcCaller class to interact with ARP database through calling stored procedures"""
        config = loads(environ.get('DATABASE', '{}'))
        user = config.get('USER')
        password = config.get('PASSWORD')
        host = config.get('HOST')
        port = config.get('PORT')
        database = config.get('DATABASE')
        super().__init__(f'postgresql://{user}:{password}@{host}:{port}/{database}')

    def _add_allowed_procs(self, allowed_procs: List[str]):
        self.procs.extend(allowed_procs)

    def insert_app_user(self, app_user: AppUser) -> bool:
        self.call_proc('arp.insert_app_user', [app_user.user_id, app_user.name, app_user.email])
        return True

    def insert_fund_strategy_results(
            self, fund_strategy: FundStrategy, user_id: str, business_date_from: dt.date, business_date_to: dt.date
    ) -> bool:
        """Insert data from an instance of FundStrategy into database"""
        business_date_range = DateRange(business_date_from, business_date_to, '[]')
        asset_weights = ArpTypeConverter.weights_to_composite(fund_strategy.asset_weights)
        strategy_analytics, strategy_asset_analytics = \
            ArpTypeConverter.fund_strategy_analytics_to_composites(fund_strategy.analytics)

        res = self.call_proc(
            'arp.insert_fund_strategy_results',
            [
                fund_strategy.fund_name, fund_strategy.strategy_name.name, fund_strategy.strategy_version,
                business_date_range, fund_strategy.weight, user_id, fund_strategy.python_code_version,
                asset_weights, strategy_analytics, strategy_asset_analytics
            ]
        )
        fund_strategy_id = res[0].get('fund_strategy_id')

        return fund_strategy_id is not None

    def select_fund_strategy_results(
            self, fund_name: str, strategy_name: Union[str, Name], strategy_version: int, business_date_from: dt.date,
            business_date_to: dt.date
    ) -> Optional[FundStrategy]:
        """Select the FundStrategy data for strategy where name equals strategy_name and version equals strategy version
        and model_instance.business_daterange equals DateRange(business_date_from, business_date_to, '[]')"""
        strategy_name = strategy_name.name if isinstance(strategy_name, Name) else Name[strategy_name].name
        strategy_id = self.call_proc('arp.select_strategy_id', [strategy_name, strategy_version])[0]['strategy_id']
        fs_weights = self.call_proc(
            'arp.select_fund_strategy_weights', [fund_name, strategy_id, business_date_from, business_date_to]
        )
        if not fs_weights:
            return

        fund_strategy = FundStrategy(fund_name, strategy_name, strategy_version, float(fs_weights[0]['strategy_weight']))
        fund_strategy.python_code_version = fs_weights[0]['python_code_version']

        for row in fs_weights:
            if pd.notna(row['strategy_weight']):
                aw = FundStrategyAssetWeight(
                    row['asset_subcategory'], row['business_date'], float(row['theoretical_asset_weight']),
                    row['asset_weight_frequency'], row['asset_ticker']
                )
                aw.implemented_weight = float(row['implemented_asset_weight'])
                fund_strategy.add_asset_weight(aw)

        fs_analytics = self.call_proc(
            'arp.select_fund_strategy_analytics', [fund_name, strategy_id, business_date_from, business_date_to]
        )
        strategy_analytics = []
        for row in fs_analytics:
            strategy_analytics.append(FundStrategyAnalytic(
                row['business_date'], row['category'], row['subcategory'], row['value'], row['frequency'])
            )

            if row['comparator_name'] is not None:
                c = FundStrategyAnalytic(
                    row['business_date'], row['category'], row['subcategory'], row['comparator_value'],
                    row['frequency'], aggregation_level=AggregationLevel.comparator
                )
                c.comparator_name = row['comparator_name']
                strategy_analytics.append(c)

        fund_strategy.add_analytics(strategy_analytics)

        fs_asset_analytics = self.call_proc(
            'arp.select_fund_strategy_asset_analytics', [fund_name, strategy_id, business_date_from, business_date_to]
        )
        asset_analytics = []
        for row in fs_asset_analytics:
            asset_analytics.append(FundStrategyAssetAnalytic(
                row['asset_ticker'], row['asset_subcategory'], row['business_date'], row['category'],
                row['subcategory'], row['value'], row['frequency']
            ))

        fund_strategy.add_analytics(asset_analytics)

        return fund_strategy

    def select_strategy_versions(self, strategy_name: Union[str, Name]) -> Dict[int, str]:
        """return dict of keys of version and values of description"""
        strategy_name = strategy_name.name if isinstance(strategy_name, Name) else Name[strategy_name].name

        res = self.call_proc('arp.select_strategy_versions', [strategy_name])
        print(res)
        return {row['version']: row['description'] for row in res}

    def select_fund_names(self) -> List[str]:
        res = self.call_proc('fund.select_fund_names', [])
        return res[0].get('fund_names') or []

    def select_asset_tickers_names_subcategories(self) -> pd.DataFrame:
        """
        :return: DataFrame with columns ticker, name, subcategory
        """
        query = """
        SELECT 
          a.ticker,
          a.name,
          ag.subcategory
        FROM
          asset.asset a
          JOIN asset.asset_group ag ON a.asset_group_id = ag.id  
        """
        with self.engine.connect() as connection:
            assets = pd.read_sql(query, connection)

        return assets


# noinspection PyAttributeOutsideInit
class StrategyProcCaller(ABC, ArpProcCaller):
    def __init__(self):
        super().__init__()
        super(ABC, self).__init__()
        self._add_allowed_procs(list(StrategyProcFactory.get_strategy_proc(self.strategy_name).__members__.keys()))

    @property
    @abstractmethod
    def strategy_name(self) -> Name:
        pass

    @abstractmethod
    def insert_strategy(self, strategy: Strategy, user_id: str) -> None:
        pass

    @abstractmethod
    def select_strategy(self, strategy_version: int) -> Optional[Strategy]:
        pass

    @abstractmethod
    def select_strategy_with_asset_analytics(
            self, strategy_version: int, business_date_from: dt.date, business_date_to: dt.date
    ) -> Optional[Strategy]:
        pass

    @abstractmethod
    def get_asset_analytics_for_strategy(
            self, strategy: Strategy, business_date_from: dt.date, business_date_to: dt.date
    ) -> None:
        """Add asset analytics to strategy."""
        pass


class TimesProcCaller(StrategyProcCaller):
    @property
    def strategy_name(self) -> Name:
        return Name.times

    def insert_strategy(self, strategy: Times, user_id: str) -> None:
        """Insert data from an instance of Times into database. Return strategy version."""
        strategy.version = self._insert_times_strategy(strategy, user_id)
        if strategy.asset_inputs:
            self._insert_times_assets(strategy.version, strategy.asset_inputs)

    def _insert_times_strategy(self, times: Times, user_id: str) -> int:
        """Insert data from an instance of Times into database"""
        res = self.call_proc(
            'arp.insert_times_strategy',
            [
                times.business_date_from, times.description, user_id, times.time_lag_interval, times.leverage_type.name,
                times.volatility_window, times.short_signals, times.long_signals, times.frequency.name,
                times.day_of_week.value
            ]
        )

        return res[0]['t_version']

    def _insert_times_assets(self, times_version: int, times_assets: List[TimesAssetInput]) -> bool:
        """Insert asset data for a version of times"""
        times_assets = ArpTypeConverter.times_assets_to_composite(times_assets)
        self.call_proc('arp.insert_times_assets', [times_version, times_assets])
        return True

    def get_asset_analytics_for_strategy(
            self, strategy: Times, business_date_from: dt.date, business_date_to: dt.date
    ) -> None:
        """Add asset analytics to strategy."""
        if strategy.asset_inputs:
            strategy.asset_inputs = self._select_times_assets_with_analytics(
                strategy.version, business_date_from, business_date_to
            )

    def _select_times_assets_with_analytics(
            self, times_version, business_date_from: dt.date, business_date_to: dt.date
    ) -> Optional[List[TimesAssetInput]]:
        """Select assets and asset analytics data for a version of times, as at business_datetime"""
        business_tstzrange = DateTimeTZRange(business_date_from, business_date_to, '[]')
        res = self.call_proc('arp.select_times_assets_with_analytics', [times_version, business_tstzrange])
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

    def select_strategy(self, times_version: int) -> Optional[Times]:
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
        t.business_date_from = row['business_date_from']
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
            self, strategy_version: int, business_date_from: dt.date, business_date_to: dt.date
    ) -> Optional[Times]:
        """Select strategy, assets and asset analytics data for a version of times, as at business_datetime"""
        times = self._select_times_strategy(strategy_version)

        if times is not None:
            times.asset_inputs = self._select_times_assets_with_analytics(
                strategy_version, business_date_from, business_date_to
            )

        return times

    def select_fund_strategy_result_dates(self, fund_name: str, strategy_version: int) -> Dict[str, Optional[bool]]:
        return {dt.date(2001, 8, 7): True}


class FxProcCaller(StrategyProcCaller):
    @property
    def strategy_name(self) -> Name:
        return Name.fx

    def insert_strategy(self, strategy: Fx, user_id: str) -> None:
        """Insert data from an instance of Fx into database. Return strategy version."""
        strategy.version = self._insert_fx_strategy(strategy, user_id)
        if strategy.asset_inputs:
            self._insert_fx_assets(strategy.version, strategy.asset_inputs)

    def _insert_fx_strategy(self, fx: Fx, user_id: str) -> int:
        """Insert data from an instance of Fx into database"""
        res = self.call_proc(
            'arp.insert_fx_strategy',
            [
                fx.business_date_from, fx.description, user_id, fx.model, fx.signal, fx.currency, fx.response_function,
                fx.exposure, fx.momentum_weights, fx.transaction_cost, fx.top_crosses, fx.vol_window, fx.value_window,
                fx.sharpe_cutoff, fx.mean_reversion, fx.historical_base, fx.defensive
            ]
        )

        return res[0]['f_version']

    def _insert_fx_assets(self, fx_version: int, fx_assets: List[FxAssetInput]) -> bool:
        """Insert asset data for a version of fx"""
        fx_assets = ArpTypeConverter.fx_assets_to_composite(fx_assets)
        self.call_proc('arp.insert_fx_assets', [fx_version, fx_assets])
        return True

    def add_asset_analytics_to_strategy(
            self, strategy: Fx, business_date_from: dt.date, business_date_to: dt.date
    ) -> None:
        """Add asset analytics to strategy."""
        if strategy.asset_inputs:
            business_tstzrange = DateTimeTZRange(business_date_from, business_date_to, '[]')
            strategy.asset_inputs = self._select_fx_assets_with_analytics(strategy.version, business_tstzrange)

            carry_tickers = FxAssetInput.get_carry_tickers(strategy.asset_inputs)
            strategy.carry_assets = self._select_assets_with_analytics(carry_tickers, business_tstzrange)

            spot_tickers = FxAssetInput.get_spot_tickers(strategy.asset_inputs)
            strategy.spot_assets = self._select_assets_with_analytics(spot_tickers, business_tstzrange)

    def _select_fx_assets_with_analytics(self, fx_version, business_tstzrange: DateTimeTZRange) -> Optional[List[FxAssetInput]]:
        """Select assets and asset analytics data for a version of fx"""
        res = self.call_proc('arp.select_fx_assets_with_analytics', [fx_version, business_tstzrange])
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

    def _select_assets_with_analytics(self, tickers: List[str], business_tstzrange: DateTimeTZRange) -> List[Asset]:
        res = self.call_proc('asset.select_assets_with_analytics', [tickers, business_tstzrange])
        assets = []
        for r in res:
            a = Asset(r['ticker'])
            a.asset_analytics = ArpTypeConverter.asset_analytics_str_to_objects(r['ticker'], r['analytics'])

            assets.append(a)

        return assets

    def select_strategy(self, strategy_version: int) -> Optional[Fx]:
        """Select strategy and asset data for a version of fx"""
        fx = self._select_fx_strategy(strategy_version)

        if fx is not None:
            fx.asset_inputs = self._select_fx_assets(strategy_version)

        return fx

    def _select_fx_strategy(self, fx_version) -> Optional[Fx]:
        """Select strategy data for a version of fx"""
        res = self.call_proc('arp.select_fx_strategy', [fx_version])
        if not res:
            return

        r = res[0]

        f = Fx(
            r['model'], r['signal'], r['currency'], r['response_function'],
            float(r['exposure']), r['momentum_weights'], float(r['transaction_cost'])
        )
        f.top_crosses = r.get('top_crosses')
        f.vol_window = r.get('vol_window')
        f.value_window = r.get('value_window')
        f.sharpe_cutoff = r.get('sharpe_cutoff')
        f.sharpe_cutoff = r.get('sharpe_cutoff')
        f.historical_base = r.get('historical_base')
        f.mean_reversion = r.get('mean_reversion')
        f.defensive = r.get('defensive')

        f.version = fx_version
        f.description = r['description']
        f.business_date_from = r['business_date_from']

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
            fx.asset_inputs = self._select_fx_assets_with_analytics(strategy_version)

            carry_tickers = FxAssetInput.get_carry_tickers(fx.asset_inputs)
            fx.carry_assets = self._select_assets_with_analytics(carry_tickers, fx.business_tstzrange)

            spot_tickers = FxAssetInput.get_spot_tickers(fx.asset_inputs)
            fx.spot_assets = self._select_assets_with_analytics(spot_tickers, fx.business_tstzrange)

        return fx

    @staticmethod
    def _construct_fx_asset_input(row) -> FxAssetInput:
        t = FxAssetInput(row['ppp_ticker'], row['cash_rate_ticker'], row['currency'])
        t.ppp_asset = Asset(row['ppp_ticker'])
        t.cash_rate_asset = Asset(row['cash_rate_ticker'])
        return t


class EffectProcCaller(StrategyProcCaller):
    @property
    def strategy_name(self) -> Name:
        return Name.effect

    def insert_strategy(self, strategy: Effect, user_id: str) -> None:
        """Insert data from an instance of Effect into database"""
        strategy.version = self._insert_effect_strategy(strategy, user_id)
        if strategy.asset_inputs:
            self._insert_effect_assets(strategy.version, strategy.asset_inputs)

    def _insert_effect_strategy(self, effect: Effect, user_id: str) -> int:
        """Insert data from an instance of Effect into database"""
        res = self.call_proc(
            'arp.insert_effect_strategy',
            [
                effect.business_date_from, effect.description, user_id, effect.carry_type.name,
                effect.closing_threshold, effect.cost, effect.day_of_week.value, effect.frequency.name,
                effect.include_shorts, effect.inflation_lag_interval, effect.interest_rate_cut_off_long,
                effect.interest_rate_cut_off_short, effect.moving_average_long_term, effect.moving_average_short_term,
                effect.is_realtime_inflation_forecast, effect.trend_indicator.name
            ]
        )
        return res[0]['e_version']

    def _insert_effect_assets(self, effect_version: int, effect_assets: List[EffectAssetInput]) -> bool:
        """Insert asset data for a version of Effect"""
        effect_assets = ArpTypeConverter.effect_assets_to_composite(effect_assets)
        res = self.call_proc('arp.insert_effect_assets', [effect_version, effect_assets])
        asset_ids = res[0].get('asset_ids')
        return bool(asset_ids)

    def add_asset_analytics_to_strategy(
            self, strategy: Effect, business_date_from: dt.date, business_date_to: dt.date
    ) -> None:
        if strategy.asset_inputs:
            strategy.asset_inputs = self._select_effect_assets_with_analytics(
                strategy.version, business_date_from, business_date_to
            )

    def select_strategy(self, strategy_version: int) -> Optional[Effect]:
        """Select strategy and asset data for a version of effect"""
        effect = self._select_effect_strategy(strategy_version)

        if effect is not None:
            effect.asset_inputs = self._select_effect_assets(strategy_version)

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
        e.business_date_from = row['business_date_from']
        return e

    def _select_effect_assets(self, effect_version: int) -> Optional[List[EffectAssetInput]]:
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
            self, strategy_version: int, business_date_from: dt.date, business_date_to: dt.date
    ) -> Optional[Effect]:
        """Select strategy, assets and asset analytics data for a version of effect, as at business_datetime"""
        effect = self._select_effect_strategy(strategy_version)

        if effect is not None:
            effect.asset_inputs = self._select_effect_assets_with_analytics(
                strategy_version, business_date_from, business_date_to
            )

        return effect

    def _select_effect_assets_with_analytics(
            self, effect_version: int, business_date_from: dt.date, business_date_to: dt.date
    ) -> Optional[List[EffectAssetInput]]:
        """Select assets and asset analytics data for a version of effect, as at business_datetime"""
        business_tstzrange = DateTimeTZRange(business_date_from, business_date_to, '[]')
        res = self.call_proc('arp.select_effect_assets_with_analytics', [effect_version, business_tstzrange])

        if not res:
            return

        effect_assets = []
        for r in res:
            e = EffectAssetInput(r['asset_ticker'], r['ndf_code'], r['spot_code'], r['position_size'])
            e.asset_analytics = ArpTypeConverter.asset_analytics_str_to_objects(r['asset_ticker'], r['asset_analytics'])

            effect_assets.append(e)

        return effect_assets


class FicaProcCaller(StrategyProcCaller):
    @property
    def strategy_name(self) -> Name:
        return Name.fica

    def insert_strategy(self, strategy: Fica, user_id: str) -> None:
        """Insert data from an instance of Fica into database"""
        strategy.version = self._insert_fica_strategy(strategy, user_id)
        if strategy.grouped_asset_inputs:
            self._insert_fica_assets(strategy.version, strategy.grouped_asset_inputs)

    def _insert_fica_strategy(self, fica: Fica, user_id: str) -> int:
        """Insert data from an instance of Fica into database"""
        res = self.call_proc(
            'arp.insert_fica_strategy',
            [
                fica.business_date_from, fica.description, user_id, fica.coupon, fica.curve, fica.strategy_weights,
                fica.tenor, fica.trading_cost
            ]
        )
        return res[0]['f_version']

    def _insert_fica_assets(self, fica_version: int, fica_asset_groups: List[FicaAssetInputGroup]) -> None:
        """Insert asset data for a version of Fica"""
        for i in fica_asset_groups:
            asset_tickers, names = [], []
            for j in i.fica_asset_inputs:
                asset_tickers.append(j.ticker)
                names.append(f'{j.curve_tenor}_{j.input_category}')

            self.call_proc(
                'arp.insert_fica_assets', [fica_version, asset_tickers, names]
            )

    def select_strategy(self, strategy_version: int) -> Optional[Fica]:
        """Select strategy and asset data for a version of fica"""
        fica = self._select_fica_strategy(strategy_version)

        if fica is not None:
            fica.grouped_asset_inputs = self._select_fica_assets(strategy_version)

        return fica

    def _select_fica_strategy(self, fica_version: int) -> Optional[Fica]:
        """Select strategy data for a version of fica"""
        res = self.call_proc('arp.select_fica_strategy', [fica_version])
        if not res:
            return

        row = res[0]
        f = Fica(row['coupon'], row['curve'], row['strategy_weights'], row['tenor'], row['trading_cost'])
        f.version = fica_version
        f.description = row['description']
        f.business_date_from = row['business_date_from']
        return f

    def _select_fica_assets(self, fica_version) -> Optional[List[FicaAssetInputGroup]]:
        """Select asset data for a version of fica"""
        res = self.call_proc('arp.select_fica_assets', [fica_version])
        if not res:
            return

        fica_asset_inputs = {}
        for r in res:
            curve_tenor, fica_asset_category = r['fica_asset_name'].split('_', 1)
            f = FicaAssetInput(r['asset_ticker'], fica_asset_category, curve_tenor)
            fica_asset_inputs[r['asset_subcategory']] = fica_asset_inputs.get(r['asset_subcategory'], [])
            fica_asset_inputs[r['asset_subcategory']].append(f)

        grouped_asset_inputs = [FicaAssetInputGroup(key, val) for key, val in fica_asset_inputs.items()]
        return grouped_asset_inputs

    def add_asset_analytics_to_strategy(
            self, strategy: Fica, business_date_from: dt.date, business_date_to: dt.date
    ) -> None:
        """Add asset analytics to strategy."""
        if strategy.grouped_asset_inputs:
            strategy.grouped_asset_inputs = self._select_fica_assets_with_analytics(
                strategy.version, business_date_from, business_date_to
            )

    def _select_fica_assets_with_analytics(
            self, fica_version: int, business_date_from: dt.date, business_date_to: dt.date
    ) -> Optional[List[FicaAssetInputGroup]]:
        """Select assets and asset analytics data for a version of fica, as at business_datetime"""
        business_tstzrange = DateTimeTZRange(business_date_from, business_date_to, '[]')
        res = self.call_proc('arp.select_fica_assets_with_analytics', [fica_version, business_tstzrange])

        if not res:
            return

        fica_asset_inputs = {}
        for r in res:
            curve_tenor, fica_asset_category = r['fica_asset_name'].split('_', 1)
            f = FicaAssetInput(r['asset_ticker'], fica_asset_category, curve_tenor)
            f.asset_analytics = ArpTypeConverter.asset_analytics_str_to_objects(r['asset_ticker'], r['asset_analytics'])
            fica_asset_inputs[r['asset_subcategory']] = fica_asset_inputs.get(r['asset_subcategory'], [])
            fica_asset_inputs[r['asset_subcategory']].append(f)

        grouped_asset_inputs = [FicaAssetInputGroup(key, val) for key, val in fica_asset_inputs.items()]
        return grouped_asset_inputs

    def select_strategy_with_asset_analytics(
            self, strategy_version: int, business_date_from: dt.date, business_date_to: dt.date
    ) -> Optional[Fica]:
        """Select strategy, assets and asset analytics data for a version of fica, as at business_datetime"""
        fica = self._select_fica_strategy(strategy_version)

        if fica is not None:
            fica.grouped_asset_inputs = self._select_fica_assets_with_analytics(
                strategy_version, business_date_from, business_date_to
            )

        return fica


class MavenProcCaller(StrategyProcCaller):
    @property
    def strategy_name(self) -> Name:
        return Name.maven

    def insert_strategy(self, strategy: Maven, user_id: str) -> None:
        """Insert data from an instance of Fica into database"""
        strategy.version = self._insert_maven_strategy(strategy, user_id)
        if strategy.asset_inputs:
            self._insert_maven_assets(strategy)

    def _insert_maven_strategy(self, strategy: Maven, user_id: str) -> int:
        """Insert data from an instance of Maven into database"""
        res = self.call_proc(
            'arp.insert_maven_strategy',
            [
                strategy.business_date_from, strategy.description, user_id, strategy.er_tr, strategy.frequency.name,
                strategy.day_of_week.value, strategy.business_tstzrange, strategy.asset_count,
                strategy.long_cutoff, strategy.short_cutoff, strategy.val_period_months,
                strategy.val_period_base, strategy.momentum_weights, strategy.volatility_weights
            ]
        )

        return res[0]['strategy_version']

    def _insert_maven_assets(self, strategy: Maven) -> bool:
        """Insert asset data for a version of fx"""
        maven_assets = ArpTypeConverter.maven_assets_to_composite(strategy.asset_inputs)
        self.call_proc('arp.insert_maven_assets', [strategy.version, maven_assets])
        return True

    def add_asset_analytics_to_strategy(
            self, strategy: Maven, business_date_from: dt.date, business_date_to: dt.date
    ) -> None:
        """Add asset analytics to strategy."""
        if strategy.asset_inputs:
            strategy.asset_inputs = self._select_maven_assets_with_analytics(
                strategy, business_date_from, business_date_to
            )

    def _select_maven_assets_with_analytics(
            self, strategy: Maven, business_date_from: dt.date, business_date_to: dt.date
    ) -> List[MavenAssetInput]:
        """Select assets and asset analytics data for a version of fx"""
        business_tstzrange = DateTimeTZRange(business_date_from, business_date_to, '[]')
        res = self.call_proc('arp.select_maven_assets_with_analytics', [strategy.version, business_tstzrange])
        if not res:
            return []

        asset_inputs = []
        for r in res:
            mai = MavenAssetInput(
                r['asset_subcategory'], r['bbg_tr_ticker'], r['bbg_er_ticker'], r['currency'],
                r['cash_ticker'], r['asset_category'], r['is_excess'], r['asset_weight'], r['transaction_cost']
            )
            mai.bbg_tr_asset.asset_analytics = ArpTypeConverter.asset_analytics_str_to_objects(
                r['bbg_tr_ticker'], r['bbg_tr_asset_analytics']
            )
            mai.bbg_er_asset.asset_analytics = ArpTypeConverter.asset_analytics_str_to_objects(
                r['bbg_er_ticker'], r['bbg_er_rate_asset_analytics']
            )
            mai.cash_asset.asset_analytics = ArpTypeConverter.asset_analytics_str_to_objects(
                r['cash_ticker'], r['cash_asset_analytics']
            )
            asset_inputs.append(mai)

        return asset_inputs

    def select_strategy(self, strategy_version: int) -> Optional[Maven]:
        """Select strategy and asset data for a version of maven"""
        strategy = self._select_maven_strategy(strategy_version)
        if strategy is not None:
            strategy.asset_inputs = self._select_maven_assets(strategy)
            return strategy

    def _select_maven_strategy(self, strategy_version) -> Optional[Maven]:
        """Select strategy data for a version of maven"""
        res = self.call_proc('arp.select_maven_strategy', [strategy_version])
        if not res:
            return

        r = res[0]
        m = Maven(
            r['er_tr'], r['frequency'], r['day_of_week'], r['business_tstzrange'], r['asset_count'], r['long_cutoff'],
            r['short_cutoff'], r['val_period_months'], r['val_period_base'], r['momentum_weights'],
            r['volatility_weights']
        )
        m.version = strategy_version
        m.description = r['description']

        return m

    def _select_maven_assets(self, strategy: Maven) -> List[MavenAssetInput]:
        """Select asset data for a version of maven"""
        res = self.call_proc('arp.select_maven_assets', [strategy.version])
        if not res:
            return []

        asset_inputs = []
        for r in res:
            mai = MavenAssetInput(
                r['asset_subcategory'], r['bbg_tr_ticker'], r['bbg_er_ticker'], r['currency'],
                r['cash_ticker'], r['asset_category'], r['is_excess'], r['asset_weight'], r['transaction_cost']
            )
            asset_inputs.append(mai)

        return asset_inputs

    def select_strategy_with_asset_analytics(
            self, strategy_version: int, business_date_from: dt.date, business_date_to: dt.date
    ) -> Optional[Maven]:
        """Select strategy, assets and asset analytics data for a version of maven"""
        strategy = self._select_maven_strategy(strategy_version)
        if strategy is not None:
            strategy.asset_inputs = self._select_maven_assets_with_analytics(
                strategy, business_date_from, business_date_to
            )
            return strategy


if __name__ == '__main__':
    from assetallocation_arp.data_etl.dal.data_frame_converter import DataFrameConverter
    apc = TimesProcCaller()
    fs = apc.select_fund_strategy_results('test_fund', Name.times, 827, business_date_from=dt.date(2000, 1, 1),
                                          business_date_to=dt.date(2001, 8, 7))
    print(fs)
    DataFrameConverter().fund_strategy_asset_weights_to_df(fs.asset_weights)
