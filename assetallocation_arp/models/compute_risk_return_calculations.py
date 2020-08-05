import numpy as np
from math import sqrt


class ComputeRiskReturnCalculations:

    def __init__(self, start_date, end_date, dates_index):
        self.start_date = start_date
        self.end_date = end_date
        self.dates_index = dates_index

    def compute_no_signals_excess_returns(self, returns_excl_signals):
        exp = 365 / (self.end_date - self.start_date).days

        return ((returns_excl_signals.loc[self.end_date][0]/returns_excl_signals.loc[self.start_date][0] ** exp) - 1) * 100

    def compute_no_signals_std_dev(self, returns_excl_signals):
        next_start_date = self.dates_index[np.where(self.dates_index == self.start_date)[0][0] + 1]
        before_last_date = self.dates_index[np.where(self.dates_index == self.end_date)[0][0] - 1]

        (returns_excl_signals / returns_excl_signals.shift(1)).std() * sqrt(52)

        (returns_excl_signals[next_start_date:] / returns_excl_signals[self.start_date:before_last_date]).std() * sqrt(52)

        return 1

    @staticmethod
    def compute_no_signals_sharpe_ratio(excess_returns, std_dev):

        return excess_returns - std_dev

    def compute_no_signals_max_drawdown(self):
        pass
        # # find out the max value between t_start and t_end
        # max_price = pd.to_numeric(self.time_series[t_start:self.t_end]).max()
        #
        # # find out the max date
        # max_date_loc = pd.Index(pd.to_numeric(self.time_series[t_start:self.t_end])).get_loc(max_price)
        # t_max = self.time_series[t_start:self.t_end].index[max_date_loc]
        #
        # # find out the min value between t_max and date_end
        # min_price = pd.to_numeric(self.time_series[t_max:self.t_end]).min()
        #
        # # compute the maximum drawdown
        # self.maximum_drawdown.append((((min_price / max_price) - 1) * 100))

    @staticmethod
    def compute_no_signals_calmar_ratio(excess_returns, max_drawdown):
        pass

    def compute_no_signals_equity_correlation(self):
        pass

    def compute_no_signals_gbi_em_correlation(self):
        pass

    def run_compute_risk_return_calculations(self, returns_excl_signals):
        excess_returns = self.compute_no_signals_excess_returns(returns_excl_signals)
        std_dev = self.compute_no_signals_std_dev(returns_excl_signals)
        sharpe_ratio = self.compute_no_signals_sharpe_ratio(excess_returns, std_dev)
        max_drawdown = self.compute_no_signals_max_drawdown()
        calmar_ratio = self.compute_no_signals_calmar_ratio()

