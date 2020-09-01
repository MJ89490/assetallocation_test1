from enum import Enum, auto


# noinspection PyArgumentList
Proc = Enum(
    value='Proc',
    names=[
        ('fund.select_fund', auto()),
        ('fund.insert_fund', auto()),
        ('arp.select_fund_strategy_results', auto()),
        ('arp.insert_fund_strategy_results', auto()),
        ('arp.insert_app_user', auto()),
        ('arp.select_strategy_versions', auto()),
        ('fund.select_fund_names', auto()),
    ]
)

# noinspection PyArgumentList
TimesProc = Enum(
    value='Proc',
    names=[
        ('arp.select_times_strategy', auto()),
        ('arp.insert_times_strategy', auto()),
        ('arp.select_times_assets', auto()),
        ('arp.insert_times_assets', auto()),
        ('arp.select_times_assets_with_analytics', auto())
    ]
)

# noinspection PyArgumentList
EffectProc = Enum(
    value='Proc',
    names=[
        ('arp.select_effect_strategy', auto()),
        ('arp.insert_effect_strategy', auto()),
        ('arp.select_effect_assets', auto()),
        ('arp.insert_effect_assets', auto()),
        ('arp.select_effect_assets_with_analytics', auto()),
    ]
)