import xlwings as xw
import data_etl.import_data as gd
import models.times as times


def run_model(model_type, mat_file=None, input_file=None):
	if model_type == "times":

		times_inputs, asset_inputs, all_data = gd.extract_inputs_and_mat_data(model_type, mat_file, input_file)
		signals, returns, r, positioning = times.format_data_and_calc(times_inputs, asset_inputs, all_data)

	return signals, returns, r, positioning


def get_inputs_from_excel():
	# Call the excel book

	# Select data from excel
	mat_file = xw.Range('I9').value
	input_file = xw.Range('I10').value
	model_type = xw.Range('I8').value

	signals, returns, r, positioning = run_model(model_type, mat_file, input_file)
	return signals, returns, r, positioning

