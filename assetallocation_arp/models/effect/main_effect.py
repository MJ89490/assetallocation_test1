import pandas as pd

from assetallocation_arp.models.effect.read_inputs_effect import read_user_date, read_update_imf, \
                                                                 read_latest_signal_date, read_aggregate_calc
from assetallocation_arp.models.effect.compute_currencies import ComputeCurrencies

from assetallocation_arp.data_etl.inputs_effect.compute_inflation_differential import ComputeInflationDifferential

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

    user_date = read_user_date(pd.to_datetime(strategy_inputs['input_user_date_effect'].item().replace('/', '-'),
                                              format='%d-%m-%Y'))

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                         EFFECT ALL CURRENCIES COMPUTATIONS                                       #
    # ---------------------------------------------------------------------------------------------------------------- #
    obj_import_data = ComputeCurrencies(asset_inputs=asset_inputs,
                                        bid_ask_spread=int(strategy_inputs['input_bid_ask_effect'].item()),
                                        frequency_mat=strategy_inputs['input_frequency_effect'].item(),
                                        end_date_mat=strategy_inputs['input_signal_date_effect'].item(),
                                        signal_day_mat=strategy_inputs['input_signal_day_effect'].item(),
                                        all_data=all_data)
    obj_import_data.process_all_data_effect()
    obj_import_data.start_date_calculations = user_date
    process_usd_eur_data_effect = obj_import_data.process_usd_eur_data_effect()
    # -------------------------- Inflation differential calculations ------------------------------------------------- #
    obj_inflation_differential = ComputeInflationDifferential(dates_index=obj_import_data.dates_index)

    imf_data_update = read_update_imf(strategy_inputs['input_update_imf_effect'])

    inflation_differential, currency_logs = obj_inflation_differential.compute_inflation_differential(
                                            strategy_inputs['input_real_time_inf_effect'].item(),
                                            obj_import_data.all_currencies_spot,
                                            obj_import_data.currencies_spot['currencies_spot_usd'],
                                            imf_data_update=imf_data_update)

    # -------------------------- Carry - Trend - Combo - Returns - Spot ---------------------------------------------- #
    carry_inputs = {'type': strategy_inputs['input_real_nominal_effect'].item().strip().lower(),
                    'inflation': inflation_differential}

    trend_inputs = {'short_term': int(strategy_inputs['input_short_term_ma'].item()),
                    'long_term': int(strategy_inputs['input_long_term_ma'].item()),
                    'trend': strategy_inputs['input_trend_indicator_effect'].item().strip().lower()}

    combo_inputs = {'cut_off': float(strategy_inputs['input_cut_off_long'].item()),
                    'incl_shorts': strategy_inputs['input_include_shorts_effect'].item().strip().lower(),
                    'cut_off_s': float(strategy_inputs['input_cut_off_short'].item()),
                    'threshold': float(strategy_inputs['input_threshold_effect'].item())}

    currencies_calculations = obj_import_data.run_compute_currencies(carry_inputs, trend_inputs, combo_inputs)

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                                 EFFECT OVERVIEW                                                  #
    # ---------------------------------------------------------------------------------------------------------------- #
    latest_signal_date = read_latest_signal_date(pd.to_datetime(strategy_inputs['input_signal_date_effect'].item().
                                                                replace('/', '-'), format='%d-%m-%Y'),
                                                 obj_import_data, strategy_inputs['input_frequency_effect'])

    # -------------------------------- Aggregate Currencies ---------------------------------------------------------- #
    obj_compute_agg_currencies = ComputeAggregateCurrencies(window=int(strategy_inputs['input_window_effect'].item()),
                                                            weight=strategy_inputs['input_risk_weighting'].item().strip(),
                                                            dates_index=obj_import_data.dates_index,
                                                            start_date_calculations=obj_import_data.start_date_calculations,
                                                            prev_start_date_calc=obj_import_data.previous_start_date_calc)

    agg_currencies = obj_compute_agg_currencies.run_aggregate_currencies(
                                                   returns_incl_costs=currencies_calculations['return_incl_curr'],
                                                   spot_origin=process_usd_eur_data_effect['common_spot'],
                                                   spot_incl_costs=currencies_calculations['spot_incl_curr'],
                                                   carry_origin=process_usd_eur_data_effect['common_carry'],
                                                   combo_curr=currencies_calculations['combo_curr'],
                                                   weight_value=float(strategy_inputs['input_position_size_effect'].item())/100)

    # -------------------------- Profit and Loss overview Combo; Returns Ex costs; Spot; Carry ----------------------- #
    obj_compute_profit_and_loss_overview = ComputeProfitAndLoss(latest_date=latest_signal_date,
                                                                position_size_attribution=float(strategy_inputs['input_position_size_effect'].item())/100,
                                                                index_dates=obj_import_data.dates_origin_index,
                                                                frequency=strategy_inputs['input_frequency_effect'].item())

    profit_and_loss = obj_compute_profit_and_loss_overview.run_profit_and_loss(
                                                   combo_curr=currencies_calculations['combo_curr'],
                                                   returns_ex_costs=currencies_calculations['return_excl_curr'],
                                                   spot_origin=process_usd_eur_data_effect['common_spot'],
                                                   total_incl_signals=agg_currencies['agg_total_incl_signals'],
                                                   spot_incl_signals=agg_currencies['agg_spot_incl_signals'],
                                                   weighted_perf=agg_currencies['weighted_performance'],
                                                   signal_day=strategy_inputs['input_signal_day_effect'].item())

    # -------------------------- Signals: Combo; Returns Ex costs; Spot; Carry --------------------------------------- #
    obj_compute_signals_overview = ComputeSignalsOverview(latest_signal_date=latest_signal_date,
                                                          size_attr=float(strategy_inputs['input_position_size_effect'].item())/100,
                                                          window=int(strategy_inputs['input_window_effect'].item()),
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
                                                                     frequency_mat=strategy_inputs['input_frequency_effect'].item())

    rates = obj_compute_warning_flags_overview.compute_warning_flags_rates(process_usd_eur_data_effect['three_month_implied_usd'],
                                                                           process_usd_eur_data_effect['three_month_implied_eur'])

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                            EFFECT RISK RETURN CALCULATIONS                                       #
    # ---------------------------------------------------------------------------------------------------------------- #
    obj_compute_risk_return_calculations = ComputeRiskReturnCalculations(
                                                    start_date=obj_import_data.start_date_prev_calculations,
                                                    end_date=latest_signal_date,
                                                    dates_index=obj_import_data.dates_origin_index)

    risk_returns = obj_compute_risk_return_calculations.run_compute_risk_return_calculations(
                                    returns_excl_signals=agg_currencies['agg_total_excl_signals'].head(-1),
                                    returns_incl_signals=agg_currencies['agg_total_incl_signals'].head(-1),
                                    spxt_index_values=process_usd_eur_data_effect['spxt_index_values'].loc[user_date:],
                                    jgenvuug_index_values=process_usd_eur_data_effect['jgenvuug_index_values'])

    write_logs = {'currency_logs': currency_logs}

    agg_curr = read_aggregate_calc(agg_currencies['agg_total_excl_signals'], agg_currencies['agg_total_incl_signals'],
                                   agg_currencies['agg_spot_incl_signals'], agg_currencies['agg_spot_excl_signals'])

    effect_outputs = {'profit_and_loss': profit_and_loss,
                      'signals_overview': signals_overview,
                      'trades_overview': trades_overview,
                      'rates': rates,
                      'risk_returns': risk_returns,
                      'combo': currencies_calculations['combo_curr'],
                      'log_ret': agg_currencies['log_returns_excl_costs'],
                      'pos_size': float(strategy_inputs['input_position_size_effect'].item())/100,
                      'region': process_usd_eur_data_effect['region_config'],
                      'agg_dates': agg_curr['agg_dates'],
                      'total_excl_signals': agg_curr['agg_total_excl_signals'],
                      'total_incl_signals': agg_curr['agg_total_incl_signals'],
                      'spot_incl_signals': agg_curr['agg_spot_incl_signals'],
                      'spot_excl_signals': agg_curr['agg_spot_excl_signals']}

    return effect_outputs, write_logs
