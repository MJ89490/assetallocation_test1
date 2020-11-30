def compute_trades_overview(profit_and_loss_combo_overview, signals_combo_overview):
    """
    Function computing the trades
    :param profit_and_loss_combo_overview: profit_and_loss_combo_overview values
    :param signals_combo_overview: signals_combo_overview values
    :return: a dataFrame with trades values
    """

    return signals_combo_overview - profit_and_loss_combo_overview
