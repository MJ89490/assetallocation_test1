from typing import Tuple

from assetallocation_UI import TimesInputs
from assetallocation_UI import InputsTimesModel
from assetallocation_arp.data_etl.dal.data_models.strategy import Times


def get_times_inputs(form: InputsTimesModel) -> Tuple[str, float, Times]:
    """
    Main function to run the TimesInputs() class
    :return: inputs data from the Flask form
    """
    times_inputs = TimesInputs(form)
    return form.fund_name.data, form.strategy_weight.data, times_inputs.inputs_times_model()
