import os
import datetime as dt

from sqlalchemy import text

import assetallocation_UI.aa_web_app.service.strategy as s
from assetallocation_arp.data_etl.dal.data_models.strategy import Times
from assetallocation_arp.data_etl.dal.data_models.asset import TimesAssetInput
from assetallocation_arp.common_libraries.dal_enums.asset import Equity
from assetallocation_arp.data_etl.dal.arp_proc_caller import ArpProcCaller


def test_re_run_strategy_returns_same_results():
    # set up
    fund_name = 'test_fund'
    strategy_weight = 0.1
    strategy = Times(2, 'weekly', 'e', [30, 60, 120], [15, 30, 60], 2, 90)
    strategy.asset_inputs = [TimesAssetInput(Equity['DM Equity'], 1, 'F25915Y Index', 'SPXT Index', 0.5)]
    user_id = os.environ.get('USERNAME')
    business_date_from = dt.date(2018, 1, 1)
    business_date_to = dt.date(2020, 1, 1)

    # test
    fs1 = s.run_strategy(fund_name, strategy_weight, strategy, user_id, business_date_from, business_date_to, True)
    fs2 = s.run_strategy(fund_name, strategy_weight, strategy, user_id, business_date_from, business_date_to, False)

    for a1, a2 in zip(fs1.analytics, fs2.analytics):
        assert a1.business_date == a2.business_date
        assert a1.value == a2.value

    for w1, w2 in zip(fs1.asset_weights, fs2.asset_weights):
        assert w1.business_date == w2.business_date
        assert w1.strategy_weight == w2.strategy_weight

    # tear down
    del_strategy = text("""
    DELETE FROM arp.strategy s
    USING arp.times t
    WHERE 
      s.id = t.strategy_id
      AND t.version = :strategy_version
    """)
    with ArpProcCaller().engine.connect() as connection:
        connection.execute(del_strategy, {'strategy_version': strategy.version})


def test_select_fund_strategy_results_correct_number_of_weights_after_re_running_strategy_overlapping_dates():
    # set up
    fund_name = 'test_fund'
    strategy_weight = 0.1
    strategy = Times(2, 'weekly', 'e', [30, 60, 120], [15, 30, 60], 2, 90)
    strategy.asset_inputs = [TimesAssetInput(Equity['DM Equity'], 1, 'F25915Y Index', 'SPXT Index', 0.5)]
    user_id = os.environ.get('USERNAME')
    business_date_from = dt.date(2018, 1, 1)
    business_date_to1 = dt.date(2020, 1, 1)
    business_date_to2 = dt.date(2020, 2, 1)
    s.run_strategy(fund_name, strategy_weight, strategy, user_id, business_date_from, business_date_to1, True)
    s.run_strategy(fund_name, strategy_weight, strategy, user_id, business_date_from, business_date_to2, False)

    # test
    fs = ArpProcCaller().select_fund_strategy_results(fund_name, strategy.name, strategy.version, business_date_from, business_date_to2)

    assert (business_date_to2 - business_date_from).days == len(fs.asset_weights)

    # tear down
    del_strategy = text("""
    DELETE FROM arp.strategy s
    USING arp.times t
    WHERE 
      s.id = t.strategy_id
      AND t.version = :strategy_version
    """)
    with ArpProcCaller().engine.connect() as connection:
        connection.execute(del_strategy, {'strategy_version': strategy.version})
