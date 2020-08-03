from enum import Enum, auto

Proc = Enum(
    value='Proc',
    names=[
        ('fund.select_fund', auto()),
        ('fund.insert_fund', auto()),
        ('arp.select_fund_strategy_results', auto()),
        ('arp.insert_fund_strategy_results', auto()),
        ('arp.insert_effect_strategy', auto()),
        ('arp.insert_fica_strategy', auto()),
        ('arp.insert_times_strategy', auto()),
        ('arp.select_times_strategy', auto()),
        ('arp.select_times_assets', auto()),
    ]
)