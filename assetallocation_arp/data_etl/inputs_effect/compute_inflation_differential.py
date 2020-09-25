
"""
    Class to make inflation differential calculations
"""

import pandas as pd
import numpy as np
import os
import json
from configparser import ConfigParser

from assetallocation_arp.common_libraries.names_columns_calculations import CurrencySpot
from assetallocation_arp.common_libraries.names_currencies_base_spot import CurrencyBaseSpot
from data_etl.outputs_effect.write_logs_computations_effect import write_logs_effect


class ComputeInflationDifferential:
    def __init__(self, dates_index):
        self.dates_index = dates_index

    def compute_inflation_release(self, realtime_inflation_forecast):
        """
        Function computing the inflation release depending on the publications IMF dates
        :return: separate dataFrames inflation_release, years_zero_inflation, months_inflation
        """
        write_logs_effect("Computing inflation release...", "logs_inflation_release")
        weo_dates = []
        inflation_release = pd.DataFrame()
        flag = False

        # Instantiate ConfigParser
        config = ConfigParser()
        # Parse existing file
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config_effect_model', 'dates_effect.ini'))
        config.read(path)
        # Read values from the dates_effect.ini file
        latest_date = config.get('latest_date_inflation_differential', 'latest_date_inflation')
        dates_imf_publishing = json.loads(config.get('dates_imf_publishing', 'dates_imf_publication'))

        for date_index in self.dates_index:

            if realtime_inflation_forecast.lower() != 'yes':
                weo_date = "Latest"
                # weo_dates.append(weo_date)
            else:
                counter = 0
                date_publication = pd.to_datetime(list(dates_imf_publishing)[0], format='%d-%m-%Y')
                date_tmp = date_index
                if date_tmp < pd.to_datetime(latest_date, format='%d-%m-%Y'):
                    weo_date = "Latest"
                else:
                    while date_tmp > date_publication:
                        counter += 1
                        if counter >= len(dates_imf_publishing):
                            # Reach the end of the dates publishing dates
                            flag = True
                            break
                        date_publication = pd.to_datetime(list(dates_imf_publishing)[counter], format='%d-%m-%Y')
                    else:
                        if date_tmp == date_publication:
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
    def process_inflation_differential_imf(inflation):
        """
        Function processing the inflation differential data from csv files
        :param inflation: inflation date (eg: Apr2020)
        :return: a dataFrame inflation_data_merged with inflation data inside for usd and eur countries
        """
        # todo modify later because data will be stored in a Db

        # Set the name of the csv file for country and group data
        data_country = 'data_imf_WEO{}all.csv'.format(inflation)
        data_group_country = 'data_imf_eur_WEO{}alla.csv'.format(inflation)

        # Read the data rom the inflation csv files
        inflation_values = pd.read_csv(
            os.path.abspath(os.path.join(os.path.dirname(__file__),  '..', '..', '..', 'data_effect', 'data', 'data_imf', data_country)))
        inflation_eur_values = pd.read_csv(
            os.path.abspath(os.path.join(os.path.dirname(__file__),  '..', '..', '..', 'data_effect', 'data', 'data_imf', data_group_country)))

        countries_currencies = {'Brazil': 'BRLUSD Curncy', 'Argentina': 'ARSUSD Curncy',
                                'Mexico': 'MXNUSD Curncy', 'Colombia': 'COPUSD Curncy',
                                'Chile': 'CLPUSD Curncy', 'Peru': 'PENUSD Curncy',
                                'Turkey': 'TRYUSD Curncy', 'Russia': 'RUBUSD Curncy',
                                'Hungary': 'HUFEUR Curncy', 'Poland': 'PLNEUR Curncy',
                                'Czech Republic': 'CZKEUR Curncy', 'South Africa': 'ZARUSD Curncy',
                                'China': 'CNYUSD Curncy', 'Korea': 'KRWUSD Curncy',
                                'Malaysia': 'MYRUSD Curncy', 'Indonesia': 'IDRUSD Curncy',
                                'India': 'INRUSD Curncy', 'Philippines': 'PHPUSD Curncy',
                                'Taiwan Province of China': 'TWDUSD Curncy', 'Thailand': 'THBUSD Curncy',
                                'United Kingdom': 'GBP_Base', 'United States': 'USD_Base'
                                }

        country_currency_eur = {'Euro area': 'EUR_Base'}

        inflation_eur_values.rename(columns={'Country Group Name': 'Country'}, inplace=True)

        inflation_data_eur = pd.DataFrame(list(country_currency_eur.items()), columns=['Country', 'Currency'])

        inflation_data = pd.DataFrame(list(countries_currencies.items()), columns=['Country', 'Currency'])
        inflation_data_sorted = inflation_data.sort_values(by='Country', ascending=True)

        inflation_eur_values = inflation_eur_values[inflation_eur_values['Country'].isin(list(country_currency_eur.keys()))]
        inflation_eur_data_merged = pd.merge(inflation_data_eur, inflation_eur_values)

        inflation_values = inflation_values[inflation_values['Country'].isin(list(countries_currencies.keys()))]
        inflation_values_sorted = inflation_values.sort_values(by='Country', ascending=True)
        inflation_data_merged = pd.merge(inflation_data_sorted, inflation_values_sorted)

        # Add Euro area data to inflation_data_merged
        inflation_data_merged = inflation_data_merged.append(inflation_eur_data_merged, ignore_index=True)

        return inflation_data_merged

    @staticmethod
    def process_inflation_differential_bloomberg():
        """
        Function processing the Bloomberg inflation differential data fom csv files
        :return: a dataFrame inflation_bloomberg_values with inflation data inside for usd and eur countries
        """
        #TODO ADD SELF POUR INF
        # Processing Bloomberg data
        inflation_values = pd.read_csv(os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data_effect', 'data', 'bloomberg_data', 'bbg_data.csv')))
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
                            'CZK': 'CZKEUR Curncy', 'RON': 'RONUSD Curncy', 'HUF': 'HUFEUR Curncy',
                            'PLN': 'PLNEUR Curncy', 'EGP': 'EGPUSD Curncy', 'ZAR': 'ZARUSD Curncy',
                            'NGN': 'NGNUSD Curncy', 'CNY': 'CNYUSD Curncy', 'KRW': 'KRWUSD Curncy',
                            'MYR': 'MYRUSD Curncy', 'IDR': 'IDRUSD Curncy', 'INR': 'INRUSD Curncy',
                            'PHP': 'PHPUSD Curncy', 'TWD': 'TWDUSD Curncy', 'THB': 'THBUSD Curncy',
                            'EUR': 'EUR', 'GBP': 'GBP', 'USD': 'USD'}

        inflation_bloomberg_values = inflation_values.rename(columns=names_currencies)

        return inflation_bloomberg_values

    def compute_inflation_differential(self, realtime_inflation_forecast, currencies_spot, currencies_usd):
        """
        Function computing the inflation differential for usd and eur countries
        :return: a dataFrame  inflation_differential with all inflation differential data
        """
        write_logs_effect("Computing inflation differential...", "logs_inflation_differential")
        inflation_bloomberg_values = self.process_inflation_differential_bloomberg()

        inflation_release, years_zero_inflation, months_inflation = self.compute_inflation_release(realtime_inflation_forecast)

        # Grab the latest inflation differential data
        # scrape_imf_data()

        years_one_inflation = years_zero_inflation.apply(lambda y: y + 1)
        years_zero_inflation = years_zero_inflation['Years'].tolist()
        years_one_inflation = years_one_inflation['Years'].tolist()

        months_inflation = months_inflation['Months'].tolist()

        inflation_release_values = inflation_release[CurrencySpot.Inflation_Release.name].tolist()

        # Compute the multipliers (12 - m)/12 and m/12
        multiplier_one = pd.Series(months_inflation).apply(lambda m: (12-m)/12)
        multiplier_two = pd.Series(months_inflation).apply(lambda m: m/12)

        inflation_differential = pd.DataFrame()

        counter = 8

        for currency in currencies_spot:
            inflation_year_zero_value = []
            inflation_year_one_value = []
            inflation_year_zero_value_base = []
            inflation_year_one_value_base = []

            flag_imf = ''
            print(currency)
            write_logs_effect(currency, counter, True)

            for inflation, year_zero, year_one in zip(inflation_release_values, years_zero_inflation, years_one_inflation):

                if inflation != 'Latest':

                    # Be sure the csv file is read only one time per inflation
                    if flag_imf != inflation:
                        inflation_data_merged = self.process_inflation_differential_imf(inflation=inflation)

                    #TODO improve later with DB to speed up the calculation of the inflation ; maybe put all the data in one DF?
                    index_currency = inflation_data_merged[inflation_data_merged.Currency.str.contains(currency)].index[0]

                    # Select the base currency (USD or EUR) depending on the currency
                    if currency in currencies_usd:
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
                    # year_one_value
                    inflation_year_one_value_base.append(inflation_data_merged.loc[index_currency_base, str(year_one)])

                else:
                    # Select the base currency (USD or EUR) depending on the currency
                    if currency in currencies_usd:
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
            inflation_differential[CurrencySpot.Inflation_Differential.value + currency] = inflation_three.tolist()

            counter += 1

        # Set the index with dates
        new_index = np.delete(self.dates_index, 0)
        inflation_differential = inflation_differential.set_index(new_index)

        return inflation_differential
