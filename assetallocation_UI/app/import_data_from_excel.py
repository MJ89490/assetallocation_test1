import pandas as pd
import os

PATH = r'C:\Users\AJ89720\PycharmProjects\assetallocation_arp\assetallocation_arp\assetallocation_UI\app\arp_dashboard_charts.xlsm'

#to create a class


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

    return us_equities, eu_equities, jp_equities, hk_equities, us_bonds, uk_bonds, eu_bonds, ca_bonds, jpy, eur, aud, \
           cad, gbp

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

   return total_performance, gbp_performance, jpy_performance, eur_performance, aud_performance, cad_performance, dates

def data_table_times(times_data):

    data_mom = times_data.loc[:, 'TIMES Signals':'GBP']
    data_mom = data_mom.set_index('TIMES Signals')

    data_positions = times_data.loc[:, 'TIMES Positions':]

    signals_off = data_mom.loc[:, 'US Equities':'HK Equities'].last_valid_index()

    signals = round(data_mom.loc[:, 'US Equities':'HK Equities'].loc[signals_off], 2)
    positions = data_mom.loc[:, 'US Equities':'HK Equities'].loc[signals_off]

    return signals

if __name__ == "__main__":
    data = read_data_from_excel()
    data_allocation_over_time_chart(data)
    data_performance_since_inception_chart(data)
    data_table_times(data)