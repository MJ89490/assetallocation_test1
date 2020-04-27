from assetallocation_UI.app.import_data_from_excel import read_data_from_excel, data_allocation_over_time_chart

times_data = read_data_from_excel()
positions_us_equities, positions_eu_equities, positions_jp_equities, positions_hk_equities, positions_us_bonds, \
positions_uk_bonds, positions_eu_bonds, positions_ca_bonds, positions_jpy, positions_eur, positions_aud, \
positions_cad, positions_gbp, jpy_dates_list = data_allocation_over_time_chart(times_data)





