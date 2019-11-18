import xlwings as xw
from assetallocation_arp.models.times import run_model


def get_inputs_from_excel():
	# Call the excel book
	wb = xw.Book.caller()

	# Select data from excel
	mat_file = xw.Range('I9').value
	input_file = xw.Range('I10').value
	model_type = xw.Range('I8').value
	#wb = xwapp.books.open(input_file)
	outputs = run_model(model_type, mat_file, input_file)
