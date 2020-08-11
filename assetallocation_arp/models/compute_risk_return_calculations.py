from math import sqrt

#todo add docstrings

class ComputeRiskReturnCalculations:

    def __init__(self, start_date, end_date, dates_index):
        self.start_date = start_date
        self.end_date = end_date
        self.dates_index = dates_index

    def compute_excess_returns(self, returns_excl_signals, returns_incl_signals):
        exp = 365 / (self.end_date - self.start_date).days

        excess_returns_no_signals = (((returns_excl_signals.loc[self.end_date][0] / returns_excl_signals.loc[self.start_date][0]) ** exp) - 1) * 100
        excess_returns_with_signals = (((returns_incl_signals.loc[self.end_date][0] / returns_incl_signals.loc[self.start_date][0]) ** exp) - 1) * 100

        return {'excess_returns_no_signals': excess_returns_no_signals,
                'excess_returns_with_signals': excess_returns_with_signals}

    @staticmethod
    def compute_std_dev(returns_excl_signals, returns_incl_signals):

        std_dev_no_signals = (returns_excl_signals / returns_excl_signals.shift(1)).std()[0] * sqrt(52) * 100
        std_dev_with_signals = (returns_incl_signals / returns_incl_signals.shift(1)).std()[0] * sqrt(52) * 100

        return {'std_dev_no_signals': std_dev_no_signals, 'std_dev_with_signals': std_dev_with_signals}

    @staticmethod
    def compute_sharpe_ratio(excess_returns, std_dev):

        sharpe_ratio_no_signals = excess_returns['excess_returns_no_signals'] / std_dev['std_dev_no_signals']
        sharpe_ratio_with_signals = excess_returns['excess_returns_with_signals'] / std_dev['std_dev_with_signals']

        return {'sharpe_ratio_no_signals': sharpe_ratio_no_signals,
                'sharpe_ratio_with_signals': sharpe_ratio_with_signals}

    @staticmethod
    def compute_max_drawdown(returns_excl_signals, returns_incl_signals):

        returns_excl_tmp = returns_excl_signals.Total_Excl_Signals.to_list()
        returns_incl_tmp = returns_incl_signals.Total_Incl_Signals.tolist()

        max_drawdown_excl_values, max_drawdown_incl_values = [], []

        for value in range(len(returns_excl_tmp)):

            max_drawdown_excl_values.append(returns_excl_tmp[value] / max(returns_excl_tmp[0: value+1]) - 1)
            max_drawdown_incl_values.append(returns_incl_tmp[value] / max(returns_incl_tmp[0: value+1]) - 1)

        return {'max_drawdown_no_signals': abs(min(max_drawdown_excl_values)) * 100,
                'max_drawdown_with_signals': abs(min(max_drawdown_incl_values)) * 100}

    @staticmethod
    def compute_calmar_ratio(excess_returns, max_drawdown):

        calmar_ratio_no_signals = excess_returns['excess_returns_no_signals'] / max_drawdown['max_drawdown_no_signals']
        calmar_ratio_with_signals = excess_returns['excess_returns_with_signals'] / max_drawdown['max_drawdown_with_signals']

        return {'calmar_ratio_no_sigals': calmar_ratio_no_signals,
                'calmar_ratio_with_signals': calmar_ratio_with_signals}

    def compute_equity_correlation(self):
        pass

    def compute_gbi_em_correlation(self):
        pass

    def run_compute_risk_return_calculations(self, returns_excl_signals, returns_incl_signals):
        excess_returns = self.compute_excess_returns(returns_excl_signals=returns_excl_signals,
                                                     returns_incl_signals=returns_incl_signals)

        std_dev = self.compute_std_dev(returns_excl_signals=returns_excl_signals,
                                       returns_incl_signals=returns_incl_signals)

        sharpe_ratio = self.compute_sharpe_ratio(std_dev=std_dev, excess_returns=excess_returns)

        max_drawdown = self.compute_max_drawdown(returns_excl_signals=returns_excl_signals,
                                                 returns_incl_signals=returns_incl_signals)

        calmar_ratio = self.compute_calmar_ratio(excess_returns=excess_returns, max_drawdown=max_drawdown)






        return {'excess_returns': excess_returns, 'std_dev': std_dev, 'sharpe_ratio': sharpe_ratio,
                'max_drawdown': max_drawdown, 'calmar_ratio': calmar_ratio}

