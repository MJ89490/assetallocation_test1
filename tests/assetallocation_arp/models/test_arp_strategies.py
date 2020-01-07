"""

 Created on 12/11/2019

 Author: AJ89720

 email: Anais.Jeremie@lgim.com

 """

import pytest

from assetallocation_arp.arp_strategies import get_inputs_from_excel


@pytest.mark.parametrize("model",

                         ["time", "", "conca"])
def test_get_inputs_from_excel_exception(model):
    """

    :param model: name of the model

    :return: an exception because the name of the model is wrong

    """

    with pytest.raises(NameError) as e:
        assert get_inputs_from_excel(model)

    assert str(e.value) == "Your input is incorrect."
