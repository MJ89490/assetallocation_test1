import xlwings as xw
import data_etl.import_data as gd
import models.times as times
import sys
import os

from assetallocation_arp.enum import models_names as models


def run_model(model_type, mat_file=None, input_file=None):

	if model_type == models.Models.times.name:
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


def run_model_from_ui(path_excel_times, model_type, times_inputs, mat_file, input_file=None):

	if model_type == models.Models.times.name:
		# get inputs from excel and matlab data
		asset_inputs, all_data = gd.extract_inputs_from_ui_and_mat_data(model_type, mat_file, input_file)
		# run strategy
		signals, returns, r, positioning = times.format_data_and_calc(times_inputs, asset_inputs, all_data)
		# write results to output sheet
		write_output_to_excel({models.Models.times.name: (asset_inputs, positioning, r, signals, times_inputs)}, path_excel_times=path_excel_times)


def write_output_to_excel(model_outputs, path_excel_times):

	if models.Models.times.name in model_outputs.keys():

		asset_inputs, positioning, returns, signals, times_inputs = model_outputs[models.Models.times.name]
		# path = os.path.join(os.path.dirname(__file__), "times_model.xls")

		wb = xw.Book()

		wb.sheets.add('signal')
		wb.sheets.add('returns')
		wb.sheets.add('positioning')

		sheet_times_signals_output = wb.sheets['signal']
		sheet_times_returns_output = wb.sheets['returns']
		sheet_times_positioning_output = wb.sheets['positioning']
		# sheet_times_input = wb.sheets['input']

		# n_columns = len(signals.columns) + 2
		n_rows = signals.shape[0]
		range_str = 'A2:A%s' % n_rows

		sheet_times_signals_output.range('A1').value = "TIMES Signals"
		sheet_times_signals_output.range(range_str).value = signals

		sheet_times_returns_output.range('A1').value = "TIMES Returns"
		sheet_times_returns_output.range(range_str).value = returns

		sheet_times_positioning_output.range('A1').value = "TIMES Returns"
		sheet_times_positioning_output.range(range_str).value = positioning


		# sheet_times_output.range('rng_times_output').offset(0, 0).value = "TIMES Signals"
		# sheet_times_output.range('rng_times_output').value = signals
		# sheet_times_output.range('rng_times_output').offset(-1, n_columns + 2).value = "TIMES Returns"
		# sheet_times_output.range('rng_times_output').offset(0, n_columns + 2).value = returns
		# sheet_times_output.range('rng_times_output').offset(-1, 2 * n_columns + 4).value = "TIMES Positions"
		# sheet_times_output.range('rng_times_output').offset(0, 2 * n_columns + 4).value = positioning
		# write inputs used to excel and run time
		#sheet_times_input.range('rng_inputs_used').offset(-1, 1).value = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		# sheet_times_input.range('rng_inputs_used').value = asset_inputs
		# sheet_times_input.range('rng_inputs_used').offset(0, 7).value = times_inputs

		app = xw.apps.active
		wb.save(path=path_excel_times)
		app.quit()


def get_inputs_from_excel():
	# select data from excel
	mat_file = xw.Range('rng_mat_file_path').value
	model_type = xw.Range('rng_model_type').value
	# run selected model
	run_model(model_type, mat_file, xw.Book.caller().fullname)


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


def get_inputs_from_flask(model_type, times_inputs, path_excel):
	# launch the script from UI
	mat_file = None
	run_model_from_ui(model_type=model_type, times_inputs=times_inputs, mat_file=mat_file, path_excel_times=path_excel)


def get_input_user():
	model_str = input("Choose a Model: ")
	return model_str


if __name__ == "__main__":
	sys.exit(get_inputs_from_python(get_input_user()))
