"""
Created on 12/05/2020
@author: AJ89720
"""

from models.effect.data_processing_effect import DataProcessingEffect
from models.effect.inflation_imf_publishing_dates import dates_imf_publishing

from assetallocation_arp.data_etl.imf_data_download import scrape_imf_data

from pandas import DataFrame

import common_libraries.constants as constants
import pandas as pd
import numpy as np
import os


class CurrencyComputations(DataProcessingEffect):

    def __init__(self):
        super().__init__()

        self.carry_currencies = pd.DataFrame()
        self.trend_currencies = pd.DataFrame()
        self.spot_ex_costs = pd.DataFrame()
        self.spot_incl_costs = pd.DataFrame()
        self.return_ex_costs = pd.DataFrame()
        self.return_incl_costs = pd.DataFrame()
        self.combo_currencies = pd.DataFrame()
        self.inflation_release = pd.DataFrame()
        self.inflation_differential = pd.DataFrame()

        self.bid_ask_spread = 0
        self.start_date_computations = ''

    @property
    def bid_ask(self):
        return self.bid_ask_spread

    @bid_ask.setter
    def bid_ask(self, value):
        self.bid_ask_spread = value

    @property
    def start_date_calculations(self):
        return self.start_date_computations

    @start_date_calculations.setter
    def start_date_calculations(self, value):
        self.start_date_computations = value

        global dates_index

        dates_index = self.data_currencies_usd[self.start_date_computations:].index.values

    def inflation_release_computations(self): #todo create another file to host the fct

        dates_index = self.data_currencies_usd.loc[self.start_date_computations:].index.values
        weo_dates = []
        flag = False

        for date_index in dates_index:
            counter = 0
            date_publication = pd.to_datetime(list(dates_imf_publishing)[0], format='%d-%m-%Y')
            date = pd.to_datetime(date_index)
            if date < pd.to_datetime('26-04-2006', format='%d-%m-%Y'):
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
                    weo_date = list(dates_imf_publishing)[counter - 1]
                    weo_date = dates_imf_publishing[weo_date]

            if flag:
                weo_date = list(dates_imf_publishing)[-1]
                weo_date = dates_imf_publishing[weo_date]
                flag = False

            weo_dates.append(weo_date)

        self.inflation_release["Inflation Release"] = weo_dates
        # Set the index and shift the data by one
        self.inflation_release = self.inflation_release.set_index(dates_index).shift(1)
        # Replace the nan by Latest because we know it is the only nan in the Series
        self.inflation_release = self.inflation_release.fillna('Latest')

    def inflation_differential_download(self):
        # Grab the data from the IMF website according to the imf publishing date
        inflation_release = self.inflation_release['Inflation Release'].drop_duplicates().iloc[1:].tolist()
        # Get files from data_imf directory
        csv_files = os.listdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data_etl", "data_imf")))
        # Get through each csv files to know if you need to download data
        print(inflation_release)
        for inflation in inflation_release:
            csv_file = 'data_imf_WEO{}all.csv'.format(inflation)
            # If there is any file in the data_imf folder todo CHANGE IT
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

    def inflation_differential_computations(self):
        # todo create a class for inflation imf
        # todo ask for eur and usd currency
        # Grab the inflation differential data if needed
        self.inflation_differential_download()
        inflations_release_values = self.inflation_release['Inflation Release'].tolist()
        years_zero = self.inflation_release['Inflation Release'].index.year.tolist()
        years_one = [year+1 for year in years_zero]
        months = self.inflation_release['Inflation Release'].index.month.tolist()

        # Compute the multiplicators (12 - m)/12 and m/12
        multiplicator_one = pd.DataFrame(months).apply(lambda x: (12-x)/12)
        multiplicator_two = pd.DataFrame(months).apply(lambda x: x/12)

        for currency in constants.CURRENCIES_SPOT:
            inflation_year_zero_value = []
            inflation_year_one_value = []
            inflation_year_zero_value_base = []
            inflation_year_one_value_base = []

            for inflation, year_zero, year_one in zip(inflations_release_values, years_zero, years_one):

                if inflation != 'Latest':
                    # Set the name of the csv file
                    csv_file = 'data_imf_WEO{}all.csv'.format(inflation)
                    # Read the data rom the inflation csv files
                    inflation_values = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data_etl", "data_imf", csv_file)))

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
                                            'United Kingdom': 'GBP Curncy', 'United States': 'USD Curncy'
                                            }

                    inflation_data = DataFrame(list(countries_currencies.items()), columns=['Country', 'Currency'])
                    inflation_data_sorted = inflation_data.sort_values(by='Country', ascending=True)

                    inflation_values = inflation_values[inflation_values['Country'].isin(list(countries_currencies.keys()))]
                    inflation_values_sorted = inflation_values.sort_values(by='Country', ascending=True)
                    inflation_data_merged = pd.merge(inflation_data_sorted, inflation_values_sorted)

                    index_currency = inflation_data_merged[inflation_data_merged.Currency.str.contains(currency)].index[0]

                    if currency in self.data_currencies_usd:
                        index_currency_base = \
                            inflation_data_merged[inflation_data_merged.Currency.str.contains('USD Curncy')].index[0]
                    else:
                        index_currency_base = \
                        inflation_data_merged[inflation_data_merged.Currency.str.contains('EUR Curncy')].index[0]

                    inflation_year_zero_value.append(inflation_data_merged.loc[index_currency, str(year_zero)])
                    inflation_year_one_value.append(inflation_data_merged.loc[index_currency, str(year_one)])

                    inflation_year_zero_value_base.append(inflation_data_merged.loc[index_currency_base, str(year_zero)])
                    inflation_year_one_value_base.append(inflation_data_merged.loc[index_currency_base, str(year_one)])

                    # Store results in dataFrames
                    inflation_year_zero_values = multiplicator_one.mul(pd.DataFrame(inflation_year_zero_value))
                    inflation_year_one_values = multiplicator_one.mul(pd.DataFrame(inflation_year_one_value))
                    inflation_year_zero_values_base = multiplicator_two.mul(pd.DataFrame(inflation_year_zero_value_base))
                    inflation_year_one_values_base = multiplicator_two.mul(pd.DataFrame(inflation_year_one_value_base))

                    # Compute the inflation differential
                    inflation_one = inflation_year_zero_values.add(inflation_year_zero_values_base).apply(lambda x: x/100)
                    inflation_two = inflation_year_one_values.add(inflation_year_one_values_base).apply(lambda x: x/100)
                    inflation_three = inflation_one.sub(inflation_two)
                    self.inflation_differential['Inflation_Differential_' + currency] = inflation_three

                    print()

    def carry_computations(self, carry_type):

        if carry_type.lower() == 'real':

            for currency_spot, currency_implied, currency_carry in zip(constants.CURRENCIES_SPOT, constants.CURRENCIES_IMPLIED, constants.CURRENCIES_CARRY):

                tmp_start_date_computations = self.start_date_computations

                rows = self.data_currencies_usd[tmp_start_date_computations:].shape[0]

                carry = []

                if currency_spot in self.data_currencies_usd.columns:
                    data_all_currencies_spot = self.data_currencies_usd.loc[:, currency_spot].tolist()
                    data_all_currencies_carry = self.data_currencies_usd.loc[:, currency_carry].tolist()
                    data_all_currencies_implied = self.data_currencies_usd.loc[:, currency_implied].tolist()
                    data_all_currencies_index = self.data_currencies_usd.loc[:, 'US0003M Index'].tolist()
                else:
                    data_all_currencies_spot = self.data_currencies_eur.loc[:, currency_spot].tolist()
                    data_all_currencies_carry = self.data_currencies_eur.loc[:, currency_carry].tolist()
                    data_all_currencies_implied = self.data_currencies_eur.loc[:, currency_implied].tolist()
                    data_all_currencies_index = self.data_currencies_eur.loc[:, 'EUR003M Curncy'].tolist()

                for values in range(rows):

                    start_date_index = self.data_currencies_usd.index.get_loc(tmp_start_date_computations)

                    previous_start_date = self.data_currencies_usd.index[start_date_index - 4]
                    previous_four_start_date_index = self.data_currencies_usd.index.get_loc(previous_start_date)

                    average_implied = np.mean(data_all_currencies_implied[previous_four_start_date_index:start_date_index])
                    average_index = np.mean(data_all_currencies_index[previous_four_start_date_index:start_date_index])

                    carry_tmp = ((average_implied - average_index) / 100) - 0.028 #inflation diff

                    if not np.isnan(carry_tmp):
                        carry.append(carry_tmp)
                    else:
                        start_date_index = self.data_currencies_usd.index.get_loc(tmp_start_date_computations)

                        previous_start_date = self.data_currencies_usd.index[start_date_index - 1]
                        previous_start_date_index = self.data_currencies_usd.index.get_loc(previous_start_date)

                        previous_eleven_start_date = self.data_currencies_usd.index[start_date_index - 11]
                        previous_eleven_start_date_index = self.data_currencies_usd.index.get_loc(previous_eleven_start_date)

                        numerator = data_all_currencies_carry[previous_start_date_index] / data_all_currencies_carry[previous_eleven_start_date_index]
                        denominator = data_all_currencies_spot[previous_start_date_index] / data_all_currencies_spot[previous_eleven_start_date_index]

                        carry.append((((numerator / denominator) ** (52/10))-1))

                    try:
                        tmp_start_date_computations = self.data_currencies_usd.index[start_date_index + 1]
                    except IndexError:
                        tmp_start_date_computations = self.data_currencies_usd.index[start_date_index]

                self.carry_currencies['Carry ' + currency_spot] = carry

        self.carry_currencies = self.carry_currencies.set_index(dates_index)

    def trend_computations(self, trend_ind, short_term, long_term):

        if trend_ind.lower() == 'total return':
            currencies = constants.CURRENCIES_CARRY
        else:
            currencies = constants.CURRENCIES_SPOT

        # loop through each date
        for currency, currency_name_col in zip(currencies, constants.CURRENCIES_SPOT):
            if currency in self.data_currencies_usd.columns:
                trend_short_tmp = self.data_currencies_usd.loc[:, currency].rolling(short_term).mean()
                trend_long_tmp = self.data_currencies_usd.loc[:, currency].rolling(long_term).mean()
            else:
                trend_short_tmp = self.data_currencies_eur.loc[:, currency].rolling(short_term).mean()
                trend_long_tmp = self.data_currencies_eur.loc[:, currency].rolling(long_term).mean()

            self.trend_currencies['Trend ' + currency_name_col] = ((trend_short_tmp / trend_long_tmp)-1)*100

        # take the previous date compared to self.date_computations because there is a shift of 1 because of rolling
        start_date_loc = self.data_currencies_usd.index.get_loc(self.start_date_computations)
        previous_start_date = self.data_currencies_usd.index[start_date_loc - 1]

        self.trend_currencies = self.trend_currencies[previous_start_date:].iloc[:-1]
        self.trend_currencies = self.trend_currencies.set_index(dates_index)

    def combo_computations(self, cut_off, incl_shorts, cut_off_s, threshold_for_closing):

        tmp_start_date_computations = self.start_date_computations
        rows = self.data_currencies_usd[tmp_start_date_computations:].shape[0]

        for currency_spot in constants.CURRENCIES_SPOT:
            combo = [0] # set the combo to zero as first value
            trend = self.trend_currencies.loc[tmp_start_date_computations:, 'Trend ' + currency_spot].tolist()
            carry = self.carry_currencies.loc[tmp_start_date_computations:, 'Carry ' + currency_spot].tolist()

            for value in range(rows):
                if combo[-1] == 0:
                    if carry[value] >= cut_off and trend[value] >= 0:
                        combo.append(1)
                    else:
                        if incl_shorts.lower() == 'yes' and carry[value] <= cut_off_s and trend[value] <= 0:
                            combo.append(-1)
                        else:
                            combo.append(0)
                else:
                    if carry[value] >= (cut_off - threshold_for_closing) and trend[value] >= 0:
                        combo.append(1)
                    else:
                        if incl_shorts.lower() == 'yes' and carry[value] <= (cut_off_s + threshold_for_closing) and trend[value] <= 0:
                            combo.append(-1)
                        else:
                            combo.append(0)

            self.combo_currencies['Combo ' + currency_spot] = combo

        self.combo_currencies = self.combo_currencies.iloc[1:]  # remove the first line as it was the initialization of the combo
        self.combo_currencies = self.combo_currencies.set_index(dates_index)

    def return_ex_costs_computations(self):

        for currency_carry, currency_spot in zip(constants.CURRENCIES_CARRY, constants.CURRENCIES_SPOT):

            first_return = [100]

            if currency_carry in self.data_currencies_usd.columns:
                return_division_tmp = (self.data_currencies_usd.loc[self.start_date_computations:, currency_carry] /
                                       self.data_currencies_usd.loc[self.start_date_computations:, currency_carry].shift(1))
            else:
                return_division_tmp = (self.data_currencies_eur.loc[self.start_date_computations:, currency_carry] /
                                       self.data_currencies_eur.loc[self.start_date_computations:, currency_carry].shift(1))

            combo_tmp = self.combo_currencies['Combo ' + currency_spot].tolist()
            combo_tmp.pop(0)
            return_division_tmp = return_division_tmp.iloc[1:]
            return_tmp = return_division_tmp.tolist()

            for values in range(len(return_tmp)):
                first_return.append(first_return[values] * return_tmp[values] ** combo_tmp[values])

            self.return_ex_costs['Return Ex Costs ' + currency_spot] = first_return

        self.return_ex_costs = self.return_ex_costs.set_index(dates_index)

    def return_incl_costs_computations(self):

        returns_division_tmp = self.return_ex_costs / self.return_ex_costs.shift(1) * (1-self.bid_ask_spread/20000)

        returns_division_tmp = returns_division_tmp.iloc[1:]

        currency_ex_costs = returns_division_tmp.columns.values.tolist()
        combo_names = self.combo_currencies.columns.tolist()

        for name, combo_name in zip(currency_ex_costs, combo_names):
            first_return = [100]
            return_tmp = returns_division_tmp[name].tolist()
            combo_tmp = self.combo_currencies[combo_name].tolist()
            combo_tmp.pop(0)
            for values in range(len(return_tmp)):
                first_return.append(first_return[values] * return_tmp[values] ** combo_tmp[values])

            self.return_incl_costs[name.replace('Return Ex Costs', 'Return Incl Costs')] = first_return

        self.return_incl_costs = self.return_incl_costs.set_index(dates_index)

    def spot_ex_costs_computations(self):

        # loop to get through each currency
        for currency in constants.CURRENCIES_SPOT:
            # Reset the Spot list for the next currency
            spot = [100]  # the Spot is set 100
            if currency in self.data_currencies_usd.columns:
                spot_division_tmp = (self.data_currencies_usd.loc[self.start_date_computations:, currency] /
                                     self.data_currencies_usd.loc[self.start_date_computations:, currency].shift(1))
            else:
                spot_division_tmp = (self.data_currencies_eur.loc[self.start_date_computations:, currency] /
                                     self.data_currencies_eur.loc[self.start_date_computations:, currency].shift(1))

            combo_tmp = self.combo_currencies.loc[self.start_date_computations:, 'Combo ' + currency].tolist()
            # Remove the first line to be equal with the spot_tmp
            combo_tmp.pop(0)
            # Remove the first nan due to the shift(1)
            spot_division_tmp = spot_division_tmp.iloc[1:]
            # Transform the spot_division_tmp into a list
            spot_tmp = spot_division_tmp.values.tolist()
            # Compute with the previous Spot
            for value in range(len(spot_tmp)):
                spot.append(spot[value] * spot_tmp[value] ** combo_tmp[value])

            # Store all the spot for each currency
            self.spot_ex_costs['Spot Ex Costs ' + currency] = spot

        # Set the dates to the index of self.spot_ex_costs
        self.spot_ex_costs = self.spot_ex_costs.set_index(dates_index)

    def spot_incl_computations(self):

        combo = abs(self.combo_currencies-self.combo_currencies.shift(1))

        spot_division_tmp = self.spot_ex_costs / self.spot_ex_costs.shift(1)*(1-self.bid_ask_spread/20000)

        # Remove the first nan due to the shift(1)
        spot_division_tmp = spot_division_tmp.iloc[1:]
        combo = combo.iloc[1:]

        currency_ex_costs = spot_division_tmp.columns.values.tolist()
        combo_names = combo.columns.tolist()

        # loop through each currency in spot_division_tmp
        for name, combo_name in zip(currency_ex_costs, combo_names):
            spot = [100]  # the Spot is set 100
            spot_tmp = spot_division_tmp[name].tolist()
            combo_tmp = combo[combo_name].tolist()
            # Compute with the previous Spot
            for values in range(len(spot_tmp)):
                spot.append(spot[values] * spot_tmp[values] ** combo_tmp[values])

            self.spot_incl_costs[name.replace('Spot Ex Costs', 'Spot Incl Costs')] = spot

        # set the dates to the index of self.spot_incl_costs
        self.spot_incl_costs = self.spot_incl_costs.set_index(dates_index)
