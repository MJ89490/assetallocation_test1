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
import data_etl.import_data as gd
import xlwings as xw


# my formatting is that variables are camel case, functions use _

# Curp Carve out file \\inv\LGIM\FrontOffice\Bonds\Asset Allocation\Research&Strategy\ARP\CURP Carve Out.xlsm
# CUMO file \\inv\LGIM\FrontOffice\Bonds\Asset Allocation\Research&Strategy\ARP\CUMO.xlsm

# TO DO:
# think of a good way to pass in weights data. might need additional input for it
# Attribution etc
# full testing of other unused models
# moving things round e.g. momentum


def run_curp(curp_inputs, asset_inputs, all_data):
    # this will be where the main code is run

    volWindow = curp_inputs.loc[curp_inputs['Variable Name'] == 'Volatility Window','CUMO'].iloc[0]
    historicalLevelAveraging =curp_inputs.loc[curp_inputs['Variable Name'] == 'Historical Level Averaging','CUMO'].iloc[0]
    window = curp_inputs.loc[curp_inputs['Variable Name']=='Window','CUMO'].iloc[0]
    signal = curp_inputs.loc[curp_inputs['Variable Name']=='Signal','CUMO'].iloc[0]
    ret = curp_inputs.loc[curp_inputs['Variable Name'] == 'Returns', 'CUMO'].iloc[0]

    # create all FX crosses from the ones given
    currencyCrosses = create_crosses(asset_inputs['Currency'])
    currencyCrossesList = currencyCrosses.cross.tolist()
    firstCurrency = currencyCrosses.applymap(lambda x: x[0:3])
    secondCurrency = currencyCrosses.applymap(lambda x: x[3:6])

    # need to define dataType, as either 'Spot' or 'Carry'. Should be passed as an input
    if signal == 1 or signal == 5 or signal == 6:
        dataType ='Spot'
    else:
        dataType = 'Carry'

    signalData, signalDataIndex = filter_data(dataType, firstCurrency, secondCurrency, currencyCrossesList, all_data)
    pppData = ppp_data(firstCurrency, secondCurrency, currencyCrossesList, asset_inputs, all_data)
    irData = ir_data(firstCurrency, secondCurrency, currencyCrossesList, asset_inputs, all_data)

    sharpeAvgData = signalDataIndex.rolling(2*historicalLevelAveraging+1).mean()
    sharpeAvgDataOffset = sharpeAvgData.shift(window-historicalLevelAveraging)

    if signal == 4: # model = 'Dynamic Hedging'
        denominator = 1
    else:
        # here window is used and not vol window... why?
        denominator = math.sqrt(12)*signalData.rolling(window).std()
    sharpe = ((signalDataIndex.div(sharpeAvgDataOffset).applymap(lambda x: math.log(x))+1)**(12/window)-1)/denominator

    # Signals tab

    if signal == 5 or signal == 6: # if model == 'PPP USD' or model == 'PPP CURP'
        if signal == 6: # if model = 'PPP CURP'
            denominator = curp_inputs.loc[curp_inputs['Variable Name'] == 'Dyn Hedge Mean Reversion', 'CUMO'].iloc[0]
        else:
            denominator = 1
        frstMatrix = (map_USD(firstCurrency, secondCurrency, currencyCrossesList, signalData) * 100 * pppData.div(signalDataIndex)-1) / denominator + (signal-5)*irData

    elif signal == 3 or signal == 4: # if model == 'Dynamic Hedging' or model == 'PPP All'
        # will need to fix this next bit too.
        frstMatrix = ((irData -(signal-3)) *((1+sharpe)**(window/12)-1)) * curp_inputs.loc[curp_inputs['Variable Name'] == 'Dyn Hedge Mean Reversion', 'CUMO'].iloc[0]
    else:
        if curp_inputs.loc[curp_inputs['Variable Name'] == 'Volatility Adjustment Signal', 'CUMO'].iloc[0] == True:
            # here vol window is used
            denominator = math.sqrt(12) * signalData.rolling(volWindow).std()
        else:
            denominator = 1
        # remove the hard coding
        frstMatrix =((1+momentum(signalData,[6,5,4,3,2,1]))**12-1)/denominator

    # second matrix
    if curp_inputs.loc[curp_inputs['Variable Name'] == 'Value Adjustment', 'CUMO'].iloc[0] == True:
        sharpeCutoff = curp_inputs.loc[curp_inputs['Variable Name'] == 'Sharpe Cut-Off', 'CUMO'].iloc[0]
        scndMatrix = frstMatrix.applymap(lambda x: 1 if -sharpeCutoff <= x <= sharpeCutoff else 0)
        # scndMatrix = same_sign_indicator(frstMatrix,sharpe,curp_inputs) * frstMatrix
    else:
        scndMatrix = frstMatrix.copy()

    # third matrix
    if curp_inputs.loc[curp_inputs['Variable Name'] == 'Response Function', 'CUMO'].iloc[0] == True:
        thrdMatrix = scndMatrix.applymap(lambda x: abs(x)* exp(-(abs(x)**2/4)))
    else:
        thrdMatrix = scndMatrix.applymap(lambda x: abs(x))

    # fourth matrix - just takes the sign
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
        ffthMatrixTop = ffthMatrixTop.drop(columns=['nth max','nth min'])
        ffthMatrixBottom = ffthMatrixBottom.drop(columns=['nth max', 'nth min'])
        ffthMatrixTop = ffthMatrixTop.applymap(lambda x: 1 if x >= 1 else 0)
        ffthMatrixBottom = ffthMatrixBottom.applymap(lambda x: -1 if x >= 1 else 0)
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
        temp.index = signalData.index
        # temp.set_index('new index', inplace=True)
        temp = temp * ffthMatrix
        outputSignals[currency] = temp.sum(axis=1)
    pass

#just changing something so I can commit



def create_crosses(currencyList):
    """

    :param currencyList: list of currencies, in the 3 letter ticker  code  format e.g. ['GBP','EUR',...]
    :return: a list of all crosses of the inputs. Only one of the 2 permutuations will exist. e.g. 'GBPEUR' will exist but not 'EURGBP'
    """
    output = pd.DataFrame(columns=['cross'])
    for i in list(range(1,(len(currencyList.index)))):
        for j in list(range(i+1,len(currencyList.index)+1)):
            output = output.append(dict(cross=currencyList[i] + currencyList[j]), ignore_index=True)
    x = output
    return x

def rebase_data(data):
    """

    :param data: data which needs to be rebased
    :return: rebased data, starting the index with 1 for all instruments.
    """
    t_1 = data.head(1)
    t_2 = pd.concat([t_1]*len(data.index))
    t_2['New Index'] = data.index
    t_2.set_index('New Index',inplace=True)
    output = data.div(t_2)
    return output

def map_USD(firstCurrency, secondCurrency, currencyCrossesList, data):
    """

    :param firstCurrency: List with the first FX of the currency cross
    :param secondCurrency: List with the second FX of the currency cross
    :param currencyCrossesList: List of the currency crosses
    :param data: the data that needs to have the map applied to it
    :return: the data, multiplied by a matrix where if the first half of the FX cross is USD the value is -1, or +1 if the second part of the cross is USD. If neither, the multplier is 0
    """
    temp = pd.DataFrame([0]*len(firstCurrency),columns = ['value'])
    temp['first'] = firstCurrency
    temp['second'] = secondCurrency
    temp.loc[(temp['first']=='USD'),'value'] = -1
    temp.loc[(temp['second'] == 'USD'), 'value'] = 1
    temp = temp.transpose()
    temp = temp.head(1)
    temp.columns = currencyCrossesList
    temp = pd.concat([temp]*len(data.index))
    temp['new index'] = data.index
    temp.set_index('new index', inplace=True)
    return temp

def momentum (data, weights):
    """

    :param data: data to apply the momentum calcs to
    :param weights: weights  to apply, in a list  of variable length
    :return: DataFrame of the momentum scores. The first item in the weights list is applied to the most recent observation as an exponential weight, then etc.
    """
    # this wont change the frequency of data
    # variable number of inputs (weights)
    # ensure that lag 1 weight is first, i.e. most recent first.
    mom = pd.DataFrame([], columns = data.columns)
    denominator = 0
    for i in list(range(0,len(weights))):
        if i == 0:
            mom = weights[i] * data
            denominator = weights[i]
        else:
            mom = mom + weights[i] * data.shift(i)
            denominator = denominator + weights[i]
    x = mom/denominator
    return x

def filter_data(returnType, firstCurrency, secondCurrency,currencyCrossesList,data):
    """

    :param returnType: spot or carry
    :param firstCurrency: list of first FX in cross, e.g. ['GBP','EUR',...]
    :param secondCurrency: list of second FX in cross, e.g. ['GBP','EUR',...]
    :param currencyCrossesList: list of crosses, e.g. ['GBPEUR',...]
    :param data: DataFrame containing all of the data
    :return: filtered data, either spot or carry, for all of the FX crosses
    """
    if returnType == 'Spot':
        suffix = 'USD Curncy'
    else:
        suffix = 'USDCR Curncy'
    firstCurrencyTicker = firstCurrency.applymap(lambda x: x +suffix)
    secondCurrencyTicker = secondCurrency.applymap(lambda x: x + suffix)
    firstCurrencyData = data[firstCurrencyTicker['cross'].tolist()]
    secondCurrencyData = data[secondCurrencyTicker['cross'].tolist()]
    firstCurrencyData.columns = currencyCrossesList
    secondCurrencyData.columns = currencyCrossesList
    data = firstCurrencyData.div(secondCurrencyData)/firstCurrencyData.div(secondCurrencyData).shift(1) - 1
    dataIndex = firstCurrencyData.div(secondCurrencyData)
    return data, dataIndex

def ppp_data(firstCurrency,secondCurrency,currencyCrossesList, asset_inputs,all_data):
    """

    :param firstCurrency: list of first FX in cross, e.g. ['GBP','EUR',...]
    :param secondCurrency: list of second FX in cross, e.g. ['GBP','EUR',...]
    :param currencyCrossesList: list of crosses, e.g. ['GBPEUR',...]
    :param asset_inputs: inputs from the spreadsheet with different variables
    :param all_data: DataFrame containing all of the data
    :return: filtered PPP data
    """
    firstCurrencyTicker = firstCurrency.applymap(lambda x:asset_inputs.loc[asset_inputs['Currency'] == x, 'PPP Tickers'].iloc[0])
    secondCurrencyTicker = secondCurrency.applymap(lambda x:asset_inputs.loc[asset_inputs['Currency'] == x, 'PPP Tickers'].iloc[0])
    firstCurrencyData = all_data[firstCurrencyTicker['cross'].tolist()]
    secondCurrencyData = all_data[secondCurrencyTicker['cross'].tolist()]
    firstCurrencyData.columns = currencyCrossesList
    secondCurrencyData.columns = currencyCrossesList
    data = secondCurrencyData.div(firstCurrencyData)
    return data

def ir_data(firstCurrency,secondCurrency,currencyCrossesList,asset_inputs,all_data):
    """

    :param firstCurrency: list of first FX in cross, e.g. ['GBP','EUR',...]
    :param secondCurrency: list of second FX in cross, e.g. ['GBP','EUR',...]
    :param currencyCrossesList: list of crosses, e.g. ['GBPEUR',...]
    :param asset_inputs: inputs from the spreadsheet with different variables
    :param all_data: DataFrame containing all of the data
    :return: filtered IR data
    """
    firstCurrencyIRTicker = firstCurrency.applymap(lambda x:asset_inputs.loc[asset_inputs['Currency'] == x, 'IR Tickers'].iloc[0])
    secondCurrencyIRTicker = secondCurrency.applymap(lambda x:asset_inputs.loc[asset_inputs['Currency'] == x, 'IR Tickers'].iloc[0])
    firstCurrencyIRData = all_data[firstCurrencyIRTicker['cross'].tolist()]
    secondCurrencyIRData = all_data[secondCurrencyIRTicker['cross'].tolist()]
    firstCurrencyIRData.columns = currencyCrossesList
    secondCurrencyIRData.columns = currencyCrossesList
    data = firstCurrencyIRData.sub(secondCurrencyIRData)
    return data

def same_sign_indicator(data_first_matrix,data_sharpe, curp_inputs):
    """

    :param data_first_matrix: dataFrame with output from the first stage
    :param data_sharpe: Sharpe data in a dataframe
    :param curp_inputs: curp inputs from spreadsheet
    :return: 0 if the absolute value of the sharpe ratio is > than the cutoff AND the sign is the same, else
    """
    # think this might be unused
    # need a fancy way to check if the signs are equal
    # map all values to 1 or -1 for both matrices. map 0's to 10. add the two together. if abs is 2 then the same sign. if abs is 20 then both 0's.
    # map all values to 1 or -1 for both matrices.
    t_1 = data_first_matrix.applymap(lambda x: 1 if x > 0 else (-1 if x < 0 else 10))
    t_2 = data_sharpe.applymap(lambda x: 1 if x > 0 else (-1 if x < 0 else 10))
    t_3 = t_1 + t_2
    # if abs is 2 then the same sign. if abs is 20 then both 0's. Otherwise will be 0,9,11
    t_3[t_3 == 20] = 2
    t_3[t_3 == -2] = 2
    t_3[t_3 == 9] = 0
    t_3[t_3 == 11] = 0
    # if t_3 = 2 then the sign is the same, if its 0 then not the same
    t_3 = t_3.applymap(lambda x: 1 if x == 2 else 0)
    # define first to speed up calc
    sharpeCutoff = curp_inputs.loc[curp_inputs['Variable Name'] == 'Sharpe Cut-Off', 'CUMO'].iloc[0]
    t_4 = t_3.applymap(lambda x: 1 if abs(x) > sharpeCutoff else 0)
    # add them together, where this is 2 both conditions are satisfied. Map this to 0, map everything else to 1. Then can multiply through by this matrix to ge tthe desired outcome :)
    t_5 = t_3 + t_4
    t_5 = t_5.applymap(lambda x: 0 if x == 2 else 1)
    return t_5

if __name__ == "__main__":
    # test inputs
    curp_inputs, asset_inputs, all_data = gd.extract_inputs_and_mat_data(model_type, mat_file, input_file)
    import data_etl.import_data as gd
    import math
    import numpy as np
    import pandas as pd
    from models.curp import rebase_data
    from models.curp import map_USD
    from models.curp import create_crosses

    file_path = r'S:\FrontOffice\Structured Products\Solutions Group\SIRM\Shared\Simone\Python\Data\matlabData.mat'
    input_path = r'H:\PycharmProjects\assetallocation_arp\assetallocation_arp\arp_dashboard.xlsm'
    model_type = 'curp'
    mat_file = file_path
    input_file = input_path
    curp_inputs, asset_inputs, all_data = gd.extract_inputs_and_mat_data(model_type, mat_file, input_file)

    all_data = all_data.asfreq('BM')
    all_data['USDUSD Curncy'] = 1
    all_data['USDUSDCR Curncy'] = 1

    # sort data problems
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
