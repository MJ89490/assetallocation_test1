from enum import Enum, auto

from assetallocation_arp.common_libraries.dal_enums.strategy import Name

# noinspection PyArgumentList
ArpProc = Enum(
    value='ArpProc',
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


class StrategyProcFactory:
    # noinspection PyArgumentList
    @staticmethod
    def get_strategy_proc(strategy_name: Name):
        return Enum(
            value=f'{strategy_name.name.capitalize()}Proc',
            names=[
                (f'arp.select_{strategy_name.name}_strategy', auto()),
                (f'arp.insert_{strategy_name.name}_strategy', auto()),
                (f'arp.select_{strategy_name.name}_assets', auto()),
                (f'arp.insert_{strategy_name.name}_assets', auto()),
                (f'arp.select_{strategy_name.name}_assets_with_analytics', auto())
            ]
        )