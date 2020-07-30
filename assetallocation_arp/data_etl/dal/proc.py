from enum import Enum, auto


class Proc(Enum):
    select_fund = auto()
    insert_fund = auto()

    select_fund_strategy_results = auto()
    insert_fund_strategy_results = auto()

    insert_effect_strategy = auto()

    insert_fica_strategy = auto()

    insert_times_strategy = auto()
    select_times_strategy = auto()
    select_times_assets = auto()
