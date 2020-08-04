from math import sqrt

class ComputeSignalsOverview:

    def __init__(self, next_latest_date, latest_date):
        self.next_latest_date = next_latest_date
        self.latest_date = latest_date

    def compute_signals_real_carry(self, real_carry):

        return real_carry.loc[self.next_latest_date]

    def compute_signals_trend(self, trend):

        return trend.loc[self.next_latest_date]

    def compute_signals_combo(self, combo):

        return combo.loc[self.next_latest_date]

    def compute_drawdown_position_size_matr(self, total_incl_signals, size_attr):

        # Drawdown
        drawdown = ((total_incl_signals.loc[self.latest_date][0] / total_incl_signals.max()[0]) - 1) * 100

        # Position size in MATR
        size_matr = size_attr

        return {'drawdown': drawdown, 'size_matr': size_matr}

    def compute_limits_controls(self, signals_combo, size_attr, log_returns, window):

        # Current signals
        current_signals = tuple(list(signals_combo * size_attr))
        # Ex-ante volatility
        latest_signal_date_loc = log_returns.index.get_loc(self.latest_date)
        # Log returns with window lag
        log_returns_lag = log_returns.iloc[latest_signal_date_loc - window:latest_signal_date_loc+1, :]
        ex_ante_vol = sqrt(52) * log_returns_lag.dot(current_signals).std()

        # MATR notional
        matr_notional = signals_combo.sum() * size_attr

        return {'ex_ante_vol': ex_ante_vol, 'matr_notional': matr_notional}

    def run_signals_overview(self, real_carry, trend, combo, total_incl_signals, size_attr, log_returns, window):

        signals_real_carry_overview = self.compute_signals_real_carry(real_carry=real_carry)
        signals_trend_overview = self.compute_signals_trend(trend=trend)
        signals_combo_overview = self.compute_signals_combo(combo=combo)
        signals_drawdown_position_size_matr = self.compute_drawdown_position_size_matr(
                                              total_incl_signals=total_incl_signals, size_attr=size_attr)
        signals_limits_controls = self.compute_limits_controls(signals_combo=signals_combo_overview, size_attr=size_attr,
                                                               log_returns=log_returns, window=52)

        signals_overview = {'signals_real_carry': signals_real_carry_overview,
                            'signals_trend_overview': signals_trend_overview,
                            'signals_combo_overview': signals_combo_overview,
                            'signals_drawdown_position_size_matr': signals_drawdown_position_size_matr}

        return signals_overview

