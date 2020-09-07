import xlwings as xw


def write_outputs_controls_tab(p_and_l_overview, signals_overview, trades_overview,  rates_usd, rates_eur):
    weekly_total_not = p_and_l_overview['profit_and_loss_notional']['profit_and_loss_total_weekly_notional']
    weekly_spot_not = p_and_l_overview['profit_and_loss_notional']['profit_and_loss_spot_weekly_notional']
    weekly_carry_not = p_and_l_overview['profit_and_loss_notional']['profit_and_loss_carry_weekly_notional']

    ytd_total_not = p_and_l_overview['profit_and_loss_notional']['profit_and_loss_total_ytd_notional']
    ytd_spot_not = p_and_l_overview['profit_and_loss_notional']['profit_and_loss_spot_ytd_notional']
    ytd_carry_not = p_and_l_overview['profit_and_loss_notional']['profit_and_loss_carry_ytd_notional']

    weekly_total_matr = p_and_l_overview['profit_and_loss_matr']['profit_and_loss_total_weekly_matr']
    weekly_spot_matr = p_and_l_overview['profit_and_loss_matr']['profit_and_loss_spot_weekly_matr']
    weekly_carry_matr = p_and_l_overview['profit_and_loss_matr']['profit_and_loss_carry_weekly_matr']

    ytd_total_matr = p_and_l_overview['profit_and_loss_matr']['profit_and_loss_total_ytd_matr']
    ytd_spot_matr = p_and_l_overview['profit_and_loss_matr']['profit_and_loss_spot_ytd_matr']
    ytd_carry_matr = p_and_l_overview['profit_and_loss_matr']['profit_and_loss_carry_ytd_matr']

    sheet_effect_input = xw.Book.caller().sheets['EFFECT']

    # Profit and Loss overview
    sheet_effect_input.range('profit_and_loss_total_weekly_notional').value = weekly_total_not
    sheet_effect_input.range('profit_and_loss_spot_weekly_notional').value = weekly_spot_not
    sheet_effect_input.range('profit_and_loss_carry_weekly_notional').value = weekly_carry_not

    sheet_effect_input.range('profit_and_loss_total_ytd_notional').value = ytd_total_not
    sheet_effect_input.range('profit_and_loss_spot_ytd_notional').value = ytd_spot_not
    sheet_effect_input.range('profit_and_loss_carry_ytd_notional').value = ytd_carry_not

    sheet_effect_input.range('profit_and_loss_total_weekly_matr').value = weekly_total_matr
    sheet_effect_input.range('profit_and_loss_spot_weekly_matr').value = weekly_spot_matr
    sheet_effect_input.range('profit_and_loss_carry_weekly_matr').value = weekly_carry_matr

    sheet_effect_input.range('profit_and_loss_total_ytd_matr').value = ytd_total_matr
    sheet_effect_input.range('profit_and_loss_spot_ytd_matr').value = ytd_spot_matr
    sheet_effect_input.range('profit_and_loss_carry_ytd_matr').value = ytd_carry_matr

    sheet_effect_input.range('profit_and_loss_combo').options(transpose=True).value = p_and_l_overview[
        'profit_and_loss_combo_overview']
    sheet_effect_input.range('profit_and_loss_total').options(transpose=True).value = p_and_l_overview[
        'profit_and_loss_total_overview']
    sheet_effect_input.range('profit_and_loss_spot').options(transpose=True).value = p_and_l_overview[
        'profit_and_loss_spot_ex_overview']
    sheet_effect_input.range('profit_and_loss_carry').options(transpose=True).value = p_and_l_overview[
        'profit_and_loss_carry_overview']

    sheet_effect_input.range('signals_real_carry').options(transpose=True).value = signals_overview[
        'signals_real_carry']
    sheet_effect_input.range('signals_trend').options(transpose=True).value = signals_overview['signals_trend_overview']
    sheet_effect_input.range('signals_combo').options(transpose=True).value = signals_overview['signals_combo_overview']

    sheet_effect_input.range('drawdown').options(transpose=True).value = \
    signals_overview['signals_drawdown_position_size_matr']['drawdown']
    sheet_effect_input.range('position_matr').options(transpose=True).value = \
    signals_overview['signals_drawdown_position_size_matr']['size_matr']
    sheet_effect_input.range('ex_ante_vol').options(transpose=True).value = signals_overview['signals_limits_controls'][
        'ex_ante_vol']
    sheet_effect_input.range('matr_notional').options(transpose=True).value = \
    signals_overview['signals_limits_controls']['matr_notional']

    sheet_effect_input.range('trades_combo').options(transpose=True).value = trades_overview

    sheet_effect_input.range('warning_rates_usd').options(transpose=True).value = rates_usd
    sheet_effect_input.range('warning_rates_eur').options(transpose=True).value = rates_eur


def write_outputs_risk_return_overview(risk_returns):
    sheet_risk_returns = xw.Book.caller().sheets['RiskReturns']

    sheet_risk_returns.range('logs_excess_ret_no_signals').options(transpose=True).value = \
    risk_returns['excess_returns']['excess_returns_no_signals']
    sheet_risk_returns.range('logs_excess_ret_signals').options(transpose=True).value = risk_returns['excess_returns'][
        'excess_returns_with_signals']

    sheet_risk_returns.range('logs_std_dev_no_signals').options(transpose=True).value = risk_returns['std_dev'][
        'std_dev_no_signals']
    sheet_risk_returns.range('logs_std_dev_signals').options(transpose=True).value = risk_returns['std_dev'][
        'std_dev_with_signals']

    sheet_risk_returns.range('logs_sharpe_ratio_no_signals').options(transpose=True).value = \
    risk_returns['sharpe_ratio']['sharpe_ratio_no_signals']
    sheet_risk_returns.range('logs_sharpe_ratio_signals').options(transpose=True).value = risk_returns['sharpe_ratio'][
        'sharpe_ratio_with_signals']

    sheet_risk_returns.range('logs_max_drawdown_no_signals').options(transpose=True).value = \
    risk_returns['max_drawdown']['max_drawdown_no_signals']
    sheet_risk_returns.range('logs_max_drawdown_signals').options(transpose=True).value = risk_returns['max_drawdown'][
        'max_drawdown_with_signals']

    sheet_risk_returns.range('logs_calmar_no_signals').options(transpose=True).value = risk_returns['calmar_ratio'][
        'calmar_ratio_no_signals']
    sheet_risk_returns.range('logs_calmar_signals').options(transpose=True).value = risk_returns['calmar_ratio'][
        'calmar_ratio_with_signals']

    sheet_risk_returns.range('logs_equity_corr_no_signals').options(transpose=True).value = risk_returns['equity_corr'][
        'equity_corr_no_signals']
    sheet_risk_returns.range('logs_equity_corr_signals').options(transpose=True).value = risk_returns['equity_corr'][
        'equity_corr_with_signals']


def write_outputs_effect(combo, total_excl_signals, total_incl_signals, spot_incl_signals, spot_excl_signals):
    sheet_effect_output = xw.Book.caller().sheets['effect_output']

    n_columns = len(combo.columns) + 2

    sheet_effect_output.range('rng_effect_output').offset(-1, 0).value = "Incl Signals"
    sheet_effect_output.range('rng_effect_output').value = combo

    sheet_effect_output.range('rng_effect_output').offset(-1, n_columns).value = "Total Excl signals"
    sheet_effect_output.range('rng_effect_output').offset(0, n_columns).value = total_excl_signals

    sheet_effect_output.range('rng_effect_output').offset(-1, n_columns + 2).value = "Total Incl signals"
    sheet_effect_output.range('rng_effect_output').offset(0, n_columns + 2).value = total_incl_signals

    sheet_effect_output.range('rng_effect_output').offset(-1, n_columns + 4).value = "Spot Incl signals"
    sheet_effect_output.range('rng_effect_output').offset(0, n_columns + 4).value = spot_incl_signals

    sheet_effect_output.range('rng_effect_output').offset(-1, n_columns + 6).value = "Spot Excl signals"
    sheet_effect_output.range('rng_effect_output').offset(0, n_columns + 6).value = spot_excl_signals


def run_write_outputs_effect_model(model_outputs: dict):
    p_and_l_overview, signals_overview, trades_overview, rates_usd, rates_eur, risk_returns, combo, \
    total_excl_signals, total_incl_signals, spot_incl_signals, spot_excl_signals = model_outputs['effect']

    write_outputs_controls_tab(p_and_l_overview, signals_overview, trades_overview,  rates_usd, rates_eur)
    write_outputs_risk_return_overview(risk_returns)
    write_outputs_effect(combo, total_excl_signals, total_incl_signals, spot_incl_signals, spot_excl_signals)


