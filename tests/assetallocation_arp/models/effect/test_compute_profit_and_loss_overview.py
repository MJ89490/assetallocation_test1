import os
import numpy as np
import pandas as pd
from unittest import TestCase
from parameterized import parameterized

from assetallocation_arp.models.effect.compute_currencies import ComputeCurrencies
from data_etl.inputs_effect.compute_inflation_differential import ComputeInflationDifferential
from assetallocation_arp.models.effect.compute_profit_and_loss_overview import ComputeProfitAndLoss
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


class TestComputeProfitAndLoss(TestCase):

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

        # Inputs
        trend_inputs = {'short_term': 4, 'long_term': 16, 'trend': 'total return'}
        carry_inputs = {'type': 'real', 'inflation': inflation_differential}
        combo_inputs = {'cut_off': 2, 'incl_shorts': 'Yes', 'cut_off_s': 0.00, 'threshold': 0.25}

        self.currencies_calculations = self.obj_import_data.run_compute_currencies(carry_inputs, trend_inputs, combo_inputs)

        # Aggregate
        self.obj_compute_agg_currencies = ComputeAggregateCurrencies(window=52,
                                                                     weight='1/N',
                                                                     dates_index=self.obj_import_data.dates_index,
                                                                     start_date_calculations=self.obj_import_data.start_date_calculations,
                                                                     prev_start_date_calc=self.obj_import_data.previous_start_date_calc)

        self.obj_compute_profit_and_loss = ComputeProfitAndLoss(latest_date=pd.to_datetime('23-09-2020', format='%d-%m-%Y'),
                                                                position_size_attribution=0.03,
                                                                index_dates=self.obj_import_data.dates_origin_index,
                                                                frequency='weekly')

    def test_compute_profit_and_loss_combo(self):
        p_and_l_combo = self.obj_compute_profit_and_loss.compute_profit_and_loss_combo(self.currencies_calculations['combo_curr'])

        assert p_and_l_combo.item() == -1

    def test_compute_profit_and_loss_total(self):
        p_and_l_total = self.obj_compute_profit_and_loss.compute_profit_and_loss_total(self.currencies_calculations['return_excl_curr'])

        assert np.allclose(np.array(p_and_l_total.item()), np.array(6.82727431390140000))

    def test_compute_profit_and_loss_spot(self):
        combo_overview = self.obj_compute_profit_and_loss.compute_profit_and_loss_combo(self.currencies_calculations['combo_curr'])
        p_and_l_spot = self.obj_compute_profit_and_loss.compute_profit_and_loss_spot(self.spot_origin, combo_overview)

        assert np.allclose(np.array(p_and_l_spot.item()), np.array(5.35433070866143000))

    def test_compute_profit_and_loss_carry(self):
        profit_and_loss_total = self.obj_compute_profit_and_loss.compute_profit_and_loss_total(self.currencies_calculations['return_excl_curr'])
        combo_overview = self.obj_compute_profit_and_loss.compute_profit_and_loss_combo(self.currencies_calculations['combo_curr'])
        profit_and_loss_spot = self.obj_compute_profit_and_loss.compute_profit_and_loss_spot(self.spot_origin, combo_overview)

        p_and_l_carry = self.obj_compute_profit_and_loss.compute_profit_and_loss_carry(profit_and_loss_total, profit_and_loss_spot)

        assert np.allclose(np.array(p_and_l_carry.item()), np.array(1.4729436052399700000))

    @parameterized.expand([["weekly", "WED", "30/11/2020", "25/12/2019"],
                           ["weekly", "WED", "23/09/2020", "25/12/2019"],
                           ["weekly", "WED", "21/10/2020", "25/12/2019"],
                           ["daily", "WED", "23/09/2020", "25/12/2019"],
                           ["daily", "THU", "24/09/2020", "26/12/2019"],
                           ["monthly", "MON", "30/11/2020", "31/12/2019"]
                           ])
    def test_get_the_last_day_of_previous_year(self, frequency, signal_day, origin_output, expected_output):
        year = (pd.to_datetime(origin_output, format="%d/%m/%Y") - pd.DateOffset(years=1)).year
        day = self.obj_compute_profit_and_loss.get_the_last_day_of_previous_year(year, 12, frequency, signal_day)

        assert day == pd.to_datetime(expected_output, format="%d/%m/%Y")

    def test_compute_profit_and_loss_notional(self):
        combo_overview = self.obj_compute_profit_and_loss.compute_profit_and_loss_combo(self.currencies_calculations['combo_curr'])
        total_overview = self.obj_compute_profit_and_loss.compute_profit_and_loss_total(self.currencies_calculations['return_excl_curr'])
        spot_overview = self.obj_compute_profit_and_loss.compute_profit_and_loss_spot(self.spot_origin, combo_overview)

        # Aggregate
        total_incl_signals = self.obj_compute_agg_currencies.compute_aggregate_total_incl_signals(self.currencies_calculations['return_incl_curr'], inverse_volatility=None)
        spot_incl_signals = self.obj_compute_agg_currencies.compute_aggregate_spot_incl_signals(self.currencies_calculations['spot_incl_curr'], inverse_volatility=None)

        p_and_l_not = self.obj_compute_profit_and_loss.compute_profit_and_loss_notional(spot_overview,
                                                                                        total_overview,
                                                                                        combo_overview,
                                                                                        total_incl_signals,
                                                                                        spot_incl_signals,
                                                                                        "WED")
        p_and_l_total_ytd_not, p_and_l_spot_ytd_not = -41.2655507007209000, -110.3272323904580000
        p_and_l_carry_ytd_not,  p_and_l_total_weekly_not = 69.0616816897371000, 682.7274313901400000
        p_and_l_spot_weekly_not, p_and_l_carry_weekly_not = 535.4330708661430000, 147.2943605239970000

        assert np.allclose(np.array([p_and_l_not['profit_and_loss_total_ytd_notional'],
                                     p_and_l_not['profit_and_loss_spot_ytd_notional'],
                                     p_and_l_not['profit_and_loss_carry_ytd_notional'],
                                     p_and_l_not['profit_and_loss_total_weekly_notional'],
                                     p_and_l_not['profit_and_loss_spot_weekly_notional'],
                                     p_and_l_not['profit_and_loss_carry_weekly_notional']]),
                           np.array([p_and_l_total_ytd_not,
                                     p_and_l_spot_ytd_not,
                                     p_and_l_carry_ytd_not,
                                     p_and_l_total_weekly_not,
                                     p_and_l_spot_weekly_not,
                                     p_and_l_carry_weekly_not]))

    def test_get_first_day_of_year(self):
        day = self.obj_compute_profit_and_loss.get_first_day_of_year()
        assert day == pd.to_datetime('01/01/2020', format='%d/%m/%Y')

    def test_compute_profit_and_loss_implemented_in_matr(self):
        combo_overview = self.obj_compute_profit_and_loss.compute_profit_and_loss_combo(self.currencies_calculations['combo_curr'])
        total_overview = self.obj_compute_profit_and_loss.compute_profit_and_loss_total(self.currencies_calculations['return_excl_curr'])
        spot_overview = self.obj_compute_profit_and_loss.compute_profit_and_loss_spot(self.spot_origin, combo_overview)

        # Aggregate
        total_incl_signals = self.obj_compute_agg_currencies.compute_aggregate_total_incl_signals(self.currencies_calculations['return_incl_curr'], inverse_volatility=None)
        spot_incl_signals = self.obj_compute_agg_currencies.compute_aggregate_spot_incl_signals(self.currencies_calculations['spot_incl_curr'], inverse_volatility=None)

        p_and_l_not = self.obj_compute_profit_and_loss.compute_profit_and_loss_notional(spot_overview,
                                                                                        total_overview,
                                                                                        combo_overview,
                                                                                        total_incl_signals,
                                                                                        spot_incl_signals,
                                                                                        "WED")
        # Weighted performance
        ret = self.obj_compute_agg_currencies.compute_excl_signals_total_return(self.carry_origin)
        log_ret = self.obj_compute_agg_currencies.compute_log_returns_excl_costs(ret)
        weighted_perf = self.obj_compute_agg_currencies.compute_weighted_performance(log_ret, self.currencies_calculations['combo_curr'], 0.03)

        p_and_l_in_matr = self.obj_compute_profit_and_loss.compute_profit_and_loss_implemented_in_matr(combo_overview,
                                                                                                       p_and_l_not['profit_and_loss_total_ytd_notional'],
                                                                                                       p_and_l_not['profit_and_loss_spot_ytd_notional'],
                                                                                                       p_and_l_not['profit_and_loss_total_weekly_notional'],
                                                                                                       p_and_l_not['profit_and_loss_spot_weekly_notional'],
                                                                                                       weighted_perf)
        p_and_l_total_ytd_matr, p_and_l_spot_ytd_matr = -1.1220809356304900000, -2.9999862365594100000
        p_and_l_carry_ytd_matr, p_and_l_total_weekly_matr = 1.8779053009289300000, 20.4818229417042000000
        p_and_l_spot_weekly_matr, p_and_l_carry_weekly_matr = 16.0629921259843000000, 4.4188308157199200000

        assert np.allclose(np.array([p_and_l_in_matr['profit_and_loss_total_ytd_matr'],
                                     p_and_l_in_matr['profit_and_loss_spot_ytd_matr'],
                                     p_and_l_in_matr['profit_and_loss_carry_ytd_matr'],
                                     p_and_l_in_matr['profit_and_loss_total_weekly_matr'],
                                     p_and_l_in_matr['profit_and_loss_spot_weekly_matr'],
                                     p_and_l_in_matr['profit_and_loss_carry_weekly_matr']]),
                           np.array([p_and_l_total_ytd_matr,
                                     p_and_l_spot_ytd_matr,
                                     p_and_l_carry_ytd_matr,
                                     p_and_l_total_weekly_matr,
                                     p_and_l_spot_weekly_matr,
                                     p_and_l_carry_weekly_matr]))
