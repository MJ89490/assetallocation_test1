from math import sqrt

from data_etl.outputs_effect.write_logs_computations_effect import write_logs_effect


class ComputeSignalsOverview:

    def __init__(self, latest_signal_date, size_attr, window, next_latest_date):
        self.latest_signal_date = latest_signal_date
        self.size_attr = size_attr
        self.window = window
        self.next_latest_date = next_latest_date

    @property
    def size_attr(self):
        return self._size_attr

    @size_attr.setter
    def size_attr(self, value):
        self._size_attr = value

    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, value):
        self._window = value

    @property
    def next_latest_date(self):
        return self._next_latest_date

    @next_latest_date.setter
    def next_latest_date(self, value):
        next_latest_date_loc = value.dates_origin_index.get_loc(self.latest_signal_date) + 1
        self._next_latest_date = value.dates_origin_index[next_latest_date_loc]

    def compute_signals_real_carry(self, real_carry_curr):
        return real_carry_curr.loc[self.next_latest_date]

    def compute_signals_trend(self, trend_curr):
        return trend_curr.loc[self.next_latest_date]

    def compute_signals_combo(self, combo_curr):
        return combo_curr.loc[self.next_latest_date]

    def compute_drawdown_position_size_matr(self, agg_total_incl_signals):
        write_logs_effect("Computing drawdown and position size in matr...", "logs_signals_drawdown_size_matr")

        # Drawdown
        drawdown = ((agg_total_incl_signals.loc[self.latest_signal_date][0] / agg_total_incl_signals.max()[0]) - 1) * 100

        # Position size in MATR
        size_matr = self.size_attr * 100

        return {'drawdown': drawdown, 'size_matr': size_matr}

    def compute_limits_controls(self, signals_combo, agg_log_returns):
        write_logs_effect("Computing limits controls...", "logs_signals_limits")
        current_signals = tuple(list(signals_combo * self.size_attr))
        # Ex-ante volatility
        latest_signal_date_loc = agg_log_returns.index.get_loc(self.latest_signal_date)
        # Log returns with window lag
        log_returns_lag = agg_log_returns.iloc[latest_signal_date_loc - (self.window-1):latest_signal_date_loc+1, :]
        ex_ante_vol = sqrt(52) * log_returns_lag.dot(current_signals).std() * 100
        # MATR notional
        matr_notional = signals_combo.sum() * self.size_attr * 100

        return {'ex_ante_vol': ex_ante_vol, 'matr_notional': matr_notional}

    def run_signals_overview(self, real_carry_curr, trend_curr, combo_curr, agg_total_incl_signals, agg_log_returns):

        signals_real_carry_overview = self.compute_signals_real_carry(real_carry_curr=real_carry_curr)
        signals_trend_overview = self.compute_signals_trend(trend_curr=trend_curr)
        signals_combo_overview = self.compute_signals_combo(combo_curr=combo_curr)
        signals_drawdown_position_size_matr = self.compute_drawdown_position_size_matr(agg_total_incl_signals=agg_total_incl_signals)
        signals_limits_controls = self.compute_limits_controls(signals_combo=signals_combo_overview, agg_log_returns=agg_log_returns)

        signals_overview = {'signals_real_carry': signals_real_carry_overview.values,
                            'signals_trend_overview': signals_trend_overview.values,
                            'signals_combo_overview': signals_combo_overview.values,
                            'signals_drawdown_position_size_matr': signals_drawdown_position_size_matr,
                            'signals_limits_controls': signals_limits_controls}

        return signals_overview

