import enum


class CurrencySpot(enum.Enum):
    """
    Class enum which creates names for dataframe columns
    """
    Inflation_Differential = 'Inflation_Differential_'
    Inflation_Release = "Inflation_Release"
    Carry = 'Carry_'
    Trend = 'Trend_'
    Combo = 'Combo_'
    Return_Ex_Costs = 'Return_Ex_Costs_'
    Return_Incl_Costs = 'Return_Incl_Costs_'
    Spot_Ex_Costs = 'Spot_Ex_Costs_'
    Spot_Incl_Costs = 'Spot_Incl_Costs_'


class CurrencyAggregate(enum.Enum):
    Total_Incl_Signals = 'Total_Incl_Signals'
    Total_Excl_Signals = 'Total_Excl_Signals'
    Spot_Incl_Signals = 'Spot_Incl_Signals'
    Spot_Excl_Signals = 'Spot_Excl_Signals'
    Weighted_Performance = 'Weighted_Performance'
    Inverse_Volatility = 'Inverse_Volatility_'







