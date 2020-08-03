import pandas as pd


class ComputeProfitAndLoss:

    def __init__(self, latest_date):
        self.latest_date = latest_date

    def compute_profit_and_loss_combo(self, combo):

        return combo.loc[self.latest_date]

    def compute_profit_and_loss_returns(self, returns_ex_costs):

        profit_and_loss_returns = returns_ex_costs / returns_ex_costs.shift(1)
        profit_and_loss_returns = profit_and_loss_returns.apply(lambda x: x - 1)

        return profit_and_loss_returns.apply(lambda x: x * 100).loc[self.latest_date]

    def compute_profit_and_loss_spot(self, spot, combo):
        profit_and_loss_spot = spot / spot.shift(1)
        profit_and_loss_spot = profit_and_loss_spot.apply(lambda x: x - 1)
        profit_and_loss_spot = profit_and_loss_spot.apply(lambda x: x * 100).loc[self.latest_date]
        profit_and_loss_spot = pd.Series(profit_and_loss_spot.values * combo.values)

        return profit_and_loss_spot

    @staticmethod
    def compute_profit_and_loss_carry(profit_and_loss_returns, profit_and_loss_spot):

        profit_and_loss_carry = profit_and_loss_returns.values - profit_and_loss_spot.values

        return pd.DataFrame(profit_and_loss_carry)[0]

    def compute_profit_and_loss_notional(self, spot_overview, returns_overview, combo_overview, returns, spot):
        last_year = pd.to_datetime("31-12-{}".format((self.latest_date - pd.DateOffset(years=1)).year))

        # YTD P&L:: Total (Returns)
        numerator_returns = returns.loc[self.latest_date].values
        denominator_returns = returns.loc[last_year].values
        ytd_total = 10000 * ((numerator_returns / denominator_returns) - 1)

        # YTD P&L: Spot
        numerator_spot = spot.loc[self.latest_date].values
        denominator_spot = spot.loc[last_year].values
        ytd_spot = 10000 * ((numerator_spot / denominator_spot) - 1)

        # YTD P&L: Carry
        ytd_carry = ytd_total - ytd_spot

        # Weekly P&L: Total (Returns)
        sum_prod = returns_overview.values.dot(abs(combo_overview.values)) / 100
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

    def compute_profit_and_loss_implemented_in_matr(self):
        pass

    def run_profit_and_loss(self, combo, returns_ex_costs, spot, total_incl_signals, spot_incl_signals):

        profit_and_loss_combo_overview = self.compute_profit_and_loss_combo(combo=combo)
        profit_and_loss_returns_ex_overview = self.compute_profit_and_loss_returns(returns_ex_costs=returns_ex_costs)
        profit_and_loss_spot_overview = self.compute_profit_and_loss_spot(spot=spot, combo=profit_and_loss_combo_overview)

        profit_and_loss_carry_overview = self.compute_profit_and_loss_carry(profit_and_loss_returns=profit_and_loss_returns_ex_overview,
                                                                            profit_and_loss_spot=profit_and_loss_spot_overview)

        profit_and_loss_notional = self.compute_profit_and_loss_notional(spot_overview=profit_and_loss_spot_overview,
                                                                         returns_overview=profit_and_loss_returns_ex_overview,
                                                                         combo_overview=profit_and_loss_combo_overview,
                                                                         returns=total_incl_signals,
                                                                         spot=spot_incl_signals)

        profit_and_loss_overview = {'profit_and_loss_combo_overview': profit_and_loss_combo_overview,
                                    'profit_and_loss_returns_ex_overview': profit_and_loss_returns_ex_overview,
                                    'profit_and_loss_spot_ex_overview': profit_and_loss_spot_overview,
                                    'profit_and_loss_carry_overview': profit_and_loss_carry_overview,
                                    'profit_and_loss_returns_notional': profit_and_loss_notional
                                    }

        return profit_and_loss_overview
