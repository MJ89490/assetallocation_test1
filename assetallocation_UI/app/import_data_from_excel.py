import pandas as pd
import os

from datetime import timedelta


PATH = r'C:\Users\AJ89720\PycharmProjects\assetallocation_arp\assetallocation_UI\app\arp_dashboard_charts.xlsm'
#todo create a class

#todo create an import depending on the asset class not depending on the chart!!!

def read_data_from_excel():
    times_data = pd.read_excel(PATH, sheet_name="times_output")

    return times_data


def data_allocation_over_time_chart(times_data):

    us_equities = times_data.loc[:, 'TIMES Positions':'US Equities.2']
    us_equities = us_equities.set_index('TIMES Positions')
    us_equities = us_equities.loc['2018-09-07':'2019-10-23']
    us_equities = us_equities['US Equities.2'].tolist()

    eu_equities = times_data.loc[:, 'TIMES Positions':'EU Equities.2']
    eu_equities = eu_equities.set_index('TIMES Positions')
    eu_equities = eu_equities.loc['2018-09-07':'2019-10-23']
    eu_equities = eu_equities['EU Equities.2'].tolist()

    jp_equities = times_data.loc[:, 'TIMES Positions':'JP Equities.2']
    jp_equities = jp_equities.set_index('TIMES Positions')
    jp_equities = jp_equities.loc['2018-09-07':'2019-10-23']
    jp_equities = jp_equities['JP Equities.2'].tolist()

    hk_equities = times_data.loc[:, 'TIMES Positions':'HK Equities.2']
    hk_equities = hk_equities.set_index('TIMES Positions')
    hk_equities = hk_equities.loc['2018-09-07':'2019-10-23']
    hk_equities = hk_equities['HK Equities.2'].tolist()

    us_bonds = times_data.loc[:, 'TIMES Positions':'US 10y Bonds.2']
    us_bonds = us_bonds.set_index('TIMES Positions')
    us_bonds = us_bonds.loc['2018-09-07':'2019-10-23']
    us_bonds = us_bonds['US 10y Bonds.2'].tolist()

    uk_bonds = times_data.loc[:, 'TIMES Positions':'UK 10y Bonds.2']
    uk_bonds = uk_bonds.set_index('TIMES Positions')
    uk_bonds = uk_bonds.loc['2018-09-07':'2019-10-23']   #injecter date selectionnée avec boxes
    uk_bonds = uk_bonds['UK 10y Bonds.2'].tolist()

    eu_bonds = times_data.loc[:, 'TIMES Positions':'Eu 10y Bonds.2']
    eu_bonds = eu_bonds.set_index('TIMES Positions')
    eu_bonds = eu_bonds.loc['2018-09-07':'2019-10-23']
    eu_bonds = eu_bonds['Eu 10y Bonds.2'].tolist()

    ca_bonds = times_data.loc[:, 'TIMES Positions':'CA 10y Bonds.2']
    ca_bonds = ca_bonds.set_index('TIMES Positions')
    ca_bonds = ca_bonds.loc['2018-09-07':'2019-10-23']
    ca_bonds = ca_bonds['CA 10y Bonds.2'].tolist()

    jpy = times_data.loc[:, 'TIMES Positions':'JPY.2']

    jpy_start_date = '2018-09-07'
    jpy_end_date = '2019-10-23'

    jpy_full_dates = [str(d.date()) for d in jpy.loc[:, 'TIMES Positions'].dropna()]



    jpy_start_date_index = jpy_full_dates.index(jpy_start_date)
    jpy_end_date_index = jpy_full_dates.index(jpy_end_date) + 1

    jpy_dates_list = jpy_full_dates[jpy_start_date_index:jpy_end_date_index]


    jpy = jpy.set_index('TIMES Positions')
    jpy = jpy.loc['2018-09-07':'2019-10-23']
    jpy = jpy['JPY.2'].tolist()

    eur = times_data.loc[:, 'TIMES Positions':'EUR.2']
    eur = eur.set_index('TIMES Positions')
    eur = eur.loc['2018-09-07':'2019-10-23']
    eur = eur['EUR.2'].tolist()

    aud = times_data.loc[:, 'TIMES Positions':'AUD.2']
    aud = aud.set_index('TIMES Positions')
    aud = aud.loc['2018-09-07':'2019-10-23']
    aud = aud['AUD.2'].tolist()

    cad = times_data.loc[:, 'TIMES Positions':'CAD.2']
    cad = cad.set_index('TIMES Positions')
    cad = cad.loc['2018-09-07':'2019-10-23']
    cad = cad['CAD.2'].tolist()

    gbp = times_data.loc[:, 'TIMES Positions':'GBP.2']
    gbp = gbp.set_index('TIMES Positions')
    gbp = gbp.loc['2018-09-07':'2019-10-23']
    gbp = gbp['GBP.2'].tolist()

    return {'us_equities': us_equities , 'eu_equities': eu_equities, 'jp_equities': jp_equities, 'hk_equities': hk_equities,
     'us_bonds': us_bonds, 'uk_bonds': uk_bonds, 'eu_bonds': eu_bonds, 'ca_bonds': ca_bonds, 'jpy': jpy, 'eur': eur,
     'aud': aud, 'cad': cad, 'gbp': gbp}


    # return us_equities, eu_equities, jp_equities, hk_equities, us_bonds, uk_bonds, eu_bonds, ca_bonds, jpy, eur, aud, \
    #        cad, gbp, jpy_dates_list

def data_performance_since_inception_chart(times_data):

   data_performance = times_data.loc[:, 'TIMES Returns':'Total'] #TO CHANGE!!!
   data_performance = data_performance.set_index('TIMES Returns')
   dates = times_data.loc[:, 'TIMES Returns']
   dates = dates.tolist()
   total_performance = data_performance['Total']
   total_performance = total_performance.loc['2016-03-16':'2019-06-29']
   total_performance = total_performance.tolist()

   gbp_performance = data_performance['GBP.1']
   gbp_performance = gbp_performance.loc['2016-03-16':'2019-06-29']
   gbp_performance = gbp_performance.tolist()

   jpy_performance = data_performance['JPY.1']
   jpy_performance = jpy_performance.loc['2016-03-16':'2019-06-29']
   jpy_performance = jpy_performance.tolist()

   eur_performance = data_performance['EUR.1']
   eur_performance = eur_performance.loc['2016-03-16':'2019-06-29']
   eur_performance = eur_performance.tolist()

   aud_performance = data_performance['AUD.1']
   aud_performance = aud_performance.loc['2016-03-16':'2019-06-29']
   aud_performance = aud_performance.tolist()

   cad_performance = data_performance['CAD.1']
   cad_performance = cad_performance.loc['2016-03-16':'2019-06-29']
   cad_performance = cad_performance.tolist()

   return {'total_performance': total_performance, 'gbp_performance': gbp_performance, 'jpy_performance': jpy_performance,
           'eur_performance': eur_performance, 'aud_performance': aud_performance, 'cad_performance': cad_performance}


def data_table_times(times_data):

    data_mom = times_data.loc[:, 'TIMES Signals':'GBP']
    data_mom = data_mom.set_index('TIMES Signals')

    data_positions = times_data.loc[:, 'TIMES Positions':'GBP.2']
    data_positions = data_positions.set_index('TIMES Positions')

    data_performance_weekly = times_data.loc[:, 'TIMES Returns':'GBP.1']
    data_performance_weekly = data_performance_weekly.set_index('TIMES Returns')

    signals_off_signals = data_mom.loc[:, 'US Equities':'HK Equities'].last_valid_index()

    signals_off_performance = data_performance_weekly.loc[:, 'US Equities.1':'HK Equities.1'].last_valid_index()
    signals_off_positions = data_positions.loc[:, 'US Equities.2':'HK Equities.2'].last_valid_index()

    signals_off_performance_weekly = signals_off_performance.date()
    signals_off_performance_weekly = signals_off_performance_weekly - timedelta(days=7)
    signals_off_performance_weekly = pd.Timestamp(signals_off_performance_weekly)

    year_end = '2018-12-31'
    year_end = pd.Timestamp(year_end)

    signals = round(data_mom.loc[:, 'US Equities':'GBP'].loc[signals_off_signals], 2)
    positions = round((data_positions.loc[:, 'US Equities.2':'GBP.2'].loc[signals_off_positions])*100, 2)
    performance_weekly = round((data_performance_weekly.loc[:, 'US Equities.1': 'GBP.1'].loc[signals_off_performance]
                                     - data_performance_weekly.loc[:, 'US Equities.1': 'GBP.1'].loc[signals_off_performance_weekly])*100, 3)
    performance_ytd = round((data_performance_weekly.loc[:, 'US Equities.1': 'GBP.1'].loc[signals_off_performance]
                                     - data_performance_weekly.loc[:, 'US Equities.1': 'GBP.1'].loc[year_end])*100, 3)

    sum_positions_equities = round(sum(positions.loc['US Equities.2':'HK Equities.2']), 2)

    sum_positions_bonds = round(sum(positions.loc['US 10y Bonds.2':'CA 10y Bonds.2']), 2)

    sum_positions_fx = round(sum(positions.loc['JPY.2':'GBP.2']), 2)

    sum_performance_weekly_equities = round(sum(performance_weekly.loc['US Equities.1': 'HK Equities.1']), 2)

    sum_performance_weekly_bonds = round(sum(performance_weekly.loc['US 10y Bonds.1':'CA 10y Bonds.1']), 2)

    sum_performance_weekly_fx = round(sum(performance_weekly.loc['JPY.1':'GBP.1']), 2)

    sum_performance_ytd_equities = round(sum(performance_ytd.loc['US Equities.1': 'HK Equities.1']), 2)

    sum_performance_ytd_bonds = round(sum(performance_ytd.loc['US 10y Bonds.1':'CA 10y Bonds.1']), 2)

    sum_performance_ytd_fx = round(sum(performance_ytd.loc['JPY.1':'GBP.1']), 2)

    return {'signals': signals, 'positions': positions, 'performance_weekly': performance_weekly,
            'performance_ytd': performance_ytd, 'sum_positions_equities': sum_positions_equities,
            'sum_positions_bonds': sum_positions_bonds, 'sum_positions_fx': sum_positions_fx,
            'sum_performance_weekly_equities': sum_performance_weekly_equities,
            'sum_performance_weekly_bonds': sum_performance_weekly_bonds, 'sum_performance_weekly_fx': sum_performance_weekly_fx,
            'sum_performance_ytd_equities': sum_performance_ytd_equities, 'sum_performance_ytd_bonds': sum_performance_ytd_bonds,
            'sum_performance_ytd_fx': sum_performance_ytd_fx}

def data_sparklines_charts(times_data):

    data = times_data.loc[:, 'TIMES Signals':'GBP']
    data = data.set_index('TIMES Signals')

    data_positions = times_data.loc[:, 'TIMES Positions':'GBP.2']
    data_positions = data_positions.set_index('TIMES Positions')

    positions_us_equities_sparklines = data_positions.loc['2019-01-01':'2019-11-28', 'US Equities.2']
    positions_us_equities_sparklines = positions_us_equities_sparklines.tolist()

    positions_eu_equities_sparklines = data_positions.loc['2019-01-01':'2019-11-28', 'EU Equities.2']
    positions_eu_equities_sparklines = positions_eu_equities_sparklines.tolist()

    positions_jp_equities_sparklines = data_positions.loc['2019-01-01':'2019-11-28', 'JP Equities.2']
    positions_jp_equities_sparklines = positions_jp_equities_sparklines.tolist()

    positions_hk_equities_sparklines = data_positions.loc['2019-01-01':'2019-11-28', 'HK Equities.2']
    positions_hk_equities_sparklines = positions_hk_equities_sparklines.tolist()

    positions_us_bonds_sparklines = data_positions.loc['2019-01-01':'2019-11-28', 'US 10y Bonds.2']
    positions_us_bonds_sparklines = positions_us_bonds_sparklines.tolist()

    positions_uk_bonds_sparklines = data_positions.loc['2019-01-01':'2019-11-28', 'UK 10y Bonds.2']
    positions_uk_bonds_sparklines = positions_uk_bonds_sparklines.tolist()

    positions_eu_bonds_sparklines = data_positions.loc['2019-01-01':'2019-11-28', 'Eu 10y Bonds.2']
    positions_eu_bonds_sparklines = positions_eu_bonds_sparklines.tolist()

    positions_ca_bonds_sparklines = data_positions.loc['2019-01-01':'2019-11-28', 'CA 10y Bonds.2']
    positions_ca_bonds_sparklines = positions_ca_bonds_sparklines.tolist()

    positions_jpy_sparklines = data_positions.loc['2019-01-01':'2019-11-28', 'JPY.2']
    positions_jpy_sparklines = positions_jpy_sparklines.tolist()

    positions_eur_sparklines = data_positions.loc['2019-01-01':'2019-11-28', 'EUR.2']
    positions_eur_sparklines = positions_eur_sparklines.tolist()

    positions_aud_sparklines = data_positions.loc['2019-01-01':'2019-11-28', 'AUD.2']
    positions_aud_sparklines = positions_aud_sparklines.tolist()

    positions_cad_sparklines = data_positions.loc['2019-01-01':'2019-11-28', 'CAD.2']
    positions_cad_sparklines = positions_cad_sparklines.tolist()

    positions_gbp_sparklines = data_positions.loc['2019-01-01':'2019-11-28', 'GBP.2']
    positions_gbp_sparklines = positions_gbp_sparklines.tolist()

    return positions_us_equities_sparklines, positions_eu_equities_sparklines, positions_jp_equities_sparklines, \
           positions_hk_equities_sparklines, positions_us_bonds_sparklines, positions_uk_bonds_sparklines, \
           positions_eu_bonds_sparklines, positions_ca_bonds_sparklines, positions_jpy_sparklines, \
           positions_eur_sparklines, positions_aud_sparklines, positions_cad_sparklines, positions_gbp_sparklines


def import_dates_inputs_dashboard(times_data):

    signals_date = [str(d.date()) for d in times_data.loc[:, 'TIMES Signals'].dropna()]
    returns_date = [str(d.date()) for d in times_data.loc[:, 'TIMES Returns'].dropna()]
    positions_date = [str(d.date()) for d in times_data.loc[:, 'TIMES Positions'].dropna()]

    ################################################################################# create another fct for this
    signals_data_double = sorted(signals_date*2)
    signals_iterator = iter(signals_data_double)
    signals_date_field = list(zip(signals_iterator, signals_iterator))

    returns_data_double = sorted(returns_date*2)
    returns_iterator = iter(returns_data_double)
    returns_date_field = list(zip(returns_iterator, returns_iterator))

    positions_data_double = sorted(positions_date*2)
    positions_iterator = iter(positions_data_double)
    positions_date_field = list(zip(positions_iterator, positions_iterator))



    return signals_date_field, returns_date_field, positions_date_field


if __name__ == "__main__":
    data = read_data_from_excel()
    data_allocation_over_time_chart(data)
    data_performance_since_inception_chart(data)
    data_table_times(data)
    data_sparklines_charts(data)
    import_dates_inputs_dashboard(data)
