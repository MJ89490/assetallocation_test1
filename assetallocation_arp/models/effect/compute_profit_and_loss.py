import common_libraries.names_all_currencies as currency_names
from assetallocation_arp.common_libraries.names_columns_calculations import CurrencySpot


class ComputeProfitAndLoss:

    def __init__(self, latest_date):
        self.latest_date = latest_date


    # @property
    # def latest_date_previous(self):
    #     latest_date_index_loc = self.index_currencies.index.get_loc(self.latest_date)
    #     previous_latest_date_index = self.index_currencies.index[latest_date_index_loc - 1]
    #
    #     return previous_latest_date_index

    def compute_profit_and_loss_returns(self, returns_ex_costs):

        profit_and_loss_returns = returns_ex_costs / returns_ex_costs.shift(1)
        profit_and_loss_returns = profit_and_loss_returns.apply(lambda x: x - 1)

        return profit_and_loss_returns.apply(lambda x: x * 100).loc[self.latest_date]

    def compute_profit_and_loss_spot(self, spot_ex_costs):

        profit_and_loss_spot = spot_ex_costs / spot_ex_costs.shift(1)
        profit_and_loss_spot = profit_and_loss_spot.apply(lambda x: x - 1)

        return profit_and_loss_spot.apply(lambda x: x * 100).loc[self.latest_date]

    def compute_profit_and_loss_carry(self, profit_and_loss_returns, profit_and_loss_spot):

        profit_and_loss_carry = profit_and_loss_returns.sub(profit_and_loss_spot)

        return profit_and_loss_carry.apply(lambda x: x * 100)
