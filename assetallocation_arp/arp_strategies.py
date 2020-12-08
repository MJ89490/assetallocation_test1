import os
import sys

ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
print(ROOT_DIR)
sys.path.insert(0, ROOT_DIR)

from assetallocation_arp.data_etl import import_data_from_excel_matlab as gd
from assetallocation_arp.models import times
from assetallocation_arp.common_libraries import models_names
from assetallocation_arp.models.effect.main_effect import run_effect

# TODO ADD JESS CHANGES FOR TIMES


def run_model(model_type, mat_file, strategy_inputs, asset_inputs):

    # if model_type == models_names.Models.times.name:
    #     # get inputs_effect from excel and matlab data
    #     times_inputs, asset_inputs, all_data = gd.extract_inputs_and_mat_data(model_type, mat_file, input_file)
    #     # run strategy
    #     signals, returns, r, positioning = times.format_data_and_calc(times_inputs, asset_inputs, all_data)
    #     # write results to output sheet
    #     write_output_to_excel({models_names.Models.times.name: (asset_inputs, positioning, r, signals, times_inputs)}, input_file)

    if model_type == models_names.Models.maven.name:
        print(model_type)

    if model_type == models_names.Models.effect.name:
        all_data = gd.extract_inputs_and_mat_data(model_type, mat_file)

        outputs_effect, write_logs = run_effect(strategy_inputs, all_data=all_data)

        return outputs_effect, write_logs

    if model_type == models_names.Models.curp.name:
        print(model_type)
    if model_type == models_names.Models.fica.name:
        print(model_type)
    if model_type == models_names.Models.factor.name:
        print(model_type)
    if model_type == models_names.Models.comca.name:
        print(model_type)


def run_effect_strategy(strategy_inputs, asset_inputs):
    model_type = 'effect'
    mat_file = r"S:\Shared\IT\MultiAsset\Data\Arquive\Sep2020\matlabData.mat"

    # run selected model
    effect_output, write_logs = run_model(model_type, mat_file, strategy_inputs, asset_inputs)

    return effect_output, write_logs




