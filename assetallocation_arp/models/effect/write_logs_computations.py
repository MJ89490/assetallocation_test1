import xlwings as xw


def write_logs_effect(current_calc: str, cell: str or int, flag_curr=None):

    sheet_effect_input = xw.Book.caller().sheets['EFFECT']

    if flag_curr:
        sheet_effect_input.range(f'C{cell}').value = current_calc
    else:
        sheet_effect_input.range(cell).value = current_calc


def remove_logs_effect():

    sheet_effect_input = xw.Book.caller().sheets['EFFECT']

    if sheet_effect_input.range("logs_inflation_release").value is not None:
        last_row = sheet_effect_input.range("logs_inflation_release").end('down').row
        last_row_curr = sheet_effect_input.range("C8").end('down').row
        for cell in range(8, last_row+1):
            sheet_effect_input.range(f"B{cell}").value = float('NaN')
        for cell in range(8, last_row_curr+1):
            sheet_effect_input.range(f"C{cell}").value = float('NaN')
