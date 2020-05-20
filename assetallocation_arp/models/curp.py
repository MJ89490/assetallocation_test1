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

    all_data= all_data.asfreq('BM')
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
    map = pd.DataFrame(np.array(
        [[-1, -0.05], [-0.05, -0.045], [-0.045, -0.04], [-0.04, -0.035], [-0.035, -0.03], [-0.03, -0.025],
         [-0.025, -0.02], [-0.02, -0.015], [-0.015, -0.01], [-0.01, -0.005], [-0.005, 0.0], [0.0, 0.0], [0.005, 0.005],
         [0.01, 0.01], [0.015, 0.015], [0.02, 0.02], [0.025, 0.025], [0.03, 0.03], [0.035, 0.035], [0.04, 0.04],
         [0.045, 0.045], [0.05, 0.05]]), columns=['Expected Return %', 'over/underweight %'])


    # create all FX crosses from the ones given
    currencyCrosses = create_crosses(asset_inputs['Currency'])
    currencyCrossesList = currencyCrosses.cross.tolist()
    firstCurrency = currencyCrosses.applymap(lambda x: x[0:3])
    secondCurrency = currencyCrosses.applymap(lambda x: x[3:6])

    # Spot Data
    firstCurrencySpotTicker = firstCurrency.applymap(lambda x: x +'USD Curncy')
    secondCurrencySpotTicker = secondCurrency.applymap(lambda x: x + 'USD Curncy')
    firstCurrencySpotData = all_data[firstCurrencySpotTicker['cross'].tolist()]
    secondCurrencySpotData = all_data[secondCurrencySpotTicker['cross'].tolist()]
    firstCurrencySpotData.columns = currencyCrossesList
    secondCurrencySpotData.columns = currencyCrossesList
    spotData = firstCurrencySpotData.div(secondCurrencySpotData)/firstCurrencySpotData.div(secondCurrencySpotData).shift(1) - 1
    spotDataRebased = firstCurrencySpotData.div(secondCurrencySpotData)
    # Carry Data
    firstCurrencyCarryTicker = firstCurrency.applymap(lambda x: x +'USDCR Curncy')
    secondCurrencyCarryTicker = secondCurrency.applymap(lambda x: x + 'USDCR Curncy')
    firstCurrencyCarryData = all_data[firstCurrencyCarryTicker['cross'].tolist()]
    secondCurrencyCarryData = all_data[secondCurrencyCarryTicker['cross'].tolist()]
    firstCurrencyCarryData.columns = currencyCrossesList
    secondCurrencyCarryData.columns = currencyCrossesList
    carryData = firstCurrencyCarryData.div(secondCurrencyCarryData) / firstCurrencyCarryData.div(secondCurrencyCarryData).shift(1) - 1
    carryDataRebased = firstCurrencyCarryData.div(secondCurrencyCarryData)

    # PPP Data
    firstCurrencyPPPTicker = firstCurrency.applymap(lambda x:asset_inputs.loc[asset_inputs['Currency'] == x, 'PPP Tickers'].iloc[0])
    secondCurrencyPPPTicker = secondCurrency.applymap(lambda x:asset_inputs.loc[asset_inputs['Currency'] == x, 'PPP Tickers'].iloc[0])
    firstCurrencyPPPData = all_data[firstCurrencyPPPTicker['cross'].tolist()]
    secondCurrencyPPPData = all_data[secondCurrencyPPPTicker['cross'].tolist()]
    firstCurrencyPPPData.columns = currencyCrossesList
    secondCurrencyPPPData.columns = currencyCrossesList
    pppData = secondCurrencyPPPData.div(firstCurrencyPPPData)

    # IR Data
    firstCurrencyIRTicker = firstCurrency.applymap(lambda x:asset_inputs.loc[asset_inputs['Currency'] == x, 'IR Tickers'].iloc[0])
    secondCurrencyIRTicker = secondCurrency.applymap(lambda x:asset_inputs.loc[asset_inputs['Currency'] == x, 'IR Tickers'].iloc[0])
    firstCurrencyIRData = all_data[firstCurrencyIRTicker['cross'].tolist()]
    secondCurrencyIRData = all_data[secondCurrencyIRTicker['cross'].tolist()]
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
    lag1 = curp_inputs.loc[curp_inputs['Variable Name'] == 'Lag 1 weight', 'CUMO'].iloc[0]
    lag2 = curp_inputs.loc[curp_inputs['Variable Name'] == 'Lag 2 weight', 'CUMO'].iloc[0]
    lag3 = curp_inputs.loc[curp_inputs['Variable Name'] == 'Lag 3 weight', 'CUMO'].iloc[0]
    lag4 = curp_inputs.loc[curp_inputs['Variable Name'] == 'Lag 4 weight', 'CUMO'].iloc[0]
    lag5 = curp_inputs.loc[curp_inputs['Variable Name'] == 'Lag 5 weight', 'CUMO'].iloc[0]
    lag6 = curp_inputs.loc[curp_inputs['Variable Name'] == 'Lag 6 weight', 'CUMO'].iloc[0]

    # signalData is % terms
    # rebasedSignalData is a price series

    if signal == 1 or signal == 5 or signal == 6:
        signalData = spotData.copy()
        signalDataIndex = spotDataRebased.copy()
    else:
        signalData = carryData.copy()
        signalDataIndex = carryDataRebased.copy()

    # returnData = ...
    if ret == 1:
        returnData = spotData.copy()
    else:
        returnData = carryData.copy()

    vol = math.sqrt(12) * signalData.rolling(volWindow).std()
    sharpeAvgData = signalDataIndex.rolling(2*historicalLevelAveraging+1).mean()
    sharpeAvgDataOffset = sharpeAvgData.shift(window-historicalLevelAveraging)

    if signal == 4:
        denominator = 1
    else:
        denominator = math.sqrt(12)*signalData.rolling(window).std()

    sharpe = ((signalDataIndex.div(sharpeAvgDataOffset).applymap(lambda x: math.log(x))+1)**(12/window)-1)/denominator

    # Signals tab
    # first matrix
    if signal == 5 or signal == 6:
        if signal == 6:
            denominator = curp_inputs.loc[curp_inputs['Variable Name'] == 'Dyn Hedge Mean Reversion', 'CUMO'].iloc[0]
        else:
            denominator = 1
        frstMatrix = (map_USD(firstCurrency, secondCurrency, currencyCrossesList, signalData) * 100 * pppData.div(signalDataIndex)-1) / denominator + (signal-5)*irData

    elif signal == 3 or signal == 4:
        frstMatrix = ((irData -(signal-3)) *((1+sharpe)**(window/12)-1)) * curp_inputs.loc[curp_inputs['Variable Name'] == 'Dyn Hedge Mean Reversion', 'CUMO'].iloc[0]
    else:
        # t_1 = (lag1*signalData + lag2*signalData.shift(1) + lag3*signalData.shift(2) + lag4*signalData.shift(3)+lag5*signalData.shift(4)+lag6*signalData.shift(5))/(lag1+lag2+lag3+lag4+lag5+lag6)
        # t_2 = (1+t_1)**12-1
        # t_3 = t_2/denominator
        # frstMatrix = t_3.copy()

        if curp_inputs.loc[curp_inputs['Variable Name'] == 'Volatility Adjustment Signal', 'CUMO'].iloc[0] == True:
            denominator = vol
        else:
            denominator = 1
        frstMatrix = ((1+((lag1*signalData + lag2*signalData.shift(1) + lag3*signalData.shift(2) + lag4*signalData.shift(3)+lag5*signalData.shift(4)+lag6*signalData.shift(5))/(lag1+lag2+lag3+lag4+lag5+lag6)))**12-1)/denominator

    # second matrix
    if curp_inputs.loc[curp_inputs['Variable Name'] == 'Value Adjustment', 'CUMO'].iloc[0] == True:
        # need a fancy way to check if the signs are equal
        # map all values to 1 or -1 for both matrices. map 0's to 10. add the two together. if abs is 2 then the same sign. if abs is 20 then both 0's.
        # map all values to 1 or -1 for both matrices.
        t_1 = frstMatrix.copy()
        t_1 = t_1.applymap(lambda x: 1 if x > 0 else(-1 if x < 0 else 10))
        t_2 = sharpe.copy()
        t_2 = t_2.applymap(lambda x: 1 if x > 0 else(-1 if x < 0 else 10))
        # add the two together.
        t_3 = t_1 + t_2
        # if abs is 2 then the same sign. if abs is 20 then both 0's. Otherwise will be 0,9,11
        t_3[t_3 == 20] = 2
        t_3[t_3 == -2] = 2
        t_3[t_3 == 9] = 0
        t_3[t_3 == 11] = 0
        # if t_3 = 2 then the sign is the same, if its 0 then not the same
        t_3 = t_3.applymap(lambda x: 1 if x == 2 else 0)
        t_4 = sharpe.copy()
        t_4 = t_4.applymap(lambda x: abs(x))
        sharpeCutoff = curp_inputs.loc[curp_inputs['Variable Name'] == 'Sharpe Cut-Off', 'CUMO'].iloc[0]
        t_4 = t_4.applymap(lambda x: 1 if x > sharpeCutoff else 0)
        #add them together, where this is 2 both conditions are satisfied. Map this to 0, map everything else to 1. Then can multiply through by this matrix to ge tthe desired outcome :)
        t_5 = t_3 + t_4
        t_5 = t_5.applymap(lambda x : 0 if x == 2 else 1)
        scndMatrix = t_5 * frstMatrix
    else:
        scndMatrix = frstMatrix.copy()

    # third matrix
    if curp_inputs.loc[curp_inputs['Variable Name'] == 'Response Function', 'CUMO'].iloc[0] == True:
        thrdMatrix = scndMatrix.applymap(lambda x: abs(x)* exp(-(abs(x)**2/4)))
    else:
        thrdMatrix = scndMatrix.applymap(lambda x: abs(x))

    # fourth matrix
    frthMatrix = scndMatrix.applymap(lambda x: 1 if x > 0 else (0 if x == 0 else -1))

    # fifth matrix
    if signal == 5:
        # create new column of the nth max & min
        noCrosses = curp_inputs.loc[curp_inputs['Variable Name'] == '# Top Crosses', 'CUMO'].iloc[0]
        ffthMatrix = frstMatrix.copy()
        ffthMatrix['nth max'] = np.nan
        ffthMatrix['nth min'] = np.nan
        for row in frstMatrix.index:
            # need to define an output matrix
            ffthMatrix.loc[[row], ['nth max']] = frstMatrix.loc[row].squeeze().nlargest(n=noCrosses).min()
            ffthMatrix.loc[[row], ['nth min']] = - frstMatrix.loc[row].squeeze().nsmallest(n=noCrosses).max()
            # drop excess cols when done with them
        ffthMatrixTop = ffthMatrix.copy()
        ffthMatrixBottom = ffthMatrix.copy()
        for column in ffthMatrix.columns:
            ffthMatrixTop[column] = ffthMatrix[column]/ffthMatrix['nth max']
            ffthMatrixBottom[column] = - ffthMatrix[column] / ffthMatrix['nth min']
        # drop those cols
        # ffthMatrix = ffthMatrix.drop(columns = ['nth max','nth min'])
        ffthMatrixTop = ffthMatrixTop.drop(columns = ['nth max','nth min'])
        ffthMatrixBottom = ffthMatrixBottom.drop(columns=['nth max', 'nth min'])
        ffthMatrixTop = ffthMatrixTop.applymap(lambda x: 1 if x>=1 else 0)
        ffthMatrixBottom = ffthMatrixBottom.applymap(lambda x: -1 if x>=1 else 0)
        #turn into signals
        ffthMatrix = (ffthMatrixBottom+ffthMatrixTop)*map_USD(firstCurrency, secondCurrency, currencyCrossesList, signalData)/noCrosses

    else:
        # index match on weights
        roundedNumbers = frstMatrix.applymap(lambda x: np.floor(2*x)/200)
        roundedNumbers = roundedNumbers.fillna(value=0)
        roundedNumbers[roundedNumbers < -0.05] = -1
        roundedNumbers[roundedNumbers > 0.05] = 0.05
        # now need to index match it
        ffthMatrix = roundedNumbers.copy()
        ffthMatrix = ffthMatrix.applymap(lambda x: map.loc[map['Expected Return %'] == x, 'over/underweight %'].iloc[0])

    # sixth matrix
    # finalSignals
    # Loop through currency list
    #for each currency, create a column of indicators if first/second currency is that currency
    #tranpose
    #set new columns
    #repeat rows
    #set new index
    #multiply through
    #subtract one from the other
    #put this in the new output
    outputSignals = pd.DataFrame([],columns = asset_inputs['Currency'].tolist())
    for currency in asset_inputs['Currency']:
        temp = pd.DataFrame([0] * len(currencyCrossesList), columns=['indicator'])
        temp['firstCurrency'] = firstCurrency
        temp['secondCurrency'] = secondCurrency
        temp.loc[(temp['firstCurrency'] == currency),'indicator'] = 1
        temp.loc[(temp['secondCurrency'] == currency), 'indicator'] = -1
        temp = temp.transpose()
        temp = temp.head(1)
        temp.columns = currencyCrossesList
        temp = pd.concat([temp]*len(signalData.index))
        temp['new index'] = signalData.index
        temp.set_index('new index', inplace=True)
        temp = temp * ffthMatrix
        outputSignals[currency] = temp.sum(axis=1)
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

def momentum (data, weights):
    # this wont change the frequency of data
    for i in list(range(0,len(weights))):
        mom = mom + weights[i] * data.shift(i)
        denominator = denominator + weights[i]
    x = mom/denominator
    return mom

if __name__ == "__main__":
    # test inputs

    curp_inputs, asset_inputs, all_data = gd.extract_inputs_and_mat_data(model_type, mat_file, input_file)
