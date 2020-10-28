from datetime import timedelta, date
from typing import Dict, Optional

import pandas as pd

from assetallocation_arp.common_libraries.dal_enums.asset import Equity, FixedIncome, FX


class TimesChartsDataComputations(object):
    """Class doing computations for the data of the times dashboard"""

    def __init__(self, times_signals, times_positions, times_returns):
        self.signals = times_signals
        self.positions = times_positions
        self.returns = times_returns
        self._signals_comp = None
        self._positions_comp = None
        self._returns_comp = None
        self._returns_ytd = None

    @property
    def max_signals_date(self) -> pd.Timestamp:
        return self.signals.last_valid_index()

    @property
    def max_returns_date(self) -> pd.Timestamp:
        return self.returns.last_valid_index()

    @property
    def max_positions_date(self) -> pd.Timestamp:
        return self.positions.last_valid_index()

    @property
    def returns_dates_weekly_off(self) -> pd.Timestamp:
        return pd.Timestamp(self.returns.last_valid_index().date() - timedelta(days=7))

    @property
    def prev_year_end(self) -> pd.Timestamp:
        return pd.Timestamp(date(self.max_returns_date.year, 1, 1) - timedelta(1))

    @property
    def signals_comp(self) -> pd.DataFrame:
        return self._signals_comp

    @signals_comp.setter
    def signals_comp(self, x: pd.DataFrame) -> None:
        self._signals_comp = x

    @property
    def positions_comp(self) -> pd.DataFrame:
        return self._positions_comp

    @positions_comp.setter
    def positions_comp(self, x: pd.DataFrame) -> None:
        self._positions_comp = x

    @property
    def returns_comp(self) -> pd.DataFrame:
        return self._returns_comp

    @returns_comp.setter
    def returns_comp(self, x: pd.DataFrame) -> None:
        self._returns_comp = x

    @property
    def returns_ytd(self) -> pd.DataFrame:
        return self._returns_ytd

    @returns_ytd.setter
    def returns_ytd(self, x: pd.DataFrame) -> None:
        self._returns_ytd = x

    def data_computations(self) -> Dict[str, pd.DataFrame]:
        self.signals_comp = round(self.signals.loc[self.max_signals_date], 2)
        self.positions_comp = round(self.positions.loc[self.max_positions_date] * 100, 2)
        self.returns_comp = round((self.returns.loc[self.max_returns_date] - self.returns.loc[self.returns_dates_weekly_off]) * 100, 3)
        self.returns_ytd = round((self.returns.loc[self.max_returns_date] - self.returns.loc[self.prev_year_end]) * 100, 3)

        return {'times_signals_comp': self.signals_comp, 'times_positions_comp': self.positions_comp,
                'times_returns_comp': self.returns_comp, 'times_returns_ytd': self.returns_ytd}

    def data_computations_sum(self) -> Dict[str, pd.DataFrame]:
        """
        :return: dictionary with all the computations such as the sum of the equities positions, sum of the bonds positions
        """
        sum_positions_bonds, sum_positions_equities, sum_positions_fx = self.sum_equities_bonds_fx(self.positions_comp)
        sum_performance_weekly_equities, sum_performance_weekly_bonds, sum_performance_weekly_fx = self.sum_equities_bonds_fx(self.returns_comp)
        sum_performance_ytd_equities, sum_performance_ytd_bonds, sum_performance_ytd_fx = self.sum_equities_bonds_fx(self.returns_ytd)

        return {'sum_positions_equities': sum_positions_equities, 'sum_positions_bonds': sum_positions_bonds,
                'sum_positions_fx': sum_positions_fx, 'sum_performance_weekly_equities': sum_performance_weekly_equities,
                'sum_performance_weekly_bonds': sum_performance_weekly_bonds, 'sum_performance_weekly_fx': sum_performance_weekly_fx,
                'sum_performance_ytd_equities': sum_performance_ytd_equities, 'sum_performance_ytd_bonds': sum_performance_ytd_bonds,
                'sum_performance_ytd_fx': sum_performance_ytd_fx}

    def sum_equities_bonds_fx(self, equities_bonds_fx_data):
        equities = [i.name for i in Equity if i.name in equities_bonds_fx_data.index]
        bonds = [i.name for i in FixedIncome if i.name in equities_bonds_fx_data.index]
        fx = [i.name for i in FX if i.name in equities_bonds_fx_data.index]

        equities = self.round_sum(equities_bonds_fx_data.loc[equities])
        bonds = self.round_sum(equities_bonds_fx_data.loc[bonds])
        fx = self.round_sum(equities_bonds_fx_data.loc[fx])
        return bonds, equities, fx

    @staticmethod
    def round_sum(df):
        return round(sum(df), 2)
