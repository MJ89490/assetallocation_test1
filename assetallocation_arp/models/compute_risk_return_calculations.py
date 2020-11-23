import numpy
from math import sqrt


class ComputeRiskReturnCalculations:

    def __init__(self, start_date, end_date, dates_index):
        self.start_date = start_date
        self.end_date = end_date
        self.dates_index = dates_index

    def compute_excess_returns(self, returns_excl_signals, returns_incl_signals):
        """
        Function computing the excess returns
        :param returns_excl_signals: returns_excl_signals values
        :param returns_incl_signals: returns_incl_signals values
        :return: a dictionary with excess returns having no signals and with signal
        """

        exp = 365 / (self.end_date - self.start_date).days

        excess_returns_no_signals = (((returns_excl_signals.loc[self.end_date][0] / returns_excl_signals.loc[self.start_date][0]) ** exp) - 1) * 100
        excess_returns_with_signals = (((returns_incl_signals.loc[self.end_date][0] / returns_incl_signals.loc[self.start_date][0]) ** exp) - 1) * 100

        return {'excess_returns_no_signals': round(excess_returns_no_signals, 2),
                'excess_returns_with_signals': round(excess_returns_with_signals, 2)}

    @staticmethod
    def compute_std_dev(returns_excl_signals, returns_incl_signals):
        """
        Function computing the standard deviation
        :param returns_excl_signals: returns_excl_signals values
        :param returns_incl_signals: returns_incl_signals values
        :return: a dictionary with standard deviation having no signals and with signal
        """

        std_dev_no_signals = (returns_excl_signals / returns_excl_signals.shift(1)).std()[0] * sqrt(52) * 100
        std_dev_with_signals = (returns_incl_signals / returns_incl_signals.head(-1).shift(1)).std()[0] * sqrt(52) * 100

        return {'std_dev_no_signals': round(std_dev_no_signals, 2),
                'std_dev_with_signals': round(std_dev_with_signals, 2)}

    @staticmethod
    def compute_sharpe_ratio(excess_returns, std_dev):
        """
        Function computing the sharpe ratio
        :param excess_returns: excess_returns values
        :param std_dev: std_dev values
        :return: a dictionary with sharpe ratio having no signals and with signal
        """

        sharpe_ratio_no_signals = excess_returns['excess_returns_no_signals'] / std_dev['std_dev_no_signals']
        sharpe_ratio_with_signals = excess_returns['excess_returns_with_signals'] / std_dev['std_dev_with_signals']

        return {'sharpe_ratio_no_signals': round(sharpe_ratio_no_signals, 2),
                'sharpe_ratio_with_signals': round(sharpe_ratio_with_signals, 2)}

    @staticmethod
    def compute_max_drawdown(returns_excl_signals, returns_incl_signals, jgenvuug_index_values):
        """
        Function computing the max drawdown
        :param returns_excl_signals: returns_excl_signals values
        :param returns_incl_signals: returns_incl_signals values
        :return: a dictionary with max drawdown having no signals and with signal
        """

        returns_excl_tmp = returns_excl_signals.Total_Excl_Signals.to_list()
        returns_incl_tmp = returns_incl_signals.Total_Incl_Signals.tolist()

        jgenvuug_index_tmp = jgenvuug_index_values[returns_excl_signals.first_valid_index():
                                                   returns_excl_signals.last_valid_index()].tolist()

        jgenvuug_index_tmp = [0 if str(val) == 'nan' else val for val in jgenvuug_index_tmp]

        drawdown_dates = returns_excl_signals.index.strftime("%Y-%m-%d").to_list()

        max_drawdown_excl_values, max_drawdown_incl_values, max_drawdown_index_values = [], [], []

        for value in range(len(returns_excl_tmp)):

            max_drawdown_excl_values.append((returns_excl_tmp[value] / max(returns_excl_tmp[0: value+1])) - 1)
            max_drawdown_incl_values.append((returns_incl_tmp[value] / max(returns_incl_tmp[0: value+1])) - 1)
            max_drawdown_index_values.append((jgenvuug_index_tmp[value] / max(jgenvuug_index_tmp[0: value + 1])) - 1)
            
        return {'max_drawdown_no_signals': round(abs(min(max_drawdown_excl_values)) * 100, 2),
                'max_drawdown_with_signals': round(abs(min(max_drawdown_incl_values)) * 100, 2),
                'all_max_drawdown_no_signals_series': max_drawdown_excl_values,
                'all_max_drawdown_with_signals_series': max_drawdown_incl_values,
                'all_max_drawdown_jgenvuug': max_drawdown_index_values,
                'drawdown_dates': drawdown_dates}

    @staticmethod
    def compute_calmar_ratio(excess_returns, max_drawdown):
        """
        Function computing the calmar ratio
        :param excess_returns: excess_returns values
        :param max_drawdown: max_drawdown values
        :return: a dictionary with calmar ratio having no signals and with signal
        """

        calmar_ratio_no_signals = excess_returns['excess_returns_no_signals'] / max_drawdown['max_drawdown_no_signals']
        calmar_ratio_with_signals = excess_returns['excess_returns_with_signals'] / max_drawdown['max_drawdown_with_signals']

        return {'calmar_ratio_no_signals': round(calmar_ratio_no_signals, 2),
                'calmar_ratio_with_signals': round(calmar_ratio_with_signals, 2)}

    @staticmethod
    def compute_equity_correlation(spx_index_values, returns_excl_signals, returns_incl_signals):
        """
        Function computing the equity correlation
        :param spx_index_values: excess_returns values
        :param returns_excl_signals: returns_excl_signals values
        :param returns_incl_signals: returns_incl_signals values
        :return: a dictionary with equity correlation having no signals and with signal
        """

        ret_excl_shift = (returns_excl_signals / returns_excl_signals.shift(1)).iloc[1:]
        ret_incl_shift = (returns_incl_signals / returns_incl_signals.shift(1)).iloc[1:]
        spxt_shift = (spx_index_values / spx_index_values.shift(1)).iloc[1:]

        equity_corr_no_signals = ret_excl_shift.corrwith(spxt_shift, axis=0)
        equity_corr_with_signals = ret_incl_shift.corrwith(spxt_shift, axis=0)

        return {'equity_corr_no_signals': round(equity_corr_no_signals.item(), 2),
                'equity_corr_with_signals': round(equity_corr_with_signals.item(), 2)}

    def compute_gbi_em_correlation(self):
        """
        Function will be added later
        :return:
        """
        pass

    def run_compute_risk_return_calculations(self, returns_excl_signals, returns_incl_signals, spxt_index_values,
                                             jgenvuug_index_values):
        """
        Function calling the functions above
        :param returns_excl_signals: returns_excl_returns_excl_signals values
        :param returns_incl_signals: returns_incl_signals values
        :param spxt_index_values: spxt_index_values values
        :return: a dictionary
        """
        excess_returns = self.compute_excess_returns(returns_excl_signals=returns_excl_signals,
                                                     returns_incl_signals=returns_incl_signals)

        std_dev = self.compute_std_dev(returns_excl_signals=returns_excl_signals,
                                       returns_incl_signals=returns_incl_signals)

        sharpe_ratio = self.compute_sharpe_ratio(std_dev=std_dev, excess_returns=excess_returns)

        max_drawdown = self.compute_max_drawdown(returns_excl_signals=returns_excl_signals,
                                                 returns_incl_signals=returns_incl_signals,
                                                 jgenvuug_index_values=jgenvuug_index_values)

        calmar_ratio = self.compute_calmar_ratio(excess_returns=excess_returns, max_drawdown=max_drawdown)

        equity_corr = self.compute_equity_correlation(spxt_index_values, returns_excl_signals, returns_incl_signals)

        return {'excess_returns': excess_returns, 'std_dev': std_dev, 'sharpe_ratio': sharpe_ratio,
                'max_drawdown': max_drawdown, 'calmar_ratio': calmar_ratio, 'equity_corr': equity_corr}
