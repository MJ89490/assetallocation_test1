import xlwings as xw


# def write_outputs_controls_tab(p_and_l_overview, signals_overview, trades_overview, rates):
def write_outputs_controls_tab(p_and_l_overview, signals_overview, trades_overview,  rates, date_run):

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

    # Date run
    sheet_effect_input.range('rng_effect_date_run').value = date_run.item()

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

    # ---- Profit and Loss table ---- #
    sheet_effect_input.range('profit_and_loss_combo').options(transpose=True).offset(1, 0).value = p_and_l_overview['profit_and_loss_combo_overview']
    sheet_effect_input.range('profit_and_loss_total').options(transpose=True).offset(1, 0).value = p_and_l_overview['profit_and_loss_total_overview']
    sheet_effect_input.range('profit_and_loss_spot').options(transpose=True).offset(1, 0).value = p_and_l_overview['profit_and_loss_spot_ex_overview']
    sheet_effect_input.range('profit_and_loss_carry').options(transpose=True).offset(1, 0).value = p_and_l_overview['profit_and_loss_carry_overview']

    # ---- Signals table ---- #
    sheet_effect_input.range('signals_real_carry').options(transpose=True).offset(1, 0).value = signals_overview['signals_real_carry']
    sheet_effect_input.range('signals_trend').options(transpose=True).offset(1, 0).value = signals_overview['signals_trend_overview']
    sheet_effect_input.range('signals_combo').options(transpose=True).offset(1, 0).value = signals_overview['signals_combo_overview']

    # ---- Drawdown and limits controls ----#
    sheet_effect_input.range('drawdown').options(transpose=True).value = signals_overview['signals_drawdown_position_size_matr']['drawdown']
    sheet_effect_input.range('position_matr').options(transpose=True).value = signals_overview['signals_drawdown_position_size_matr']['size_matr']
    sheet_effect_input.range('ex_ante_vol').options(transpose=True).value = signals_overview['signals_limits_controls']['ex_ante_vol']
    sheet_effect_input.range('matr_notional').options(transpose=True).value = signals_overview['signals_limits_controls']['matr_notional']

    # ---- Trades ----#
    sheet_effect_input.range('trades_combo').options(transpose=True).offset(1, 0).value = trades_overview

    # ---- Warning flags ----#
    sheet_effect_input.range('warning_flags_rates').options(transpose=True).offset(1, 0).value = rates


def write_outputs_risk_return_overview(risk_returns):
    sheet_risk_returns = xw.Book.caller().sheets['RiskReturns']

    sheet_risk_returns.range('rng_excess_ret_no_signals').options(transpose=True).value = \
    risk_returns['excess_returns']['excess_returns_no_signals']
    sheet_risk_returns.range('rng_excess_ret_signals').options(transpose=True).value = risk_returns['excess_returns'][
        'excess_returns_with_signals']

    sheet_risk_returns.range('rng_std_dev_no_signals').options(transpose=True).value = risk_returns['std_dev'][
        'std_dev_no_signals']
    sheet_risk_returns.range('rng_std_dev_signals').options(transpose=True).value = risk_returns['std_dev'][
        'std_dev_with_signals']

    sheet_risk_returns.range('rng_sharpe_ratio_no_signals').options(transpose=True).value = \
    risk_returns['sharpe_ratio']['sharpe_ratio_no_signals']
    sheet_risk_returns.range('rng_sharpe_ratio_signals').options(transpose=True).value = risk_returns['sharpe_ratio'][
        'sharpe_ratio_with_signals']

    sheet_risk_returns.range('rng_max_drawdown_no_signals').options(transpose=True).value = \
    risk_returns['max_drawdown']['max_drawdown_no_signals']
    sheet_risk_returns.range('rng_max_drawdown_signals').options(transpose=True).value = risk_returns['max_drawdown'][
        'max_drawdown_with_signals']

    sheet_risk_returns.range('rng_calmar_no_signals').options(transpose=True).value = risk_returns['calmar_ratio'][
        'calmar_ratio_no_signals']
    sheet_risk_returns.range('rng_calmar_signals').options(transpose=True).value = risk_returns['calmar_ratio'][
        'calmar_ratio_with_signals']

    sheet_risk_returns.range('rng_equity_corr_no_signals').options(transpose=True).value = risk_returns['equity_corr'][
        'equity_corr_no_signals']
    sheet_risk_returns.range('rng_equity_corr_signals').options(transpose=True).value = risk_returns['equity_corr'][
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


def add_color_scheme_to_tables():
    from xlwings.utils import rgb_to_int

    sheet_effect_input = xw.Book.caller().sheets['EFFECT']

    # ------------------------------------ P&L Signals Warning Flags ------------------------------------
    last_row = sheet_effect_input.range("G19").end('down').row + 1

    # Columns letters
    col_letters = ['H', 'I', 'J', 'K', 'M', 'N', 'O', 'P', 'S', 'Q']
    for letter in col_letters:
        for row in range(19, last_row):
            if sheet_effect_input.range(f'{letter}{row}').value is not None:
                if letter == 'H' or letter == 'O' or letter == 'Q':
                    sheet_effect_input.range(f'{letter}{row}').api.Font.bold = True
                if sheet_effect_input.range(f'{letter}{row}').value < 0:
                    sheet_effect_input.range(f'{letter}{row}').api.Font.Color = rgb_to_int((204, 0, 0))
                else:
                    sheet_effect_input.range(f'{letter}{row}').api.Font.Color = rgb_to_int((0, 128, 0))

    # ------------------------------------ Summary tables ------------------------------------
    ranges = ['profit_and_loss_total_weekly_notional', 'profit_and_loss_spot_weekly_notional',
              'profit_and_loss_carry_weekly_notional', 'profit_and_loss_total_ytd_notional',
              'profit_and_loss_spot_ytd_notional', 'profit_and_loss_carry_ytd_notional',
              'profit_and_loss_total_weekly_matr', 'profit_and_loss_spot_weekly_matr',
              'profit_and_loss_carry_weekly_matr', 'profit_and_loss_total_ytd_matr',
              'profit_and_loss_spot_ytd_matr', 'profit_and_loss_carry_ytd_matr',
              'drawdown', 'position_matr', 'ex_ante_vol', 'matr_notional']

    for rng in ranges:
        if sheet_effect_input.range(rng).value < 0:
            sheet_effect_input.range(rng).api.Font.Color = rgb_to_int((204, 0, 0))
        else:
            sheet_effect_input.range(rng).api.Font.Color = rgb_to_int((0, 128, 0))


def run_write_outputs_effect_model(model_outputs: dict):
    p_and_l_overview, signals_overview, trades_overview, rates, risk_returns, combo, \
    total_excl_signals, total_incl_signals, spot_incl_signals, spot_excl_signals, date_run = model_outputs['effect']

    write_outputs_controls_tab(p_and_l_overview, signals_overview, trades_overview,  rates, date_run)
    write_outputs_risk_return_overview(risk_returns)
    write_outputs_effect(combo, total_excl_signals, total_incl_signals, spot_incl_signals, spot_excl_signals)

    add_color_scheme_to_tables()


