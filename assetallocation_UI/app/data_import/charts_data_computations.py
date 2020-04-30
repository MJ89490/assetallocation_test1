from app.data_import.assets_names import Assets

from datetime import timedelta

import pandas as pd


class ChartsDataComputations(object):

    def __init__(self, times_signals, times_positions, times_returns):
        self.times_signals = times_signals
        self.times_positions = times_positions
        self.times_returns = times_returns
        self.end_year = ""

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

    def data_computations(self, signal_off, returns_off, returns_weekly_off, positions_off):

        times_signals_comp = round(self.times_signals.loc[signal_off], 2)
        times_positions_comp = round((self.times_positions.loc[positions_off]) * 100, 2)
        times_returns_comp = round((self.times_returns.loc[returns_off] - self.times_returns.loc[returns_weekly_off]) * 100, 3)
        times_returns_ytd = round((self.times_returns.loc[returns_off] - self.times_returns.loc[self.end_year]) * 100, 3)

        return {'times_signals_comp': times_signals_comp, 'times_positions_comp': times_positions_comp,
                'times_returns_comp': times_returns_comp, 'times_returns_ytd': times_returns_ytd}

    def data_computations_sum(self, times_returns_ytd, times_positions_comp, times_returns):

        sum_positions_equities = round(sum(times_positions_comp.loc[Assets.US_Equities.name:Assets.HK_Equities.name]), 2)

        sum_positions_bonds = round(sum(times_positions_comp.loc[Assets.US_10_y_Bonds.name:Assets.CA_10_y_Bonds.name]), 2)

        sum_positions_fx = round(sum(times_positions_comp.loc[Assets.JPY.name:Assets.GBP.name]), 2)

        sum_performance_weekly_equities = round(sum(times_returns.loc[Assets.US_Equities.name:Assets.HK_Equities.name]), 2)

        sum_performance_weekly_bonds = round(sum(times_returns.loc[Assets.US_10_y_Bonds.name:Assets.CA_10_y_Bonds.name]), 2)

        sum_performance_weekly_fx = round(sum(times_returns.loc[Assets.JPY.name:Assets.GBP.name]), 2)

        sum_performance_ytd_equities = round(sum(times_returns_ytd.loc[Assets.US_Equities.name:Assets.HK_Equities.name]), 2)

        sum_performance_ytd_bonds = round(sum(times_returns_ytd.loc[Assets.US_10_y_Bonds.name:Assets.CA_10_y_Bonds.name]), 2)

        sum_performance_ytd_fx = round(sum(times_returns_ytd.loc[Assets.JPY.name:Assets.GBP.name]), 2)

        return {'sum_positions_equities': sum_positions_equities, 'sum_positions_bonds': sum_positions_bonds,
                'sum_positions_fx': sum_positions_fx, 'sum_performance_weekly_equities': sum_performance_weekly_equities,
                'sum_performance_weekly_bonds': sum_performance_weekly_bonds, 'sum_performance_weekly_fx': sum_performance_weekly_fx,
                'sum_performance_ytd_equities': sum_performance_ytd_equities, 'sum_performance_ytd_bonds': sum_performance_ytd_bonds,
                'sum_performance_ytd_fx': sum_performance_ytd_fx}