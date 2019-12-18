import xlwings as xw
import data_etl.import_data as gd
import models.times as times
from time import gmtime, strftime
import enum
import sys
import os

class Models(enum.Enum):
	times = 0
	maven = 1
	effect = 2
	curp = 3
	fica = 4
	factor = 5
	comca = 6

def run_model(model_type, mat_file=None, input_file=None):

	if model_type == Models.times.name:
		# get inputs from excel and matlab data
		times_inputs, asset_inputs, all_data = gd.extract_inputs_and_mat_data(model_type, mat_file, input_file)
		# run strategy
		signals, returns, r, positioning = times.format_data_and_calc(times_inputs, asset_inputs, all_data)
		# write results to output sheet
		write_output_to_excel({Models.times.name: (asset_inputs, positioning, r, signals, times_inputs)})

	if model_type == Models.maven.name:
		print(model_type)
	if model_type == Models.effect.name:
		print(model_type)
	if model_type == Models.curp.name:
		print(model_type)
	if model_type == Models.fica.name:
		print(model_type)
	if model_type == Models.factor.name:
		print(model_type)
	if model_type == Models.comca.name:
		print(model_type)

def write_output_to_excel(model_outputs):

	if Models.times.name in model_outputs.keys():
		asset_inputs, positioning, returns, signals, times_inputs = model_outputs[Models.times.name]
		path = os.path.join(os.path.dirname(__file__), "times_model.xls")
		wb = xw.Book(path)
		sheet_times_output = wb.sheets['output']
		sheet_times_input = wb.sheets['input']

		n_columns = len(signals.columns) + 2
		sheet_times_output.range('rng_times_output').offset(-1, 0).value = "TIMES Signals"
		sheet_times_output.range('rng_times_output').value = signals
		sheet_times_output.range('rng_times_output').offset(-1, n_columns + 2).value = "TIMES Returns"
		sheet_times_output.range('rng_times_output').offset(0, n_columns + 2).value = returns
		sheet_times_output.range('rng_times_output').offset(-1, 2 * n_columns + 4).value = "TIMES Positions"
		sheet_times_output.range('rng_times_output').offset(0, 2 * n_columns + 4).value = positioning
		# write inputs used to excel and run time
		#sheet_times_input.range('rng_inputs_used').offset(-1, 1).value = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		sheet_times_input.range('rng_inputs_used').value = asset_inputs
		sheet_times_input.range('rng_inputs_used').offset(0, 7).value = times_inputs

def get_inputs_from_excel():
	# select data from excel
	# mat_file = xw.Range('rng_mat_file_path').value
	# model_type = xw.Range('rng_model_type').value
	# mock_caller = xw.Book.caller().fullname
	# # run selected model
	# run_model(model_type, mat_file, mock_caller)

	#launch the script from Python
	mat_file = None
	input_file = None
	modelsList = [Models.times.name, Models.maven.name, Models.effect.name, Models.curp.name,
				  Models.fica.name, Models.factor.name, Models.comca.name]

	modelsStr = input("Choose a Model: ")
	if modelsStr in modelsList:
		model_type = modelsStr
		run_model(model_type, mat_file, input_file)
	else:
		raise NameError("Your input is incorrect.")

if __name__ == "__main__":
	sys.exit(get_inputs_from_excel())