import os
import numpy as np
import pandas as pd

from unittest import TestCase

from assetallocation_arp.models.effect.compute_currencies import ComputeCurrencies
from assetallocation_arp.models.effect.compute_signals_overview import ComputeSignalsOverview
from data_etl.inputs_effect.compute_inflation_differential import ComputeInflationDifferential
from assetallocation_arp.models.effect.compute_aggregate_currencies import ComputeAggregateCurrencies

"""
Notes: 
    TrendIndicator: Total Return
    Short-term: 4
    Long-term: 16 
    Incl Shorts: Yes
    Cut-off long: 2.0% 
    Cut-off short: 0.0% 
    Real/Nominal: real
    Realtime Inflation F'cast: Yes
    Threshold for closing: 0.25%
    Risk-weighting: 1/N
    STDev window (weeks): 52
    Bid-ask spread (bp): 10
    Position size: 3%
"""


class TestComputeAggregateCurrencies(TestCase):

    def setUp(self):
        all_data = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "all_date.csv")), sep=',', engine='python')
        all_data = all_data.set_index(pd.to_datetime(all_data.Date, format='%Y-%m-%d'))
        del all_data['Date']
        self.obj_import_data = ComputeCurrencies(asset_inputs=pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "asset_inputs.csv")), sep=',', engine='python'),
                                                 bid_ask_spread=10,
                                                 frequency_mat='weekly',
                                                 end_date_mat='23/09/2020',
                                                 signal_day_mat='WED',
                                                 all_data=all_data)
        self.obj_import_data.process_all_data_effect()
        self.spot_origin, self.carry_origin, spx_index_values, three_month_implied_usd, three_month_implied_eur, region, jgenvuug_index_values = self.obj_import_data.return_process_usd_eur_data_effect()

        self.obj_import_data.start_date_calculations = pd.to_datetime('12-01-2000', format='%d-%m-%Y')

        # Inflation differential calculations
        obj_inflation_differential = ComputeInflationDifferential(dates_index=self.obj_import_data.dates_index)
        realtime_inflation_forecast, imf_data_update = 'Yes', False
        inflation_differential, currency_logs = obj_inflation_differential.compute_inflation_differential(
                                                realtime_inflation_forecast,
                                                self.obj_import_data.all_currencies_spot,
                                                self.obj_import_data.currencies_spot['currencies_spot_usd'],
                                                imf_data_update=imf_data_update)

        latest_signal_date = pd.to_datetime('23-09-2020', format='%d-%m-%Y')
        self.trend_inputs = {'short_term': 4, 'long_term': 16, 'trend': 'total return'}
        self.carry_inputs = {'type': 'real', 'inflation': inflation_differential}
        self.combo_inputs = {'cut_off': 2, 'incl_shorts': 'Yes', 'cut_off_s': 0.00, 'threshold': 0.25}

        self.currencies_calculations = self.obj_import_data.run_compute_currencies(self.carry_inputs, self.trend_inputs, self.combo_inputs)

        self.obj_compute_agg_currencies = ComputeAggregateCurrencies(window=52,
                                                                     weight='1/N',
                                                                     dates_index=self.obj_import_data.dates_index,
                                                                     start_date_calculations=self.obj_import_data.start_date_calculations,
                                                                     prev_start_date_calc=self.obj_import_data.previous_start_date_calc)

        self.obj_compute_signals_overview = ComputeSignalsOverview(latest_signal_date=latest_signal_date,
                                                                   size_attr=0.03,
                                                                   window=52,
                                                                   next_latest_date=self.obj_import_data)

    def test_compute_signals_real_carry(self):
        signals_carry = self.obj_compute_signals_overview.compute_signals_real_carry(self.currencies_calculations['carry_curr'])

        assert np.allclose(np.array(signals_carry.item()), np.array(-0.035424500000))

    def test_compute_signals_trend(self):
        signals_trend = self.obj_compute_signals_overview.compute_signals_trend(self.currencies_calculations['trend_curr'])

        assert np.allclose(np.array(signals_trend.item()), np.array(-0.6946033067203320000))

    def test_compute_signals_combo(self):
        signals_combo = self.obj_compute_signals_overview.compute_signals_trend(self.currencies_calculations['combo_curr'])

        assert signals_combo.item() == -1

    def test_compute_drawdown_position_size_matr(self):
        agg_total_incl_signals = self.obj_compute_agg_currencies.compute_aggregate_total_incl_signals(self.currencies_calculations['return_incl_curr'], inverse_volatility=None)

        res = self.obj_compute_signals_overview.compute_drawdown_position_size_matr(agg_total_incl_signals)

        assert np.allclose(np.array([res['drawdown'], res['size_matr']]), np.array([-6.168478116205640000, 3.00]))

    def test_compute_limits_controls(self):
        signals_combo = self.obj_compute_signals_overview.compute_signals_trend(self.currencies_calculations['combo_curr'])
        agg_log_returns = self.obj_compute_agg_currencies.compute_excl_signals_total_return(self.carry_origin)
        limits = self.obj_compute_signals_overview.compute_limits_controls(signals_combo, agg_log_returns)

        assert np.allclose(np.array([limits['ex_ante_vol'], limits['matr_notional']]), np.array([673.0302687471427, -3.00]))
