import xlwings as xw
import data_etl.import_data as gd
import models.times as times
from time import gmtime, strftime


def run_model(model_type, mat_file=None, input_file=None):

	if model_type == "times":
		# get inputs from excel and matlab data
		times_inputs, asset_inputs, all_data = gd.extract_inputs_and_mat_data(model_type, mat_file, input_file)

		# write inputs used to excel and run time
		xw.Range('rng_inputs_used').offset(-1, 1).value = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		xw.Range('rng_inputs_used').value = times_inputs
		xw.Range('rng_inputs_used').offset(3, 0).value = asset_inputs

		signals, returns, r, positioning = times.format_data_and_calc(times_inputs, asset_inputs, all_data)
		
		# write results to output sheet
		n_columns = len(signals.columns) + 2
		xw.Range('rng_times_output').offset(-1, 0).value = "TIMES Signals"
		xw.Range('rng_times_output').value = signals
		xw.Range('rng_times_output').offset(-1, n_columns + 2).value = "TIMES Returns"
		xw.Range('rng_times_output').offset(0, n_columns + 2).value = returns
		xw.Range('rng_times_output').offset(-1, 2 * n_columns + 4).value = "TIMES Positions"
		xw.Range('rng_times_output').offset(0, 2 * n_columns + 4).value = positioning

	if model_type == "maven":
		print(model_type)
	if model_type == "effect":
		print(model_type)
	if model_type == "curp":
		print(model_type)
	if model_type == "fica":
		print(model_type)
	if model_type == "factor":
		print(model_type)
	if model_type == "comca":
		print(model_type)


def get_inputs_from_excel():

	# Select data from excel
	mat_file = xw.Range('rng_mat_file_path').value
	model_type = xw.Range('rng_model_type').value

	run_model(model_type, mat_file, xw.Book.caller().fullname)


