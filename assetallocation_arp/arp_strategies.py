import xlwings as xw
import data_etl.import_data as gd
import models.times as times
import models.fica as fica
import models.maven as maven
import sys
import os

from assetallocation_arp.enum import models_names as models


def run_model(model_type, mat_file=None, input_file=None, model_date=None):

	if model_type == models.Models.times.name:
		# get inputs from excel and matlab data
		times_inputs, asset_inputs, all_data = gd.extract_inputs_and_mat_data(model_type, mat_file, input_file)
		# run strategy
		signals, returns, r, positioning = times.format_data_and_calc(times_inputs, asset_inputs, all_data)
		# write results to output sheet
		write_output_to_excel({models.Models.times.name: (asset_inputs, positioning, r, signals, times_inputs)})

	if model_type == models.Models.maven.name:
		# get inputs from excel and matlab data
		maven_inputs, asset_inputs, all_data = gd.extract_inputs_and_mat_data(model_type, mat_file, input_file,
																			model_date)
		# calculate asset return index series and and maven's excess return index series
		asset_returns = maven.format_data(maven_inputs, asset_inputs, all_data)
		maven_returns = maven.calculating_excess_returns(maven_inputs, asset_inputs, asset_returns)
		# calculate value and momentum scores, and the top/bottom countries on the combination score
		momentum, value, long_signals, short_signals, long_signals_name, short_signals_name, value_last, \
											momentum_last, long_exposures, short_exposures, volatility = \
														maven.calculating_signals(maven_inputs, maven_returns)
		# calculate the maven return series
		returns_maven, asset_class_long, asset_class_short,asset_contribution_long, asset_contribution_short = \
		 maven.run_performance_stats(maven_inputs, asset_inputs, maven_returns, volatility, long_signals, short_signals)
		# write results to output sheet
		write_output_to_excel({models.Models.maven.name: (momentum, value, long_signals_name, short_signals_name, \
					value_last, momentum_last, long_exposures, short_exposures, returns_maven, asset_class_long, \
				asset_class_short, asset_contribution_long, asset_contribution_short, asset_inputs, maven_inputs)})

	if model_type == models.Models.effect.name:
		print(model_type)

	if model_type == models.Models.curp.name:
		curp_inputs, asset_inputs, all_data = gd.extract_inputs_and_mat_data(model_type, mat_file, input_file)
		print(model_type)

	if model_type == models.Models.fica.name:
		# get inputs from excel and matlab data
		fica_inputs, asset_inputs, all_data = gd.extract_inputs_and_mat_data(model_type, mat_file, input_file,
																			model_date)
		# create yield curves and calculate carry & roll down
		curve = fica.format_data(fica_inputs, asset_inputs, all_data)
		carry_roll, country_returns = fica.calculate_carry_roll_down(fica_inputs, asset_inputs, curve)
		# run strategy
		signals, cum_contribution, returns = fica.calculate_signals_and_returns(fica_inputs, carry_roll,
																			country_returns)
		# run daily attributions
		carry_daily, return_daily = fica.run_daily_attribution(fica_inputs, asset_inputs, all_data, signals)
		# write results to output sheet
		write_output_to_excel({models.Models.fica.name: (carry_roll, signals, country_returns, cum_contribution,
													returns, asset_inputs, fica_inputs, carry_daily, return_daily)})
	if model_type == models.Models.factor.name:
		print(model_type)
	if model_type == models.Models.comca.name:
		print(model_type)


def write_output_to_excel(model_outputs):

	if models.Models.times.name in model_outputs.keys():
		asset_inputs, positioning, returns, signals, times_inputs = model_outputs[models.Models.times.name]
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
		# sheet_times_input.range('rng_inputs_used').offset(-1, 1).value = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		sheet_times_input.range('rng_input_times_used').value = asset_inputs
		sheet_times_input.range('rng_input_times_used').offset(0, 7).value = times_inputs

	if models.Models.fica.name in model_outputs.keys():
		carry_roll, signals, country_returns, cum_contribution, returns, asset_inputs, fica_inputs, carry_daily, \
																return_daily = model_outputs[models.Models.fica.name]
		path = os.path.join(os.path.dirname(__file__), "arp_dashboard.xlsm")
		wb = xw.Book(path)
		sheet_fica_output = wb.sheets['fica_output']
		sheet_fica_input = wb.sheets['fica_input']

		n_columns = len(carry_roll.columns) + 3
		sheet_fica_output.clear_contents()
		sheet_fica_output.range('rng_fica_output').offset(-1, 0).value = "FICA Carry & Roll"
		sheet_fica_output.range('rng_fica_output').value = carry_roll
		sheet_fica_output.range('rng_fica_output').offset(-1, n_columns).value = "FICA Signals"
		sheet_fica_output.range('rng_fica_output').offset(0, n_columns).value = signals
		sheet_fica_output.range('rng_fica_output').offset(-1, 2 * n_columns + 1).value = "FICA Country Returns"
		sheet_fica_output.range('rng_fica_output').offset(0, 2 * n_columns + 1).value = country_returns
		sheet_fica_output.range('rng_fica_output').offset(-1, 3 * n_columns + 1).value = "FICA Contributions"
		sheet_fica_output.range('rng_fica_output').offset(0, 3 * n_columns + 1).value = cum_contribution
		sheet_fica_output.range('rng_fica_output').offset(-1, 4 * n_columns + 2).value = "FICA Returns"
		sheet_fica_output.range('rng_fica_output').offset(0, 4 * n_columns + 2).value = returns
		sheet_fica_output.range('rng_fica_output').offset(-1, 4 * n_columns + 9).value = "FICA Daily Carry"
		sheet_fica_output.range('rng_fica_output').offset(0, 4 * n_columns + 9).value = carry_daily
		sheet_fica_output.range('rng_fica_output').offset(-1, 5 * n_columns + 12).value = "FICA Daily Returns"
		sheet_fica_output.range('rng_fica_output').offset(0, 5 * n_columns + 12).value = return_daily
		# write inputs used to excel and run time
		#sheet_fica_input.range('rng_inputs_used').offset(-1, 1).value = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		sheet_fica_input.range('rng_input_fica_used').value = fica_inputs
		sheet_fica_input.range('rng_input_fica_used').offset(3, 0).value = asset_inputs

	if models.Models.maven.name in model_outputs.keys():
		momentum, value, long_signals_name, short_signals_name, value_last, momentum_last, long_exposures, \
				short_exposures, returns_maven, asset_class_long, asset_class_short, asset_contribution_long, \
					asset_contribution_short, asset_inputs, maven_inputs = model_outputs[models.Models.maven.name]
		path = os.path.join(os.path.dirname(__file__), "arp_dashboard.xlsm")
		wb = xw.Book(path)
		sheet_maven_output = wb.sheets['maven_output']
		sheet_maven_input = wb.sheets['maven_input']

		n_columns = len(value.columns) + 3
		m_columns = len(long_signals_name.columns) + 3
		sheet_maven_output.clear_contents()
		sheet_maven_output.range('rng_maven_output').offset(-1, 0).value = "Value Scores"
		sheet_maven_output.range('rng_maven_output').value = value
		sheet_maven_output.range('rng_maven_output').offset(-1, n_columns).value = "Momentum Scores"
		sheet_maven_output.range('rng_maven_output').offset(0, n_columns).value = momentum
		sheet_maven_output.range('rng_maven_output').offset(-1, 2 * n_columns).value = "Long Asset Signals"
		sheet_maven_output.range('rng_maven_output').offset(0, 2 * n_columns).value = long_signals_name
		sheet_maven_output.range('rng_maven_output').offset(-1, 2 * n_columns + m_columns).value = "Short Asset Signals"
		sheet_maven_output.range('rng_maven_output').offset(0, 2 * n_columns + m_columns).value = short_signals_name
		sheet_maven_output.range('rng_maven_output').offset(-1, 2 * n_columns + 2 * m_columns).value = "Value Last"
		sheet_maven_output.range('rng_maven_output').offset(0, 2 * n_columns + 2 * m_columns).value = value_last
		sheet_maven_output.range('rng_maven_output').offset(-1, 2 * n_columns + 2*m_columns+2).value = "Momentum Last"
		sheet_maven_output.range('rng_maven_output').offset(0, 2 * n_columns + 2 * m_columns + 2).value = momentum_last
		sheet_maven_output.range('rng_maven_output').offset(-1, 2 * n_columns + 2*m_columns+7).value = "Long Exposures"
		sheet_maven_output.range('rng_maven_output').offset(0, 2 * n_columns + 2 * m_columns + 7).value = long_exposures
		sheet_maven_output.range('rng_maven_output').offset(-1, 2*n_columns + 2*m_columns+9).value = "Short Exposures"
		sheet_maven_output.range('rng_maven_output').offset(0, 2*n_columns + 2*m_columns+9).value = short_exposures
		sheet_maven_output.range('rng_maven_output').offset(-1, 2*n_columns + 2*m_columns+13).value = "Maven Returns"
		sheet_maven_output.range('rng_maven_output').offset(0, 2*n_columns + 2*m_columns+13).value = returns_maven
		sheet_maven_output.range('rng_maven_output').offset(-1, 2*n_columns + 2*m_columns+22).value = "Asset Class %L"
		sheet_maven_output.range('rng_maven_output').offset(0, 2*n_columns + 2*m_columns+22).value = asset_class_long
		sheet_maven_output.range('rng_maven_output').offset(-1, 2*n_columns + 2*m_columns+31).value = "Asset Class %S"
		sheet_maven_output.range('rng_maven_output').offset(0, 2*n_columns + 2*m_columns+31).value = asset_class_short
		sheet_maven_output.range('rng_maven_output').offset(-1,2*n_columns+2*m_columns+40).value="Asset Contribution L"
		sheet_maven_output.range('rng_maven_output').offset(0,2*n_columns+2*m_columns+40).value=asset_contribution_long
		sheet_maven_output.range('rng_maven_output').offset(-1,2*n_columns+2*m_columns+49).value="Asset Contribution S"
		sheet_maven_output.range('rng_maven_output').offset(0,2*n_columns+2*m_columns+49).value=asset_contribution_short
		# write inputs used to excel and run time
		#sheet_maven_input.range('rng_inputs_used').offset(-1, 1).value = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		sheet_maven_input.range('rng_input_maven_used').value = maven_inputs
		sheet_maven_input.range('rng_input_maven_used').offset(3, 0).value = asset_inputs



def get_inputs_from_excel():
	# select data from excel
	input_file = None
	model_date = None
	mat_file = xw.Range('rng_mat_file_path').value

	model_type = xw.Range('rng_model_type').value
	run_model(model_type, mat_file, input_file, model_date)

	# run selected model
	#run_model(model_type, mat_file, xw.Book.caller().fullname)
#


def get_inputs_from_python(model):
	#launch the script from Python
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
