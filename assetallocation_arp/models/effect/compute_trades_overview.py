from data_etl.outputs_effect.write_logs_computations_effect import write_logs_effect


def compute_trades_overview(profit_and_loss_combo_overview, signals_combo_overview):
    write_logs_effect("Computing trade overview...", "logs_trade_overview")
    return signals_combo_overview - profit_and_loss_combo_overview
