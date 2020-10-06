import pandas as pd
import os
import calendar
from configparser import ConfigParser
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from assetallocation_arp.models.effect.compute_currencies import ComputeCurrencies

from data_etl.inputs_effect.compute_inflation_differential import ComputeInflationDifferential

from assetallocation_arp.models.effect.compute_profit_and_loss_overview import ComputeProfitAndLoss
from assetallocation_arp.models.effect.compute_signals_overview import ComputeSignalsOverview
from assetallocation_arp.models.effect.compute_trades_overview import compute_trades_overview
from assetallocation_arp.models.effect.compute_warning_flags_overview import ComputeWarningFlagsOverview

from assetallocation_arp.models.effect.compute_aggregate_currencies import ComputeAggregateCurrencies
from assetallocation_arp.models.compute_risk_return_calculations import ComputeRiskReturnCalculations


"""
    Main function to run the EFFECT computations
"""


def run_effect(strategy_inputs, asset_inputs, all_data):

    user_date = strategy_inputs['userdate'].item()

    if user_date is None:
        # Instantiate ConfigParser
        config = ConfigParser()
        # Parse existing file
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config_effect_model', 'dates_effect.ini'))
        config.read(path)
        # Read values from the dates_effect.ini file
        default_start_date = config.get('start_date_computations', 'start_date_calculations')
        user_date = default_start_date

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                         EFFECT ALL CURRENCIES COMPUTATIONS                                       #
    # ---------------------------------------------------------------------------------------------------------------- #
    obj_import_data = ComputeCurrencies(asset_inputs=asset_inputs,
                                        bid_ask_spread=strategy_inputs['Bid-ask spread (bp)'].item(),
                                        frequency_mat=strategy_inputs['Frequency'].item(),
                                        start_date_mat=strategy_inputs['StartDate'].item(),
                                        end_date_mat=strategy_inputs['latest signal date'].item(),
                                        signal_day_mat=strategy_inputs['SignalDay'].item(), all_data=all_data)
    spx_index_values = obj_import_data.process_data_effect()
    obj_import_data.start_date_calculations = user_date
    spot_origin, carry_origin = obj_import_data.process_data_config_effect()
    # -------------------------- Inflation differential calculations ------------------------------------------------- #
    obj_inflation_differential = ComputeInflationDifferential(dates_index=obj_import_data.dates_index)

    inflation_differential = obj_inflation_differential.compute_inflation_differential(
                             strategy_inputs['Realtime Inflation Forecast'].item(), obj_import_data.all_currencies_spot,
                             obj_import_data.currencies_spot['currencies_spot_usd'],
                             imf_data_update=strategy_inputs['updateIMFdata'].item())

    # -------------------------- Carry - Trend - Combo - Returns - Spot ---------------------------------------------- #
    carry_inputs = {'type': strategy_inputs['Real/Nominal'].item().strip().lower(), 'inflation': inflation_differential}
    trend_inputs = {'short_term': int(strategy_inputs['Short-term MA'].item()), 'long_term': int(strategy_inputs['Long-term MA'].item()), 'trend': strategy_inputs['TrendIndicator'].item().strip().lower()}
    combo_inputs = {'cut_off': float(strategy_inputs['Interest rate cut-off (long)'].item())*100, 'incl_shorts': strategy_inputs['Include Shorts'].item().strip().lower(), 'cut_off_s': float(strategy_inputs['Interest rate cut-off (short)'].item())*100, 'threshold': float(strategy_inputs['Threshold for closing'].item())*100}

    currencies_calculations = obj_import_data.run_compute_currencies(carry_inputs, trend_inputs, combo_inputs)

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                                 EFFECT OVERVIEW                                                  #
    # ---------------------------------------------------------------------------------------------------------------- #
    latest_signal_date = strategy_inputs['latest signal date'].item()

    if latest_signal_date is None:
        latest_signal_date = obj_import_data.dates_origin_index[-2]
        # Previous Wednesday
        if strategy_inputs['Frequency'].item() == 'weekly' or strategy_inputs['Frequency'].item() == 'daily':
            delta = (latest_signal_date.weekday() + 4) % 7 + 1
            latest_signal_date = pd.to_datetime(latest_signal_date - timedelta(days=delta), format='%d-%m-%Y')
        # Previous month
        else:
            days = []
            y, m = latest_signal_date.year, (latest_signal_date - relativedelta(months=1)).month
            for d in range(1, calendar.monthrange(y, m)[1] + 1):
                tmp_date = pd.to_datetime('{:04d}-{:02d}-{:02d}'.format(y, m, d), format='%Y-%m-%d')
                days.append(tmp_date)
            latest_signal_date = pd.to_datetime(days[-1], format='%d-%m-%Y')

    # -------------------------------- Aggregate Currencies ---------------------------------------------------------- #
    obj_compute_agg_currencies = ComputeAggregateCurrencies(window=int(strategy_inputs['STDev window (weeks)'].item()),
                                                            weight=strategy_inputs['Risk-weighting'].item().strip(),
                                                            dates_index=obj_import_data.dates_origin_index,
                                                            start_date_calculations=obj_import_data.start_date_calculations,
                                                            prev_start_date_calc=obj_import_data.previous_start_date_calc)

    agg_currencies = obj_compute_agg_currencies.run_aggregate_currencies(
                                                   returns_incl_costs=currencies_calculations['return_incl_curr'],
                                                   spot_origin=spot_origin,
                                                   spot_incl_costs=currencies_calculations['spot_incl_curr'],
                                                   carry_origin=carry_origin,
                                                   combo_curr=currencies_calculations['combo_curr'],
                                                   weight_value=strategy_inputs['Position size'].item())

    # -------------------------- Profit and Loss overview Combo; Returns Ex costs; Spot; Carry ----------------------- #
    obj_compute_profit_and_loss_overview = ComputeProfitAndLoss(latest_date=latest_signal_date,
                                                                position_size_attribution=float(strategy_inputs['Position size'][1]),
                                                                index_dates=obj_import_data.dates_origin_index,
                                                                frequency=strategy_inputs['Frequency'].item())

    profit_and_loss = obj_compute_profit_and_loss_overview.run_profit_and_loss(
                                                   combo_curr=currencies_calculations['combo_curr'],
                                                   returns_ex_costs=currencies_calculations['return_excl_curr'],
                                                   spot_origin=spot_origin,
                                                   total_incl_signals=agg_currencies['agg_total_incl_signals'],
                                                   spot_incl_signals=agg_currencies['agg_spot_incl_signals'],
                                                   weighted_perf=agg_currencies['weighted_performance'],
                                                   signal_day=strategy_inputs['SignalDay'].item())

    # -------------------------- Signals: Combo; Returns Ex costs; Spot; Carry --------------------------------------- #
    obj_compute_signals_overview = ComputeSignalsOverview(latest_signal_date=latest_signal_date,
                                                          size_attr=float(strategy_inputs['Position size'].item()),
                                                          window=int(strategy_inputs['STDev window (weeks)'].item()),
                                                          next_latest_date=obj_import_data)

    signals_overview = obj_compute_signals_overview.run_signals_overview(
                                                    real_carry_curr=currencies_calculations['carry_curr'],
                                                    trend_curr=currencies_calculations['trend_curr'],
                                                    combo_curr=currencies_calculations['combo_curr'],
                                                    agg_total_incl_signals=agg_currencies['agg_total_incl_signals'],
                                                    agg_log_returns=agg_currencies['log_returns_excl_costs'])

    # -------------------------- Trades: Combo ----------------------------------------------------------------------- #
    trades_overview = compute_trades_overview(profit_and_loss_combo_overview=profit_and_loss['profit_and_loss_combo_overview'],
                                              signals_combo_overview=signals_overview['signals_combo_overview'])

    # -------------------------- Warning Flags: Rates; Inflation ----------------------------------------------------- #
    obj_compute_warning_flags_overview = ComputeWarningFlagsOverview(latest_signal_date=latest_signal_date,
                                                                     asset_inputs=asset_inputs,
                                                                     end_date_mat=strategy_inputs['latest signal date'].item(),
                                                                     frequency_mat=strategy_inputs['Frequency'].item(),
                                                                     start_date_mat=strategy_inputs['StartDate'].item(),
                                                                     signal_day_mat=strategy_inputs['SignalDay'].item(),
                                                                     all_data=all_data)
    obj_compute_warning_flags_overview.process_data_effect()
    rates = obj_compute_warning_flags_overview.compute_warning_flags_rates()

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                            EFFECT RISK RETURN CALCULATIONS                                       #
    # ---------------------------------------------------------------------------------------------------------------- #
    obj_compute_risk_return_calculations = ComputeRiskReturnCalculations(
                                                    start_date=obj_import_data.start_date_calculations,
                                                    end_date=obj_import_data.dates_origin_index[-1],
                                                    dates_index=obj_import_data.dates_origin_index)

    risk_returns = obj_compute_risk_return_calculations.run_compute_risk_return_calculations(
                                                    returns_excl_signals=agg_currencies['agg_total_excl_signals'],
                                                    returns_incl_signals=agg_currencies['agg_total_incl_signals'],
                                                    spxt_index_values=spx_index_values.loc[pd.to_datetime(user_date, format='%d-%m-%Y'):])

    effect_outputs = {'profit_and_loss': profit_and_loss, 'signals_overview': signals_overview,
                      'trades_overview': trades_overview, 'rates': rates,
                      'risk_returns': risk_returns, 'combo': currencies_calculations['combo_curr'],
                      'total_excl_signals': agg_currencies['agg_total_excl_signals'],
                      'total_incl_signals': agg_currencies['agg_total_incl_signals'],
                      'spot_incl_signals': agg_currencies['agg_spot_incl_signals'],
                      'spot_excl_signals': agg_currencies['agg_spot_excl_signals']}

    return effect_outputs
