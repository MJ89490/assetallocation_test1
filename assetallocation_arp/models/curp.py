# from .times import format_data_and_calc
# from assetallocation_arp.arp_strategies import write_output_to_excel

"""
Created on Fri Nov  15 17:27:51 2019
CURP
@author: JL89005
"""
import pandas as pd
import math
import numpy as np
import xlwings as xw


# my formatting is that variables are camel case, functions use _

# Curp Carve out file \\inv\LGIM\FrontOffice\Bonds\Asset Allocation\Research&Strategy\ARP\CURP Carve Out.xlsm
# CUMO file \\inv\LGIM\FrontOffice\Bonds\Asset Allocation\Research&Strategy\ARP\CUMO.xlsm

def run_curp(curp_inputs, asset_inputs, all_data ):
    # this will be where the main code is run
    all_data['USDUSD Curncy'] = 1
    all_data['USDUSDCR Curncy'] = 1
    # this below should be deleted when the data is made available in the mat file
    all_data['SEKUSD Curncy'] = 1
    all_data['CHFUSD Curncy'] = 1
    all_data['NOKUSD Curncy'] = 1
    all_data['CHFUSDCR Curncy'] = 1
    all_data['SEKUSDCR Curncy'] = 1
    all_data['CADUSDCR Curncy'] = 1
    all_data['NOKUSDCR Curncy'] = 1

    # create all FX crosses from the ones given
    currencyCrosses = create_crosses(asset_inputs['Currency'])
    firstCurrency = currencyCrosses.applymap(lambda x: x[0:3])
    secondCurrency = currencyCrosses.applymap(lambda x: x[3:6])

    # Spot Data
    firstCurrencySpotTicker = firstCurrency.applymap(lambda x: x +'USD Curncy')
    firstCurrencySpotTickerList = firstCurrencySpotTicker['cross'].tolist()
    secondCurrencySpotTicker = secondCurrency.applymap(lambda x: x + 'USD Curncy')
    secondCurrencySpotTickerList = secondCurrencySpotTicker['cross'].tolist()
    firstCurrencySpotData = all_data[firstCurrencySpotTickerList]
    secondCurrencySpotData = all_data[secondCurrencySpotTickerList]
    # Next line might need to change: see https://pythontic.com/pandas/dataframe-binaryoperatorfunctions/div
    firstCurrencySpotDataRatio = firstCurrencySpotData.pct_change+1
    secondCurrencySpotDataRatio = secondCurrencySpotData.pct_change+1
    SpotData = firstCurrencySpotDataRatio.div(secondCurrencySpotDataRatio)-1

    # Blank line, delete later

    # Carry Data
    firstCurrencyCarryTicker = firstCurrency.applymap(lambda x: x +'USDCR Curncy')
    firstCurrencyCarryTickerList = firstCurrencyCarryTicker['cross'].tolist()
    secondCurrencyCarryTicker = secondCurrency.applymap(lambda x: x + 'USDCR Curncy')
    secondCurrencyCarryTickerList = secondCurrencyCarryTicker['cross'].tolist()
    firstCurrencyCarryData = all_data[firstCurrencyCarryTickerList]
    secondCurrencyCarryData = all_data[secondCurrencyCarryTickerList]
    # Next line might need to change: see https://pythontic.com/pandas/dataframe-binaryoperatorfunctions/div
    firstCurrencyCarryDataRatio = firstCurrencyCarryData.pct_change+1
    secondCurrencyCarryDataRatio = secondCurrencyCarryData.pct_change + 1
    carryData = firstCurrencyCarryDataRatio.div(secondCurrencyCarryDataRatio)-1

    # PPP Data
    firstCurrencyPPPTicker = firstCurrency.applymap(lambda x:asset_inputs.loc[asset_inputs['Currency'] == x, 'PPP Tickers'].iloc[0])
    firstCurrencyPPPTickerList = firstCurrencyPPPTicker['cross'].tolist()
    secondCurrencyPPPTicker = secondCurrency.applymap(lambda x:asset_inputs.loc[asset_inputs['Currency'] == x, 'PPP Tickers'].iloc[0])
    secondCurrencyPPPTickerList = secondCurrencyPPPTicker['cross'].tolist()
    firstCurrencyPPPData = all_data[firstCurrencyPPPTickerList]
    secondCurrencyPPPData = all_data[secondCurrencyPPPTickerList]
    pppData = secondCurrencyPPPData.div(firstCurrencyPPPData)

    # IR Data
    firstCurrencyIRTicker = firstCurrency.applymap(lambda x:asset_inputs.loc[asset_inputs['Currency'] == x, 'IR Tickers'].iloc[0])
    firstCurrencyIRTickerList = firstCurrencyIRTicker['cross'].tolist()
    secondCurrencyIRTicker = secondCurrency.applymap(lambda x:asset_inputs.loc[asset_inputs['Currency'] == x, 'IR Tickers'].iloc[0])
    secondCurrencyIRTickerList = secondCurrencyIRTicker['cross'].tolist()
    firstCurrencyIRData = all_data[firstCurrencyIRTickerList]
    secondCurrencyIRData = all_data[secondCurrencyIRTickerList]
    irData = firstCurrencyIRData.sub(secondCurrencyIRData)


    # process data

    # Define some variables from curp_inputs
    volWindow = curp_inputs.loc[curp_inputs['Variable Name'] == 'Volatility Window','CUMO'].iloc[0]
    historicalLevelAveraging =curp_inputs.loc[curp_inputs['Variable Name'] == 'Historical Level Averaging','CUMO'].iloc[0]
    window = curp_inputs.loc[curp_inputs['Variable Name']=='Window','CUMO'].iloc[0]
    signal = curp_inputs.loc[curp_inputs['Variable Name']=='Signal','CUMO'].iloc[0]
    ret = curp_inputs.loc[curp_inputs['Variable Name'] == 'Returns', 'CUMO'].iloc[0]

    # Define which type of data should be used for the signals. From the inputs
    # signalData = ...
    if signal == 1 or signal == 5 or signal == 6:
        signalData = spotData
    else:
        signalData = carryData

    # returnData = ...
    if ret == 1:
        returnData = spotData
    else:
        returnData = carryData

    vol = sqrt(12)*pd.rolling_std(signalData,volWindow)
    # could take the rolling average then use 'shift' on the column
    sharpeAvgData = pd.rolling_mean(rebasedSignalData,2*historicalLevelAveraging)
    # I think i need to shift by 'Window' - 'Historic Volatility Window'
    sharpeAvgDataOffset = sharpeAvgData.shift(window-historicalLevelAveraging)

    if signal == 4:
        denominator = 1
    else:
        denominator = sqrt(12)*pd.rolling_std(signalData,window)

    sharpe = (math.log(rebasedSignalData.div(sharpeAvgDataOffset)) ** (12 / window) - 1)/denominator



    pass

def create_crosses(currencyList):
    # create data frame
    output = pd.DataFrame(columns=['cross'])
    for i in list(range(1,(len(currencyList.index)))):
        for j in list(range(i+1,len(currencyList.index)+1)):
            output = output.append(dict(cross=currencyList[i] + currencyList[j]), ignore_index=True)
    x = output
    return x

if __name__ == "__main__":
    # test inputs

    curp_inputs, asset_inputs, all_data = gd.extract_inputs_and_mat_data(model_type, mat_file, input_file)
