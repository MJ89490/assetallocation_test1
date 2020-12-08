import os
import numpy as np
import pandas as pd
from unittest import TestCase

from assetallocation_arp.models.compute_risk_return_calculations import ComputeRiskReturnCalculations
from assetallocation_arp.models.effect.compute_aggregate_currencies import ComputeAggregateCurrencies
from assetallocation_arp.models.effect.compute_currencies import ComputeCurrencies
from data_etl.inputs_effect.compute_inflation_differential import ComputeInflationDifferential
from assetallocation_arp.common_libraries.dal_enums.strategy import Frequency, DayOfWeek, TrendIndicator, CarryType, RiskWeighting
"""
Notes: 
    TrendIndicator: Total Return
    Short-term: 4
    Long-term: 16 
    Incl Shorts: True
    Cut-off long: 2.0% 
    Cut-off short: 0.0% 
    real/nominal: real
    Realtime Inflation F'cast: True
    Threshold for closing: 0.25%
    Risk-weighting: 1/N
    STDev window (weeks): 52
    Bid-ask spread (bp): 10
    Position size: 3%
"""


class TestComputeRiskReturnCalculations(TestCase):

    def setUp(self):
        all_data = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "all_date.csv")), sep=',', engine='python')
        all_data = all_data.set_index(pd.to_datetime(all_data.Date, format='%Y-%m-%d'))
        del all_data['Date']
        self.obj_import_data = ComputeCurrencies(asset_inputs=pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "asset_inputs.csv")), sep=',', engine='python'),
                                                 bid_ask_spread=10,
                                                 frequency_mat=Frequency.weekly,
                                                 end_date_mat=pd.to_datetime('23-09-2020', format='%d-%m-%Y'),
                                                 signal_day_mat=DayOfWeek.WED,
                                                 all_data=all_data)

        self.obj_import_data.process_all_data_effect()
        self.obj_import_data.start_date_calculations = pd.to_datetime('12-01-2000', format='%d-%m-%Y')
        self.process_usd_eur_data_effect = self.obj_import_data.process_usd_eur_data_effect()

        # Inflation differential calculations
        obj_inflation_differential = ComputeInflationDifferential(dates_index=self.obj_import_data.dates_index)
        realtime_inflation_forecast, imf_data_update = True, False
        inflation_differential, currency_logs = obj_inflation_differential.compute_inflation_differential(
                                                realtime_inflation_forecast,
                                                self.obj_import_data.all_currencies_spot,
                                                self.obj_import_data.currencies_spot['currencies_spot_usd'],
                                                imf_data_update=imf_data_update)

        # Inputs
        trend_inputs = {'short_term': 4, 'long_term': 16, 'trend': TrendIndicator['total return']}
        carry_inputs = {'type': CarryType.real, 'inflation': inflation_differential}
        combo_inputs = {'cut_off': 2, 'incl_shorts': True, 'cut_off_s': 0.00, 'threshold': 0.25}

        self.currencies_calculations = self.obj_import_data.run_compute_currencies(carry_inputs, trend_inputs, combo_inputs)
        self.obj_compute_agg_currencies = ComputeAggregateCurrencies(window=52,
                                                                     weight=RiskWeighting['1/N'],
                                                                     dates_index=self.obj_import_data.dates_index,
                                                                     start_date_calculations=self.obj_import_data.start_date_calculations,
                                                                     prev_start_date_calc=self.obj_import_data.previous_start_date_calc)

        total_incl = self.obj_compute_agg_currencies.compute_aggregate_total_incl_signals(self.currencies_calculations['return_incl_curr'], inverse_volatility=None)
        ret_excl_costs = self.obj_compute_agg_currencies.compute_excl_signals_total_return(self.process_usd_eur_data_effect['common_carry'])
        total_excl = self.obj_compute_agg_currencies.compute_aggregate_total_excl_signals(ret_excl_costs, inverse_volatility=None)
        self.returns_excl_signals = total_excl.head(-1)
        self.returns_incl_signals = total_incl.head(-1)

        self.compute_risk_ret = ComputeRiskReturnCalculations(start_date=self.obj_import_data.start_date_prev_calculations,
                                                              end_date=pd.to_datetime('23-09-2020', format='%d-%m-%Y'),
                                                              dates_index=self.obj_import_data.dates_origin_index)

    def test_compute_excess_returns(self):
        # Excess returns
        excess_ret = self.compute_risk_ret.compute_excess_returns(self.returns_excl_signals, self.returns_incl_signals)

        assert np.allclose(np.array([excess_ret['excess_returns_no_signals'],
                                     excess_ret['excess_returns_with_signals']]),
                           np.array([3.84572606745583000, 10.068448229337900000]))

    def test_compute_std_dev(self):
        # Standard deviation
        std_dev = self.compute_risk_ret.compute_std_dev(self.returns_excl_signals, self.returns_incl_signals)

        assert np.allclose(np.array([std_dev['std_dev_no_signals'],
                                     std_dev['std_dev_with_signals']]),
                           np.array([16.68743875343896, 10.466027604266557]))

    def test_compute_sharpe_ratio(self):
        # Excess returns
        excess_ret = self.compute_risk_ret.compute_excess_returns(self.returns_excl_signals, self.returns_incl_signals)
        # Standard deviation
        std_dev = self.compute_risk_ret.compute_std_dev(self.returns_excl_signals, self.returns_incl_signals)

        sharpe_ratio = self.compute_risk_ret.compute_sharpe_ratio(excess_ret, std_dev)

        assert np.allclose(np.array([sharpe_ratio['sharpe_ratio_no_signals'],
                                     sharpe_ratio['sharpe_ratio_with_signals']]),
                           np.array([0.23045634050122574, 0.9620123899953575]))

    def test_compute_max_drawdown(self):
        max_drawdown = self.compute_risk_ret.compute_max_drawdown(self.returns_excl_signals, self.returns_incl_signals, self.process_usd_eur_data_effect['jgenvuug_index_values'])

        assert np.allclose(np.array([max_drawdown['max_drawdown_no_signals'],
                                     max_drawdown['max_drawdown_with_signals']]),
                           np.array([49.24300804033870000, 12.1652008006123000]))

    def test_compute_calmar_ratio(self):
        # Excess returns
        excess_ret = self.compute_risk_ret.compute_excess_returns(self.returns_excl_signals, self.returns_incl_signals)
        # Max draxdown
        max_drawdown = self.compute_risk_ret.compute_max_drawdown(self.returns_excl_signals, self.returns_incl_signals,
                                                                  self.process_usd_eur_data_effect['jgenvuug_index_values'])

        calmar_ratio = self.compute_risk_ret.compute_calmar_ratio(excess_ret, max_drawdown)

        assert np.allclose(np.array([calmar_ratio['calmar_ratio_no_signals'],
                                     calmar_ratio['calmar_ratio_with_signals']]),
                           np.array([0.07809689579291150000, 0.82764340633252400000]))

    def test_compute_equity_correlation(self):

        equity_corr = self.compute_risk_ret.compute_equity_correlation(self.process_usd_eur_data_effect['spxt_index_values'], self.returns_excl_signals, self.returns_incl_signals)

        assert np.allclose(np.array([equity_corr['equity_corr_no_signals'],
                                     equity_corr['equity_corr_with_signals']]),
                           np.array([0.3896184250275422, 0.19600035947809472]))

