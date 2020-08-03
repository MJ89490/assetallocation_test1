from assetallocation_UI.aa_web_app.data_import.import_data_from_form import TimesInputs
from assetallocation_UI.aa_web_app.forms import InputsTimesModel


def main_form():
    """
    Main function to run the TimesInputs() class
    :return: inputs data from the Flask form
    """
    obj_times_inputs = TimesInputs(form=InputsTimesModel())
    data = obj_times_inputs.inputs_times_model()
    strategy_inputs_times = obj_times_inputs.strategy_times_inputs(data=data)

    return strategy_inputs_times


if __name__ == "__main__":
    main_form()
