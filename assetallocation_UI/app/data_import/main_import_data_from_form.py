from app.data_import.import_data_from_form import TimesInputs


def main():
    obj_times_inputs = TimesInputs()
    data = obj_times_inputs.inputs_times_model()
    strategy_inputs_times = obj_times_inputs.strategy_times_inputs(data=data)

    return strategy_inputs_times


if __name__ == "__main__":
    main()
