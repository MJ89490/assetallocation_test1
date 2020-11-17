import xlwings as xw


def write_logs_effect(current_calc: str, cell: str or int, flag_curr=None):
    xw.Book("arp_dashboard_effect.xlsm").set_mock_caller()
    sheet_effect_input = xw.Book.caller().sheets['EFFECT']

    if flag_curr:
        sheet_effect_input.range(f'D{cell+11}').value = current_calc[:3]
    else:
        sheet_effect_input.range(cell).value = current_calc
