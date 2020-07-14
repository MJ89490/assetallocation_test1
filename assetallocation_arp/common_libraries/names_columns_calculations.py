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







