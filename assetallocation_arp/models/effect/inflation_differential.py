
"""
    Class to make inflation differential calculations
"""

import pandas as pd
import numpy as np
import os
import common_libraries.constants as constants
from models.effect.inflation_imf_publishing_dates import dates_imf_publishing
from assetallocation_arp.data_etl.imf_data_download import scrape_imf_data
from assetallocation_arp.common_libraries.names_columns_dataframe import CurrencySpot
from assetallocation_arp.common_libraries.names_currencies_spot import CurrencyBaseSpot


class InflationDifferential:
    def __init__(self, dates_index):
        self.dates_index = dates_index

    def inflation_release_computations(self):

        weo_dates = []
        inflation_release = pd.DataFrame()
        flag = False

        for date_index in self.dates_index:
            counter = 0
            date_publication = pd.to_datetime(list(dates_imf_publishing)[0], format='%d-%m-%Y')
            date = pd.to_datetime(date_index)
            if date < pd.to_datetime('19-04-2006', format='%d-%m-%Y'):
                weo_date = "Latest"
            else:
                while date > date_publication:
                    counter += 1
                    if counter >= len(dates_imf_publishing):
                        # Reach the end of the dates publishing dates
                        flag = True
                        break
                    date_publication = pd.to_datetime(list(dates_imf_publishing)[counter], format='%d-%m-%Y')
                else:
                    if date == date_publication:
                        weo_date = list(dates_imf_publishing)[counter]
                        weo_date = dates_imf_publishing[weo_date]
                    else:
                        weo_date = list(dates_imf_publishing)[counter - 1]
                        weo_date = dates_imf_publishing[weo_date]

            if flag:
                weo_date = list(dates_imf_publishing)[-1]
                weo_date = dates_imf_publishing[weo_date]
                flag = False

            weo_dates.append(weo_date)

        inflation_release[CurrencySpot.Inflation_Release.name] = weo_dates
        inflation_release = inflation_release.set_index(self.dates_index)

        # We have to shift by one each year because for each current date,
        # we have to take the previous year to compute the inflation differential
        years_zero_inflation = pd.DataFrame(inflation_release[CurrencySpot.Inflation_Release.name].index.year,
                                            columns=['Years']).shift(1).set_index(self.dates_index).iloc[1:]
        years_zero_inflation = years_zero_inflation.astype('int64')

        # We have to shift by one each month because for each current date,
        # we have to take the previous month to compute the inflation differential
        months_inflation = pd.DataFrame(inflation_release[CurrencySpot.Inflation_Release.name].index.month,
                                        columns=['Months']).shift(1).set_index(self.dates_index).iloc[1:]
        months_inflation = months_inflation.astype('int64')

        inflation_release = inflation_release.set_index(self.dates_index).shift(1).iloc[1:]

        return inflation_release, years_zero_inflation, months_inflation

    @staticmethod
    def inflation_differential_download(inflation_release):
        # Grab the data from the IMF website according to the imf publishing date
        inflation_release = inflation_release[CurrencySpot.Inflation_Release.name].drop_duplicates().iloc[1:].tolist()
        # Get files from data_imf directory
        csv_files = os.listdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data_etl", "data_imf")))
        # Get through each csv files to know if you need to download data
        print(inflation_release)
        for inflation in inflation_release:
            csv_file = 'data_imf_WEO{}all.csv'.format(inflation)
            # If there is any file in the data_imf folder
            if len(csv_files) == 0:
                for date in dates_imf_publishing.keys():
                    date_tmp = pd.to_datetime(date, format='%d-%m-%Y')
                    print(date_tmp)
                    # Inflation end of period consumer prices not available on IMF website for 2006 and 2007
                    if date_tmp.year == 2006 or date_tmp.year == 2007:
                        continue
                    # Download the data according to the publishing date
                    scrape_imf_data(date_imf=date)
            else:
                if csv_file not in csv_files:
                    # Get the date publishing to download the data
                    months = {'Apr': 0o4, 'Oct': 10}
                    month = months[inflation[:3]]
                    year = inflation[3:]
                    for date in dates_imf_publishing.keys():
                        if month and year in date:
                            # Download the data according to the publishing date
                            scrape_imf_data(date_imf=date)
                else:
                    print('OK ', csv_file)

    @staticmethod
    def inflation_differential_imf_processing(inflation):

        # Set the name of the csv file
        csv_file = 'data_imf_WEO{}all.csv'.format(inflation)

        # Read the data rom the inflation csv files
        inflation_values = pd.read_csv(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data_etl", "data_imf", csv_file)))

        countries_currencies = {'Brazil': 'BRLUSD Curncy', 'Argentina': 'ARSUSD Curncy',
                                'Mexico': 'MXNUSD Curncy', 'Colombia': 'COPUSD Curncy',
                                'Chile': 'CLPUSD Curncy', 'Peru': 'PENUSD Curncy',
                                'Turkey': 'TRYUSD Curncy', 'Russia': 'RUBUSD Curncy',
                                'Hungary': 'HUFUSD Curncy', 'Poland': 'PLNUSD Curncy',
                                'Czech Republic': 'CZKUSD Curncy', 'South Africa': 'ZARUSD Curncy',
                                'China': 'CNYUSD Curncy', 'Korea': 'KRWUSD Curncy',
                                'Malaysia': 'MYRUSD Curncy', 'Indonesia': 'IDRUSD Curncy',
                                'India': 'INRUSD Curncy', 'Philippines': 'PHPUSD Curncy',
                                'Taiwan Province of China': 'TWDUSD Curncy', 'Thailand': 'THBUSD Curncy',
                                'United Kingdom': 'GBP_Base', 'United States': 'USD_Base'
                                }

        inflation_data = pd.DataFrame(list(countries_currencies.items()), columns=['Country', 'Currency'])
        inflation_data_sorted = inflation_data.sort_values(by='Country', ascending=True)

        inflation_values = inflation_values[inflation_values['Country'].isin(list(countries_currencies.keys()))]
        inflation_values_sorted = inflation_values.sort_values(by='Country', ascending=True)
        inflation_data_merged = pd.merge(inflation_data_sorted, inflation_values_sorted)

        return inflation_data_merged

    @staticmethod
    def inflation_differential_bloomberg_processing():

        # Processing bloomberg data
        inflation_values = pd.read_csv(os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "data_etl", "bloomberg_data", "bbg_data.csv")))

        # Remove the first two rows
        inflation_values = inflation_values.iloc[2:]

        # Set the dates to timestamp
        inflation_values_index = inflation_values.iloc[:, 0].apply(lambda x: int(str(x).split('.')[0]))

        # inflation_values = inflation_values.set_index(inflation_values_index)
        inflation_values = inflation_values.iloc[:, 1:]
        inflation_values = inflation_values.set_index(inflation_values_index)

        # Delete unused columns
        inflation_values.drop(columns=['RON', 'ILS', 'EGP', 'NGN'])

        # Rename the columns correctly
        names_currencies = {'BRL': 'BRLUSD Curncy', 'PEN': 'PENUSD Curncy', 'ARS': 'ARSUSD Curncy',
                            'MXN': 'MXNUSD Curncy', 'COP': 'COPUSD Curncy', 'CLP': 'CLPUSD Curncy',
                            'TRY': 'TRYUSD Curncy', 'RUB': 'RUBUSD Curncy', 'ILS': 'ILSUSD Curncy',
                            'CZK': 'CZKUSD Curncy', 'RON': 'RONUSD Curncy', 'HUF': 'HUFUSD Curncy',
                            'PLN': 'PLNUSD Curncy', 'EGP': 'EGPUSD Curncy', 'ZAR': 'ZARUSD Curncy',
                            'NGN': 'NGNUSD Curncy', 'CNY': 'CNYUSD Curncy', 'KRW': 'KRWUSD Curncy',
                            'MYR': 'MYRUSD Curncy', 'IDR': 'IDRUSD Curncy', 'INR': 'INRUSD Curncy',
                            'PHP': 'PHPUSD Curncy', 'TWD': 'TWDUSD Curncy', 'THB': 'THBUSD Curncy',
                            'EUR': 'EUR', 'GBP': 'GBP', 'USD': 'USD'}

        inflation_values = inflation_values.rename(columns=names_currencies)

        return inflation_values

    def inflation_differential_computations(self):

        inflation_bloomberg_values = self.inflation_differential_bloomberg_processing()

        inflation_release, years_zero_inflation, months_inflation = self.inflation_release_computations()

        # Grab the inflation differential data if needed
        self.inflation_differential_download(inflation_release=inflation_release)

        years_one_inflation = years_zero_inflation.apply(lambda y: y + 1)
        years_zero_inflation = years_zero_inflation['Years'].tolist()
        years_one_inflation = years_one_inflation['Years'].tolist()

        months_inflation = months_inflation['Months'].tolist()

        inflation_release_values = inflation_release[CurrencySpot.Inflation_Release.name].tolist()

        # Compute the multipliers (12 - m)/12 and m/12
        multiplier_one = pd.Series(months_inflation).apply(lambda m: (12-m)/12)
        multiplier_two = pd.Series(months_inflation).apply(lambda m: m/12)

        inflation_differential = pd.DataFrame()

        for currency in constants.CURRENCIES_SPOT:
            inflation_year_zero_value = []
            inflation_year_one_value = []
            inflation_year_zero_value_base = []
            inflation_year_one_value_base = []

            flag_imf = ''
            print(currency)
            for inflation, year_zero, year_one in zip(inflation_release_values, years_zero_inflation, years_one_inflation):

                if inflation != 'Latest':

                    # Be sure the csv file is read only one time per inflation
                    if flag_imf != inflation:
                        inflation_data_merged = self.inflation_differential_imf_processing(inflation=inflation)

                    index_currency = inflation_data_merged[inflation_data_merged.Currency.str.contains(currency)].index[0]

                    # Select the base currency (USD or EUR) depending on the currency
                    if currency in constants.CURRENCIES_USD:
                        index_currency_base = \
                            inflation_data_merged[inflation_data_merged.Currency.str.contains(CurrencyBaseSpot.USD_Base.name)].index[0]
                    else:
                        index_currency_base = \
                            inflation_data_merged[inflation_data_merged.Currency.str.contains(CurrencyBaseSpot.EUR_Base.name)].index[0]

                    # Look for the value of the inflation at year0 and then append to the list inflation_year_zero_value
                    inflation_year_zero_value.append(inflation_data_merged.loc[index_currency, str(year_zero)])
                    # Look for the value of the inflation at year1 and then append to the list inflation_year_one_value
                    inflation_year_one_value.append(inflation_data_merged.loc[index_currency, str(year_one)])

                    # Look for the value of the base currency at year0 and then append to the list inflation_
                    # year_zero_value
                    inflation_year_zero_value_base.append(inflation_data_merged.loc[index_currency_base, str(year_zero)])
                    # Look for the value of the base currency at year1 and then append to the list inflation_
                    # year_zero_value
                    inflation_year_one_value_base.append(inflation_data_merged.loc[index_currency_base, str(year_one)])

                else:
                    # Select the base currency (USD or EUR) depending on the currency
                    if currency in constants.CURRENCIES_USD:
                        base_currency = CurrencyBaseSpot.USD.name
                    else:
                        base_currency = CurrencyBaseSpot.EUR.name

                    # Look for the value of the inflation at year0 and then append to the list inflation_year_zero_value
                    inflation_year_zero_value.append(float(inflation_bloomberg_values.loc[year_zero, currency]))
                    # Look for the value of the inflation at year1 and then append to the list inflation_year_one_value
                    inflation_year_one_value.append(float(inflation_bloomberg_values.loc[year_one, currency]))
                    # Look for the value of the base currency at year0 and then append to the list inflation_
                    # year_zero_value
                    inflation_year_zero_value_base.append(float(inflation_bloomberg_values.loc[year_zero, base_currency]))
                    # Look for the value of the base currency at year1 and then append to the list inflation_
                    # year_zero_value
                    inflation_year_one_value_base.append(float(inflation_bloomberg_values.loc[year_one, base_currency]))

                flag_imf = inflation

            # Store results in dataFrames
            inflation_year_zero_values = multiplier_one.mul(pd.Series(inflation_year_zero_value).astype(np.float64))
            inflation_year_one_values = multiplier_two.mul(pd.Series(inflation_year_one_value).astype(np.float64))
            inflation_year_zero_values_base = multiplier_one.mul(pd.Series(inflation_year_zero_value_base).astype(np.float64))
            inflation_year_one_values_base = multiplier_two.mul(pd.Series(inflation_year_one_value_base).astype(np.float64))

            # Compute the inflation differential
            inflation_one = inflation_year_zero_values.add(inflation_year_one_values).apply(lambda x: x/100)
            inflation_two = inflation_year_zero_values_base.add(inflation_year_one_values_base).apply(lambda x: x/100)

            inflation_three = inflation_one.sub(inflation_two).apply(lambda x: x * 100)

            inflation_differential[CurrencySpot.Inflation_Differential.name + currency] = inflation_three.tolist()

        # Set the index with dates
        new_index = np.delete(self.dates_index, 0)
        inflation_differential = inflation_differential.set_index(new_index)

        return inflation_differential
