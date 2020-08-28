from typing import List

from assetallocation_arp.data_etl.dal.arp_proc_caller import ArpProcCaller


def get_fund_names() -> List[str]:
    apc = ArpProcCaller()
    return apc.select_fund_names()
