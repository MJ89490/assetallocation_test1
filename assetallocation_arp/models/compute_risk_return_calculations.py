

def compute_no_signals_excess_returns(start_date, end_date, returns_excl_signals):
    pass

def compute_no_signals_std_dev(returns_excl_signals):
    pass

def compute_no_signals_sharpe_ratio(returns_excl_signals):
    pass

def compute_no_signals_max_drawdown():
    pass

def compute_no_signals_calmar_ratio():
    pass

def compute_no_signals_equity_correlation():
    pass

def compute_no_signals_gbi_em_correlation():
    pass


def run_compute_risk_return_calculations(start_date, end_date, returns_excl_signals):

    excess_returns = compute_no_signals_excess_returns(start_date, end_date, returns_excl_signals)
    std_dev = compute_no_signals_std_dev(returns_excl_signals)
    sharpe_ratio = compute_no_signals_sharpe_ratio(returns_excl_signals)
    max_drawdown = compute_no_signals_max_drawdown()
    calmar_ratio = compute_no_signals_calmar_ratio()

    