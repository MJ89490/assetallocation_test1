import xlwings as xw
import data_etl.import_data as gd
import models.times as times
import models.fica as fica
import models.maven as maven
import models.fxmodels as fxmodels
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
		maven_returns = maven.calculate_excess_returns(maven_inputs, asset_inputs, asset_returns)
		# calculate value and momentum scores, and the top/bottom countries on the combination score
		momentum, value, long_signals, short_signals, long_signals_name, short_signals_name, value_last, \
											momentum_last, long_list, short_list, volatility = \
													maven.calculate_signals(maven_inputs, maven_returns)
		# calculate maven return series, and benchmarks, asset class exposures and contributions
		returns_maven, asset_class_long, asset_class_short, asset_contribution_long, asset_contribution_short = \
		maven.run_performance_stats(maven_inputs, asset_inputs, maven_returns, volatility, long_signals, short_signals)
		# write results to output sheet
		write_output_to_excel({models.Models.maven.name: (momentum, value, long_signals_name, short_signals_name, \
				value_last, momentum_last, long_list, short_list, returns_maven, asset_class_long, \
				asset_class_short, asset_contribution_long, asset_contribution_short, asset_inputs, maven_inputs)})

	if model_type == models.Models.effect.name:
		print(model_type)

	if model_type == models.Models.fxmodels.name:
		# get inputs from excel and matlab data
		fxmodels_inputs, asset_inputs, all_data = gd.extract_inputs_and_mat_data(model_type, mat_file, input_file)
		# create the input series for the signal types
		spot, carry, cash, ppp = fxmodels.format_data(fxmodels_inputs, asset_inputs, all_data)
		# calculate signals
		signal, volatility = fxmodels.calculate_signals(fxmodels_inputs, spot, carry, cash, ppp)
		# determine exposures
		fx_model, exposure, exposure_agg = fxmodels.determine_sizing(fxmodels_inputs, asset_inputs, signal, volatility)
		# calculate returns
		base_fx, returns, contribution, carry_base = fxmodels.calculate_returns(fxmodels_inputs, carry, signal, \
													exposure, exposure_agg)
		# write results to output sheet
		write_output_to_excel({models.Models.fxmodels.name: (fx_model, base_fx, signal, exposure, exposure_agg, \
													returns, contribution, carry_base, fxmodels_inputs, asset_inputs)})

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
		momentum, value, long_signals_name, short_signals_name, value_last, momentum_last, long_list, \
			short_list, returns_maven, asset_class_long, asset_class_short, asset_contribution_long, \
			asset_contribution_short, asset_inputs, maven_inputs = model_outputs[models.Models.maven.name]
		path = os.path.join(os.path.dirname(__file__), "arp_dashboard.xlsm")
		wb = xw.Book(path)
		sheet_maven_output = wb.sheets['maven_output']
		sheet_maven_input = wb.sheets['maven_input']

		ncol = len(value.columns) + 3
		mcol = len(long_signals_name.columns) + 3
		sheet_maven_output.clear_contents()
		sheet_maven_output.range('rng_maven_output').offset(-1, 0).value = "Value Scores"
		sheet_maven_output.range('rng_maven_output').value = value
		sheet_maven_output.range('rng_maven_output').offset(-1, ncol).value = "Momentum Scores"
		sheet_maven_output.range('rng_maven_output').offset(0, ncol).value = momentum
		sheet_maven_output.range('rng_maven_output').offset(-1, 2 * ncol).value = "Long Asset Signals"
		sheet_maven_output.range('rng_maven_output').offset(0, 2 * ncol).value = long_signals_name
		sheet_maven_output.range('rng_maven_output').offset(-1, 2 * ncol + mcol).value = "Short Asset Signals"
		sheet_maven_output.range('rng_maven_output').offset(0, 2 * ncol + mcol).value = short_signals_name
		sheet_maven_output.range('rng_maven_output').offset(-1, 2 * ncol + 2 * mcol).value = "Value Last"
		sheet_maven_output.range('rng_maven_output').offset(0, 2 * ncol + 2 * mcol).value = value_last
		sheet_maven_output.range('rng_maven_output').offset(-1, 2 * ncol + 2 * mcol + 2).value = "Momentum Last"
		sheet_maven_output.range('rng_maven_output').offset(0, 2 * ncol + 2 * mcol + 2).value = momentum_last
		sheet_maven_output.range('rng_maven_output').offset(-1, 2 * ncol + 2 * mcol + 8).value = "Long Exposures"
		sheet_maven_output.range('rng_maven_output').offset(0, 2 * ncol + 2 * mcol + 8).value = long_list
		sheet_maven_output.range('rng_maven_output').offset(-1, 2 * ncol + 2 * mcol + 10).value = "Short Exposures"
		sheet_maven_output.range('rng_maven_output').offset(0, 2 * ncol + 2 * mcol + 10).value = short_list
		sheet_maven_output.range('rng_maven_output').offset(-1, 2 * ncol + 2 * mcol + 14).value = "Maven Returns"
		sheet_maven_output.range('rng_maven_output').offset(0, 2 * ncol + 2 * mcol + 14).value = returns_maven
		sheet_maven_output.range('rng_maven_output').offset(-1, 2 * ncol + 2 * mcol + 23).value = "Asset Class %L"
		sheet_maven_output.range('rng_maven_output').offset(0, 2 * ncol + 2 * mcol + 23).value = asset_class_long
		sheet_maven_output.range('rng_maven_output').offset(-1, 2 * ncol + 2 * mcol + 32).value = "Asset Class %S"
		sheet_maven_output.range('rng_maven_output').offset(0, 2 * ncol + 2 * mcol + 32).value = asset_class_short
		sheet_maven_output.range('rng_maven_output').offset(-1, 2 * ncol + 2 * mcol + 41).value = "Asset Contribution L"
		sheet_maven_output.range('rng_maven_output').offset(0, 2 * ncol + 2 * mcol + 41).value = asset_contribution_long
		sheet_maven_output.range('rng_maven_output').offset(-1, 2 * ncol + 2 * mcol + 50).value = "Asset Contribution S"
		sheet_maven_output.range('rng_maven_output').offset(0, 2 * ncol + 2 * mcol + 50).value = asset_contribution_short
		# write inputs used to excel and run time
		#sheet_maven_input.range('rng_inputs_used').offset(-1, 1).value = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		sheet_maven_input.range('rng_input_maven_used').value = maven_inputs
		sheet_maven_input.range('rng_input_maven_used').offset(3, 0).value = asset_inputs

	if models.Models.fxmodels.name in model_outputs.keys():
		fx_model, base_fx, signal, exposure, exposure_agg, returns, contribution, carry_base, fxmodels_inputs, \
													asset_inputs = model_outputs[models.Models.fxmodels.name]
		path = os.path.join(os.path.dirname(__file__), "arp_dashboard.xlsm")
		wb = xw.Book(path)
		sheet_fxmodels_output = wb.sheets['fxmodels_output']
		sheet_fxmodels_input = wb.sheets['fxmodels_input']

		ncol = len(signal.columns) + 3
		mcol = len(exposure_agg.columns) + 3
		sheet_fxmodels_output.clear_contents()
		sheet_fxmodels_output.range('rng_fxmodels_output').offset(-1, 1).value = fx_model
		sheet_fxmodels_output.range('rng_fxmodels_output').offset(-1, 2).value = base_fx
		sheet_fxmodels_output.range('rng_fxmodels_output').offset(-1, 0).value = "Signals"
		sheet_fxmodels_output.range('rng_fxmodels_output').value = signal
		sheet_fxmodels_output.range('rng_fxmodels_output').offset(-1, ncol).value = "Exposures per Cross"
		sheet_fxmodels_output.range('rng_fxmodels_output').offset(0, ncol).value = exposure
		sheet_fxmodels_output.range('rng_fxmodels_output').offset(-1, 2 * ncol).value = "Exposures per FX"
		sheet_fxmodels_output.range('rng_fxmodels_output').offset(0, 2 * ncol).value = exposure_agg
		sheet_fxmodels_output.range('rng_fxmodels_output').offset(-1, 2 * ncol + mcol).value = "Contribution per FX"
		sheet_fxmodels_output.range('rng_fxmodels_output').offset(0, 2 * ncol + mcol).value = contribution
		sheet_fxmodels_output.range('rng_fxmodels_output').offset(-1, 2 * ncol + 2 * mcol).value = "FX Returns vs Base"
		sheet_fxmodels_output.range('rng_fxmodels_output').offset(0, 2 * ncol + 2 * mcol).value = carry_base
		sheet_fxmodels_output.range('rng_fxmodels_output').offset(-1, 2 * ncol + 3 * mcol).value = "Returns"
		sheet_fxmodels_output.range('rng_fxmodels_output').offset(0, 2 * ncol + 3 * mcol).value = returns
		# write inputs used to excel and run time
		#sheet_maven_input.range('rng_inputs_used').offset(-1, 1).value = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		sheet_fxmodels_input.range('rng_input_fxmodels_used').value = fxmodels_inputs
		sheet_fxmodels_input.range('rng_input_fxmodels_used').offset(3, 0).value = asset_inputs


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