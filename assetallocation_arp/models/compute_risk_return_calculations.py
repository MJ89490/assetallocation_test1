import pandas as pd
from math import sqrt


class ComputeRiskReturnCalculations:

    def __init__(self, start_date, end_date, dates_index):
        self.start_date = start_date
        self.end_date = end_date
        self.dates_index = dates_index

    def compute_no_signals_excess_returns(self, returns_excl_signals):
        exp = 365 / (self.end_date - self.start_date).days

        return (((returns_excl_signals.loc[self.end_date][0]/returns_excl_signals.loc[self.start_date][0]) ** exp) - 1) * 100

    @staticmethod
    def compute_no_signals_std_dev(returns_excl_signals):

        return (returns_excl_signals / returns_excl_signals.shift(1)).std()[0] * sqrt(52) * 100

    @staticmethod
    def compute_no_signals_sharpe_ratio(excess_returns, std_dev):

        return excess_returns / std_dev

    def compute_no_signals_max_drawdown(self, returns_excl_signals):

        # find out the max value between t_start and t_end
        max_price = (returns_excl_signals[self.start_date:self.end_date]).max()[0]
        # find out the max date
        max_price_date = returns_excl_signals[returns_excl_signals.Total_Excl_Signals == max_price].index.values[0]

        # find out the min value between t_max and date_end
        min_price = (returns_excl_signals[max_price_date:self.end_date]).min()[0]

        # compute the maximum drawdown
        return ((min_price / max_price) - 1) * 100

    @staticmethod
    def compute_no_signals_calmar_ratio(excess_returns, max_drawdown):

        return excess_returns / max_drawdown

    def compute_no_signals_equity_correlation(self):
        pass

    def compute_no_signals_gbi_em_correlation(self):
        pass

    def run_compute_risk_return_calculations(self, returns_excl_signals):
        returns_excl_signals.to_csv('returns_exl_sign.csv')
        excess_returns = self.compute_no_signals_excess_returns(returns_excl_signals)
        std_dev = self.compute_no_signals_std_dev(returns_excl_signals)
        sharpe_ratio = self.compute_no_signals_sharpe_ratio(excess_returns, std_dev)
        max_drawdown = self.compute_no_signals_max_drawdown(returns_excl_signals)
        calmar_ratio = self.compute_no_signals_calmar_ratio(excess_returns, max_drawdown)

