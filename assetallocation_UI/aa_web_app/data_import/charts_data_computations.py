from datetime import timedelta
from typing import Dict

import pandas as pd

from assetallocation_UI.aa_web_app.data_import.assets_names import Assets


class ChartsDataComputations(object):
    """
        Class doing computations for the data of the dashboard
    """

    def __init__(self, times_signals, times_positions, times_returns):
        self.times_signals = times_signals
        self.times_positions = times_positions
        self.times_returns = times_returns
        self.end_year = ""
        self._times_signals_comp = None
        self._times_positions_comp = None
        self._times_returns_comp = None
        self._times_returns_ytd = None

    @property
    def signals_dates_off(self):
        return self.times_signals.last_valid_index()

    @property
    def returns_dates_off(self):
        return self.times_returns.last_valid_index()

    @property
    def positions_dates_off(self):
        return self.times_positions.last_valid_index()

    @property
    def returns_dates_weekly_off(self):
        return pd.Timestamp(self.times_returns.last_valid_index().date() - timedelta(days=7))

    @property
    def end_year_date(self):
        return self.end_year

    @end_year_date.setter
    def end_year_date(self, value):
        self.end_year = value

    @property
    def times_signals_comp(self) -> pd.DataFrame:
        return self._times_signals_comp

    @times_signals_comp.setter
    def times_signals_comp(self, x: pd.DataFrame) -> None:
        self._times_signals_comp = x

    @property
    def times_positions_comp(self) -> pd.DataFrame:
        return self._times_positions_comp

    @times_positions_comp.setter
    def times_positions_comp(self, x: pd.DataFrame) -> None:
        self._times_positions_comp = x

    @property
    def times_returns_comp(self) -> pd.DataFrame:
        return self._times_returns_comp

    @times_returns_comp.setter
    def times_returns_comp(self, x: pd.DataFrame) -> None:
        self._times_returns_comp = x

    @property
    def times_returns_ytd(self) -> pd.DataFrame:
        return self._times_returns_ytd

    @times_returns_ytd.setter
    def times_returns_ytd(self, x: pd.DataFrame) -> None:
        self._times_returns_ytd = x

    def data_computations(self) -> Dict[str, pd.DataFrame]:
        self.times_signals_comp = round(self.times_signals.loc[self.signals_dates_off], 2)
        self.times_positions_comp = round(self.times_positions.loc[self.positions_dates_off] * 100, 2)
        self.times_returns_comp = round((self.times_returns.loc[self.returns_dates_off] - self.times_returns.loc[self.returns_dates_weekly_off]) * 100, 3)
        self.times_returns_ytd = round((self.times_returns.loc[self.returns_dates_off] - self.times_returns.loc[self.end_year]) * 100, 3)

        return {'times_signals_comp': self.times_signals_comp, 'times_positions_comp': self.times_positions_comp,
                'times_returns_comp': self.times_returns_comp, 'times_returns_ytd': self.times_returns_ytd}

    def data_computations_sum(self) -> Dict[str, pd.DataFrame]:
        """
        :return: dictionary with all the computations such as the sum of the equities positions, sum of the bonds positions
        """
        sum_positions_bonds, sum_positions_equities, sum_positions_fx = self.sum_equities_bonds_fx(self.times_positions_comp)
        sum_performance_weekly_equities, sum_performance_weekly_bonds, sum_performance_weekly_fx = self.sum_equities_bonds_fx(self.times_returns)
        sum_performance_ytd_equities, sum_performance_ytd_bonds, sum_performance_ytd_fx = self.sum_equities_bonds_fx(self.times_returns_ytd)

        return {'sum_positions_equities': sum_positions_equities, 'sum_positions_bonds': sum_positions_bonds,
                'sum_positions_fx': sum_positions_fx, 'sum_performance_weekly_equities': sum_performance_weekly_equities,
                'sum_performance_weekly_bonds': sum_performance_weekly_bonds, 'sum_performance_weekly_fx': sum_performance_weekly_fx,
                'sum_performance_ytd_equities': sum_performance_ytd_equities, 'sum_performance_ytd_bonds': sum_performance_ytd_bonds,
                'sum_performance_ytd_fx': sum_performance_ytd_fx}

    def sum_equities_bonds_fx(self, equities_bonds_fx_data):
        equities1 = Assets.US_Equities.name
        equities2 = Assets.HK_Equities.name

        position_bond1 = Assets.US_10_y_Bonds.name
        position_bond2 = Assets.CA_10_y_Bonds.name

        positions_fx1 = Assets.JPY.name
        positions_fx2 = Assets.GBP.name

        equities = self.round_sum(equities1, equities2, equities_bonds_fx_data)
        bonds = self.round_sum(position_bond1, position_bond2, equities_bonds_fx_data)
        fx = self.round_sum(positions_fx1, positions_fx2, equities_bonds_fx_data)
        return bonds, equities, fx

    @staticmethod
    def round_sum(a1, a2, times_positions_comp):
        return round(sum(times_positions_comp.loc[a1:a2]), 2)
