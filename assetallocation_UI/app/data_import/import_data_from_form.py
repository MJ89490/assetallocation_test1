from app.forms import InputsTimesModel


def inputs_times_model():

    form = InputsTimesModel()

    return {form.time_lag.name: [int(form.time_lag.data)],
            form.leverage_type.name: [form.leverage_type.data],
            form.volatility_window.name: [int(form.volatility_window.data)],
            form.sig1_short.name: [int(form.sig1_short.data)],
            form.sig1_long.name: [int(form.sig1_long.data)],
            form.sig2_short.name: [int(form.sig2_short.data)],
            form.sig2_long.name: [int(form.sig2_long.data)],
            form.sig3_short.name: [int(form.sig3_short.data)],
            form.sig3_long.name: [int(form.sig3_long.data)],
            form.frequency.name: [form.frequency.data],
            form.week_day.name: [form.week_day.data]
           }

