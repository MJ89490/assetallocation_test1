# from .times import format_data_and_calc
# from assetallocation_arp.arp_strategies import write_output_to_excel

"""
Created on Fri Nov  15 17:27:51 2019
CURP
@author: JL89005
"""
import pandas as pd
import numpy as np
import xlwings as xw


# my formatting is that variables are camel case, functions use _





# Curp Carve out file \\inv\LGIM\FrontOffice\Bonds\Asset Allocation\Research&Strategy\ARP\CURP Carve Out.xlsm



def run_curp(curp_inputs, asset_inputs, all_data ):
    # this will be where the main code is run

    # get data test
    currencyCrosses = create_crosses_two(asset_inputs['Currency'])
    pppData = filter_data(all_data, asset_inputs['PPP Tickers'])
    irData = filter_data(all_data, asset_inputs['IR Tickers'])
    spotSparseData = filter_data(all_data, asset_inputs['Spot Tickers'])
    carrySparseData = filter_data(all_data, asset_inputs['Carry Tickers'])

    # process data

    asset_inputs.set_index('Currency')

    # create all FX crosses from the ones given
    # this needs to be smart in that it takes the first part of the cross as one matrix, the second part as the other and does A/B

    mtxSpot=pd.DataFrame({currencyCrosses:[]})
    for (columnName, columnData) in mtxSpot.iteritems():
        # get base fx
        baseFx = columnName[0:3]
        priceFX = columnName[2:5]
        # need to find the ticker to use for the base fx
        baseTicker = asset_inputs.loc[asset_inputs['Currency'] == baseFx, 'Spot Tickers'].iloc[0]
        priceTicker = asset_inputs.loc[asset_inputs['Currency'] == priceFX, 'Spot Ticker'].iloc[0]
        # Get the data for each of these columns, then divide or subtract the two and put it back into the DF



    firstCurrency = [frst(x) for x in currencyCrosses]
    secondCurrency = [scnd(x) for x in currencyCrosses]
    matrixSpotA = pd.DataFrame({firstCurrency})
    matrixSpotB = pd.DataFrame({secondCurrency})
    matrixCarryA = pd.DataFrame({firstCurrency})
    matrixCarryB = pd.DataFrame({secondCurrency})

    for currency in asset_inputs['Currency']:
        matrixSpotA[firstCurrency == currency] = spotSparseData[(currency + 'USD Curncy')]
        matrixSpotB[secondCurrency == currency] = spotSparseData[(currency + 'USD Curncy')]
        matrixCarryA[firstCurrency == currency] = carrySparseData[(currency + 'USDCR Curncy')]
        matrixCarryB[secondCurrency == currency] = carrySparseData[(currency + 'USDCR Curncy')]
    spotData = matrixSpotA/matrixSpotB #this wont work
    carryData = matrixCarryA/matrixCarryB #this wont work

    """""""""""
    For this section i need to calculate IR differentials
    To do this:
    Build 2 empty DF
    """""""""""

    pass

def create_crosses_two(currencyList):
    # create data frame
    output = pd.DataFrame(columns=['cross'])
    for i in list(range(1,(len(currencyList.index)))):
        for j in list(range(i+1,len(currencyList.index)+1)):
            output = output.append({'cross': currencyList[i]+currencyList[j]}, ignore_index=True)
    print(len(currencyList.index)+1)
    print(currencyList[(len(currencyList.index) + 1)])
    x = output
    return x
# output = output.append({'cross' : currencyList[i]currencyList[j]}, ignore_index=True)

def frst(inpt):
    return inpt[0:3]

def scnd(inpt):
    return inpt[3:6]

def filter_data(all_data, tickers):
    # pass in the entire load of data and only take the columns needed
    output = pd.DataFrame(all_data,columns = tickers)
    return output


if __name__ == "__main__":
    # test inputs

    curp_inputs, asset_inputs, all_data = gd.extract_inputs_and_mat_data(model_type, mat_file, input_file)
