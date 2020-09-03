import pandas as pd


class ComputeProfitAndLoss:

    def __init__(self, latest_date, position_size_attribution, index_dates):
        self.latest_date = latest_date
        self.position_size_attribution = position_size_attribution
        self.index_dates = index_dates

    def compute_profit_and_loss_combo(self, combo_curr):
        """
        Function computing the last week of the profit and loss overview
        :param combo_curr: combo data of all currencies from compute_currencies.py
        :return: a dataFrame with the combo of all currencies at the latest date
        """
        print('compute_profit_and_loss_combo')
        return combo_curr.loc[self.latest_date]

    def compute_profit_and_loss_total(self, returns_ex_costs):
        """
        Function computing the Total (returns) of profit an loss overview
        :param returns_ex_costs: returns exclude costs of all currencies
        :return:a dataFrame of the returns of all currencies at the latest date
        """
        print('compute_profit_and_loss_total')
        profit_and_loss_returns = returns_ex_costs / returns_ex_costs.shift(1)
        profit_and_loss_returns = profit_and_loss_returns.apply(lambda x: x - 1)

        return profit_and_loss_returns.apply(lambda x: x * 100).loc[self.latest_date]

    def compute_profit_and_loss_spot(self, spot_origin, combo_overview):
        """
        Function computing the Spot of profit and loss overview
        :param spot_origin: spot of all currencies
        :param combo_overview: combo from compute_profit_and_loss_combo function
        :return: a dataFrame of the spot of all currencies at the latest date
        """
        print('compute_profit_and_loss_spot')
        profit_and_loss_spot = spot_origin / spot_origin.shift(1)
        profit_and_loss_spot = profit_and_loss_spot.apply(lambda x: x - 1)
        profit_and_loss_spot = profit_and_loss_spot.apply(lambda x: x * 100).loc[self.latest_date]
        profit_and_loss_spot = pd.Series(profit_and_loss_spot.values * combo_overview.values)

        return profit_and_loss_spot

    @staticmethod
    def compute_profit_and_loss_carry(profit_and_loss_total, profit_and_loss_spot):
        """
        Function computing the carry of all currencies according to the returns and spot profit and loss overview
        :param profit_and_loss_total: returns of profit and loss overview for all currencies
        :param profit_and_loss_spot: spot of profit and loss overview for all currencies
        :return: a dataFrame of carry of all currencies
        """
        print('compute_profit_and_loss_carry')
        profit_and_loss_carry = profit_and_loss_total.values - profit_and_loss_spot.values

        return pd.DataFrame(profit_and_loss_carry)[0]

    def compute_profit_and_loss_notional(self, spot_overview, total_overview, combo_overview, total_incl_signals, spot_incl_signals):
        """
        Function calculating the profit and loss notional (bp) of the spot, returns and carry
        :param spot_overview: spot overview data of all currencies
        :param total_overview: returns overview data of all currencies
        :param combo_overview: combo overview of all currencies
        :param total_incl_signals: returns data from aggregate currencies (compute_aggregate_total_incl_signals)
        :param spot_incl_signals: spot data from aggregate currencies (compute_aggregate_spot_incl_signals)
        :return: a dictionary of profit and loss ytd and weekly
        """
        print('compute_profit_and_loss_notional')
        #todo ajouter fct Laura pour work day
        last_year = pd.to_datetime("31-12-{}".format((self.latest_date - pd.DateOffset(years=1)).year))

        # YTD P&L:: Total (Returns)
        numerator_returns = total_incl_signals.loc[self.latest_date].values[0]
        denominator_returns = total_incl_signals.loc[last_year].values[0]
        ytd_total = 10000 * ((numerator_returns / denominator_returns) - 1)

        # YTD P&L: Spot
        numerator_spot = spot_incl_signals.loc[self.latest_date].values[0]
        denominator_spot = spot_incl_signals.loc[last_year].values[0]
        ytd_spot = 10000 * ((numerator_spot / denominator_spot) - 1)

        # YTD P&L: Carry
        ytd_carry = ytd_total - ytd_spot

        # Weekly P&L: Total (Returns)
        sum_prod = total_overview.values.dot(abs(combo_overview.values)) / 100
        length = combo_overview.shape[0]
        weekly_returns = 10000 * (sum_prod / length)

        # Weekly P&L: Spot
        sum_prod = spot_overview.values.dot(abs(combo_overview.values)) / 100
        weekly_spot = 10000 * (sum_prod / length)

        # Weekly P&L: Carry
        weekly_carry = weekly_returns - weekly_spot

        return {'profit_and_loss_total_ytd_notional': ytd_total,
                'profit_and_loss_spot_ytd_notional': ytd_spot,
                'profit_and_loss_carry_ytd_notional': ytd_carry,
                'profit_and_loss_total_weekly_notional': weekly_returns,
                'profit_and_loss_spot_weekly_notional': weekly_spot,
                'profit_and_loss_carry_weekly_notional': weekly_carry}

    def compute_profit_and_loss_implemented_in_matr(self, combo_overview, ytd_total_notional, ytd_spot_notional, weekly_total_notional, weekly_spot_notional, weighted_perf):
        """
        Function calculating the profit and loss implemented in matr
        :param combo_overview: combo overview from profit and loss notional overview
        :param ytd_total_notional: ytd returns from profit and loss notional overview
        :param ytd_spot_notional: ytd spot from profit and loss notional overview
        :param weekly_total_notional: weekly returns from profit and loss notional overview
        :param weekly_spot_notional: weekly spot from profit and loss notional overview
        :param weighted_perf: weighted performance data
        :return: a dictionary of profit and loss implemented in MATR
        """
        print('compute_profit_and_loss_implemented_in_matr')
        # YTD P&L:: Total (Returns)
        ytd_total_matr = (weighted_perf.loc[self.latest_date][0]/100) * 10000

        # YTD P&L: Spot
        ytd_spot_matr = ytd_total_matr * (ytd_spot_notional / ytd_total_notional)

        # YTD P&L: Carry
        ytd_carry_matr = ytd_total_matr - ytd_spot_matr

        # Weekly P&L: Total (Returns)
        weekly_returns_matr = combo_overview.shape[0] * weekly_total_notional * self.position_size_attribution

        # Weekly P&L: Spot
        weekly_spot_matr = combo_overview.shape[0] * weekly_spot_notional * self.position_size_attribution

        # Weekly P&L: Carry
        weekly_carry_matr = weekly_returns_matr - weekly_spot_matr

        return {'profit_and_loss_total_ytd_matr': ytd_total_matr, 'profit_and_loss_spot_ytd_matr': ytd_spot_matr,
                'profit_and_loss_carry_ytd_matr': ytd_carry_matr, 'profit_and_loss_total_weekly_matr': weekly_returns_matr,
                'profit_and_loss_spot_weekly_matr': weekly_spot_matr, 'profit_and_loss_carry_weekly_matr': weekly_carry_matr }

    def run_profit_and_loss(self, combo_curr, returns_ex_costs, spot_origin, total_incl_signals, spot_incl_signals, weighted_perf):

        profit_and_loss_combo_overview = self.compute_profit_and_loss_combo(combo_curr=combo_curr)
        profit_and_loss_total_overview = self.compute_profit_and_loss_total(returns_ex_costs=returns_ex_costs)
        profit_and_loss_spot_overview = self.compute_profit_and_loss_spot(spot_origin=spot_origin,
                                                                          combo_overview=profit_and_loss_combo_overview)
        profit_and_loss_carry_overview = self.compute_profit_and_loss_carry(profit_and_loss_total=profit_and_loss_total_overview,
                                                                            profit_and_loss_spot=profit_and_loss_spot_overview)

        profit_and_loss_notional = self.compute_profit_and_loss_notional(spot_overview=profit_and_loss_spot_overview,
                                                                         total_overview=profit_and_loss_total_overview,
                                                                         combo_overview=profit_and_loss_combo_overview,
                                                                         total_incl_signals=total_incl_signals,
                                                                         spot_incl_signals=spot_incl_signals)

        profit_and_loss_matr = self.compute_profit_and_loss_implemented_in_matr(combo_overview=profit_and_loss_combo_overview,
                                                                                ytd_total_notional=profit_and_loss_notional['profit_and_loss_total_ytd_notional'],
                                                                                ytd_spot_notional=profit_and_loss_notional['profit_and_loss_spot_ytd_notional'],
                                                                                weekly_total_notional=profit_and_loss_notional['profit_and_loss_total_weekly_notional'],
                                                                                weekly_spot_notional=profit_and_loss_notional['profit_and_loss_spot_weekly_notional'],
                                                                                weighted_perf=weighted_perf)

        profit_and_loss_overview = {'profit_and_loss_combo_overview': profit_and_loss_combo_overview.values,
                                    'profit_and_loss_total_overview': profit_and_loss_total_overview.values,
                                    'profit_and_loss_spot_ex_overview': profit_and_loss_spot_overview.values,
                                    'profit_and_loss_carry_overview': profit_and_loss_carry_overview.values,
                                    'profit_and_loss_notional': profit_and_loss_notional,
                                    'profit_and_loss_matr': profit_and_loss_matr
                                    }

        return profit_and_loss_overview
