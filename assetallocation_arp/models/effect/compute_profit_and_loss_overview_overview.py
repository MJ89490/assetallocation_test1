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

    def run_profit_and_loss(self, combo, returns_ex_costs, spot):

        profit_and_loss_combo_overview = self.compute_profit_and_loss_combo(combo=combo)
        profit_and_loss_returns_ex_overview = self.compute_profit_and_loss_returns(returns_ex_costs=returns_ex_costs)
        profit_and_loss_spot_overview = self.compute_profit_and_loss_spot(spot=spot, combo=profit_and_loss_combo_overview)

        profit_and_loss_carry_overview = self.compute_profit_and_loss_carry(profit_and_loss_returns=profit_and_loss_returns_ex_overview,
                                                                            profit_and_loss_spot=profit_and_loss_spot_overview)

        profit_and_loss_overview = {'profit_and_loss_combo_overview': profit_and_loss_combo_overview,
                                    'profit_and_loss_returns_ex_overview': profit_and_loss_returns_ex_overview,
                                    'profit_and_loss_spot_ex_overview': profit_and_loss_spot_overview,
                                    'profit_and_loss_carry_overview': profit_and_loss_carry_overview
                                    }

        return profit_and_loss_overview
