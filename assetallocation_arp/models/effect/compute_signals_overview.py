
class ComputeSignalsOverview:

    def __init__(self, next_latest_date):
        self.next_latest_date = next_latest_date

    def compute_signals_real_carry(self, real_carry):

        return real_carry.loc[self.next_latest_date]

    def compute_signals_trend(self, trend):

        return trend.loc[self.next_latest_date]

    def compute_signals_combo(self, combo):

        return combo.loc[self.next_latest_date]

    def run_signals_overview(self, real_carry, trend, combo):

        signals_real_carry_overview = self.compute_signals_real_carry(real_carry=real_carry)
        signals_trend_overview = self.compute_signals_trend(trend=trend)
        signals_combo_overview = self.compute_signals_combo(combo=combo)

        return signals_real_carry_overview, signals_trend_overview, signals_combo_overview

