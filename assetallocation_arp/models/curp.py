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

    # These models only run monthly. start by stripping out all other data

    all_data= all_data.asfreq('M').ffill()
    all_data= all_data.loc['1999-12-31':]
    all_data['USDUSD Curncy'] = 1
    all_data['USDUSDCR Curncy'] = 1
    # this below should be deleted when the data is made available in the mat file
    all_data['SEKUSD Curncy'] = 1/all_data['USDSEK Curncy']
    all_data['CHFUSD Curncy'] = 1/all_data['USDCHF Curncy']
    all_data['NOKUSD Curncy'] = 1/all_data['USDNOK Curncy']
    all_data['CHFUSDCR Curncy'] = 1/all_data['USDCHFCR Curncy']
    all_data['SEKUSDCR Curncy'] = 1/all_data['USDSEKCR Curncy']
    all_data['CADUSDCR Curncy'] = 1/all_data['USDCADCR Curncy']
    all_data['NOKUSDCR Curncy'] = 1/all_data['USDNOKCR Curncy']
    all_data['JPYUSDCR Curncy'] = 1/all_data['USDJPYCR Curncy']

    # create all FX crosses from the ones given
    currencyCrosses = create_crosses(asset_inputs['Currency'])
    currencyCrossesList = currencyCrosses.cross.tolist()
    firstCurrency = currencyCrosses.applymap(lambda x: x[0:3])
    secondCurrency = currencyCrosses.applymap(lambda x: x[3:6])

    # Spot Data
    firstCurrencySpotTicker = firstCurrency.applymap(lambda x: x +'USD Curncy')
    firstCurrencySpotTickerList = firstCurrencySpotTicker['cross'].tolist()
    secondCurrencySpotTicker = secondCurrency.applymap(lambda x: x + 'USD Curncy')
    secondCurrencySpotTickerList = secondCurrencySpotTicker['cross'].tolist()
    firstCurrencySpotData = all_data[firstCurrencySpotTickerList]
    secondCurrencySpotData = all_data[secondCurrencySpotTickerList]
    firstCurrencySpotData.columns = currencyCrossesList
    secondCurrencySpotData.columns = currencyCrossesList
    spotDataTemp = firstCurrencySpotData.div(secondCurrencySpotData)
    spotData = spotDataTemp/spotDataTemp.shift(1) -1
    spotDataRebased = rebase_data(spotData)
    # Carry Data
    firstCurrencyCarryTicker = firstCurrency.applymap(lambda x: x +'USDCR Curncy')
    firstCurrencyCarryTickerList = firstCurrencyCarryTicker['cross'].tolist()
    secondCurrencyCarryTicker = secondCurrency.applymap(lambda x: x + 'USDCR Curncy')
    secondCurrencyCarryTickerList = secondCurrencyCarryTicker['cross'].tolist()
    firstCurrencyCarryData = all_data[firstCurrencyCarryTickerList]
    secondCurrencyCarryData = all_data[secondCurrencyCarryTickerList]
    firstCurrencyCarryData.columns = currencyCrossesList
    secondCurrencyCarryData.columns = currencyCrossesList
    carryDataTemp = firstCurrencyCarryData.div(secondCurrencyCarryData)
    carryData = carryDataTemp / carryDataTemp.shift(1) - 1
    carryDataRebased = rebase_data(carryData)

    # PPP Data
    firstCurrencyPPPTicker = firstCurrency.applymap(lambda x:asset_inputs.loc[asset_inputs['Currency'] == x, 'PPP Tickers'].iloc[0])
    firstCurrencyPPPTickerList = firstCurrencyPPPTicker['cross'].tolist()
    secondCurrencyPPPTicker = secondCurrency.applymap(lambda x:asset_inputs.loc[asset_inputs['Currency'] == x, 'PPP Tickers'].iloc[0])
    secondCurrencyPPPTickerList = secondCurrencyPPPTicker['cross'].tolist()
    firstCurrencyPPPData = all_data[firstCurrencyPPPTickerList]
    secondCurrencyPPPData = all_data[secondCurrencyPPPTickerList]
    firstCurrencyPPPData.columns = currencyCrossesList
    secondCurrencyPPPData.columns = currencyCrossesList
    pppData = secondCurrencyPPPData.div(firstCurrencyPPPData)

    # IR Data
    firstCurrencyIRTicker = firstCurrency.applymap(lambda x:asset_inputs.loc[asset_inputs['Currency'] == x, 'IR Tickers'].iloc[0])
    firstCurrencyIRTickerList = firstCurrencyIRTicker['cross'].tolist()
    secondCurrencyIRTicker = secondCurrency.applymap(lambda x:asset_inputs.loc[asset_inputs['Currency'] == x, 'IR Tickers'].iloc[0])
    secondCurrencyIRTickerList = secondCurrencyIRTicker['cross'].tolist()
    firstCurrencyIRData = all_data[firstCurrencyIRTickerList]
    secondCurrencyIRData = all_data[secondCurrencyIRTickerList]
    firstCurrencyIRData.columns = currencyCrossesList
    secondCurrencyIRData.columns = currencyCrossesList
    irData = firstCurrencyIRData.sub(secondCurrencyIRData)

    # process data

    # Define some variables from curp_inputs
    volWindow = curp_inputs.loc[curp_inputs['Variable Name'] == 'Volatility Window','CUMO'].iloc[0]
    historicalLevelAveraging =curp_inputs.loc[curp_inputs['Variable Name'] == 'Historical Level Averaging','CUMO'].iloc[0]
    window = curp_inputs.loc[curp_inputs['Variable Name']=='Window','CUMO'].iloc[0]
    signal = curp_inputs.loc[curp_inputs['Variable Name']=='Signal','CUMO'].iloc[0]
    ret = curp_inputs.loc[curp_inputs['Variable Name'] == 'Returns', 'CUMO'].iloc[0]

    # Define which type of data should be used for the signals. From the inputs
    # signalData is % terms
    # rebasedSignalData is rebased

    if signal == 1 or signal == 5 or signal == 6:
        signalData = spotData
        signalDataIndex = spotDataTemp
    else:
        signalData = carryData
        signalDataIndex = carryDataTemp

    # returnData = ...
    if ret == 1:
        returnData = spotData
    else:
        returnData = carryData

    vol = math.sqrt(12) * signalData.rolling(volWindow).std()
    # could take the rolling average then use 'shift' on the column
    sharpeAvgData = signalDataIndex.rolling(2*historicalLevelAveraging).mean()
    # I think i need to shift by 'Window' - 'Historic Volatility Window' --- this needs checking
    sharpeAvgDataOffset = sharpeAvgData.shift(window-historicalLevelAveraging)

    if signal == 4:
        denominator = 1
    else:
        denominator = sqrt(12)*signalData.rolling(window).std()

    temp = signalDataIndex.div(sharpeAvgDataOffset)
    temp = temp.applymap(lambda x: math.log(x))

    sharpe = ((temp+1)**(12/window)-1)/denominator

    # Signals tab
    # if signal == 5 or signal == 6:

    pass

def create_crosses(currencyList):
    # create data frame
    output = pd.DataFrame(columns=['cross'])
    for i in list(range(1,(len(currencyList.index)))):
        for j in list(range(i+1,len(currencyList.index)+1)):
            output = output.append(dict(cross=currencyList[i] + currencyList[j]), ignore_index=True)
    x = output
    return x

def rebase_data(data):
    t_1 = data.head(1)
    t_2 = pd.concat([t_1]*len(data.index))
    t_2['New Index'] = data.index
    t_2.set_index('New Index',inplace=True)
    output = data.div(t_2)
    return output

def map_USD(firstCurrency, secondCurrency, currencyCrossesList, data):
    temp = pd.DataFrame([0]*len(firstCurrency),columns = ['value'])
    temp['first']=firstCurrency
    temp['second']=secondCurrency
    temp.loc[(temp['first']=='USD'),'value']=-1
    temp.loc[(temp['second'] == 'USD'), 'value'] = 1
    temp = temp.transpose()
    temp = temp.head(1)
    temp.columns = currencyCrossesList
    temp = pd.concat([temp]*len(data.index))
    temp['new index'] = data.index
    temp.set_index('new index', inplace=True)
    return temp

if __name__ == "__main__":
    # test inputs

    curp_inputs, asset_inputs, all_data = gd.extract_inputs_and_mat_data(model_type, mat_file, input_file)
