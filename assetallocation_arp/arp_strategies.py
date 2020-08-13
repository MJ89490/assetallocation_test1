import pandas as pd
import assetallocation_arp.data_etl.import_all_data as gd
import assetallocation_arp.models.times as times
import sys

from assetallocation_arp.common_libraries.models_names import Models as models


def run_model(model_type, mat_file=None, input_file=None):

	if model_type == models.times.name:
		# get inputs from excel and matlab data
		times_inputs, asset_inputs, all_data = gd.extract_inputs_and_mat_data(model_type, mat_file, input_file)
		# run strategy
		signals, returns, r, positioning = times.format_data_and_calc(times_inputs, asset_inputs, all_data)
		# write results to output sheet
		write_output_to_excel({models.Models.times.name: (asset_inputs, positioning, r, signals, times_inputs)})

	if model_type == models.Models.maven.name:
		print(model_type)
	if model_type == models.Models.effect.name:
		print(model_type)
	if model_type == models.Models.curp.name:
		print(model_type)
	if model_type == models.Models.fica.name:
		print(model_type)
	if model_type == models.Models.factor.name:
		print(model_type)
	if model_type == models.Models.comca.name:
		print(model_type)


def run_model_from_web_interface(model_type, mat_file=None, input_file=None):

	if model_type == models.times.name:
		# get inputs from excel and matlab data
		times_inputs, asset_inputs, all_data = gd.extract_inputs_and_mat_data(model_type, mat_file, input_file)
		# run strategy
		signals, returns, r, positioning = times.format_data_and_calc(times_inputs, asset_inputs, all_data)

		return asset_inputs, positioning, r, signals, times_inputs


def write_output_to_excel(model_outputs, path_excel_times):

	if models.times.name in model_outputs.keys():
		positioning, returns, signals = model_outputs[models.times.name]
		with pd.ExcelWriter(path_excel_times, engine='xlswriter') as writer:
			signals.to_excel(writer, sheet_name='signal', encoding='utf8')
			returns.to_excel(writer, sheet_name='returns', encoding='utf8')
			positioning.to_excel(writer, sheet_name='positioning', encoding='utf8')
			writer.save()
			writer.close()
		writer.save()

def get_inputs_from_python(model):
	#launch the script from Python
	# launch the script from Python
	mat_file = None
	input_file = None
	models_list = [model.name for model in models.Models]

	if model in models_list:
		model_type = model
		run_model(model_type, mat_file, input_file)
	else:
		raise NameError("Your input is incorrect.")


def get_input_user():
	model_str = input("Choose a Model: ")
	return model_str


if __name__ == "__main__":
	sys.exit(get_inputs_from_python(get_input_user()))
