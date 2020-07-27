



def compute_total_incl_signals(weight, returns_incl_costs, date):

    first_total_signals = [100]

    if weight == '1/N':

        average_incl_signals = (returns_incl_costs.loc[date:] / returns_incl_costs.loc[date:].shift(1)).mean(axis=1).iloc[1:].tolist()

        for value in range(len(average_incl_signals)):
            first_total_signals.append(first_total_signals[value] * average_incl_signals[value])

        average_incl_signals['Total_Incl_Signals'] = first_total_signals





def compute_inverse_volatility():
    pass

def compute_log_returns_ex_costs():
    pass

def compute_weighted_performance():
    pass



