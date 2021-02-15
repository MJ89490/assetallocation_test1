# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 17:15:00 2020

@author: WK68945
"""
# import sys
# sys.path.append(r'S:\Shared\Front Office\Asset Allocation\Analytics\libs')
import numpy as np
import pandas as pd
import xlwings as xw
import bloomberg
from comca_attribution import comca_att, factor_att


def calculate_comca():
    wb = xw.Book.caller()
    bbg = bloomberg.Bloomberg()

    # Get Excel inputs and format
    date_to = wb.sheets['Dashboard'].range('rngDate').value
    date_from = wb.sheets['Dashboard'].range('rngDateF').value
    freq = wb.sheets['Dashboard'].range('rngFreq').value
    tblTickers = wb.sheets['Dashboard'].range('tblTickers').value
    rngIndices = wb.sheets['Dashboard'].range('rngIndices').value
    rngWeights = wb.sheets['Dashboard'].range('rngWeights').value
    tickers = pd.DataFrame(data=tblTickers, columns=rngIndices).set_index('Contract', drop=True)
    tickers_blp = tickers.applymap(lambda x: x + ' Index')
    tickers_blp = tickers_blp.values.flatten().tolist()
    comca_weights = pd.DataFrame(rngWeights, columns=['Name', 'Long', 'Short']).set_index(['Name']).replace(np.nan, 0)
    indices = [x + ' Index' for x in rngIndices[1:]]

    # Get Bloomberg data and format
    sub_data = bbg.historicalRequest(tickers_blp, "PX LAST", date_from, date_to, periodicitySelection="DAILY", \
                                       nonTradingDayFillOption="NON_TRADING_WEEKDAYS",
                                       nonTradingDayFillMethod="PREVIOUS_VALUE")
    index_data = bbg.historicalRequest(indices, "PX LAST", date_from, date_to, periodicitySelection="DAILY", \
                                       nonTradingDayFillOption="NON_TRADING_WEEKDAYS",
                                       nonTradingDayFillMethod="PREVIOUS_VALUE")
    members = bbg.referenceRequest(indices, {"INDX_MWEIGHT"})

    sub_data = pd.pivot_table(sub_data, values='bbergvalue', index=['bbergdate'],
                                columns=['bbergsymbol'], aggfunc=np.max)
    index_data = pd.pivot_table(index_data, values='bbergvalue', index=['bbergdate'],
                               columns=['bbergsymbol'], aggfunc=np.max)
    sub_data = sub_data[tickers_blp]
    index_data = index_data[indices]

    # Get constituent data from a Bloomberg reference request
    members = members.bbergvalue
    com = pd.DataFrame()
    exp = pd.DataFrame()
    for i in range(0, len(members)):
        start_com = members[i].find('{0', 0)
        start_exp = members[i].find('{0', start_com + 1)
        counter = start_com
        contract = 0
        while members[i].find(':', counter) != -1 and members[i].find(':', counter) < members[i].find('}'):
            counter = members[i].find(':', counter)
            com.loc[i, 'contract_'+str(contract)] = members[i][counter + 3: counter + 7]
            counter = counter + 1
            contract = contract + 1
        counter = start_exp
        contract = 0
        while members[i].find(":", counter) != -1:
            counter = members[i].find(':', counter)
            end = members[i].find(',', counter)
            exp.loc[i, 'contract_'+str(contract)] = members[i][counter + 1: end]
            counter = counter + 1
            contract = contract + 1
    exp = exp.replace('\}', '', regex=True)

    # combining commodity tickers and exposure
    com = com.replace(np.nan, '')
    com = com.applymap(lambda x: x[:2])
    exp = exp.replace(np.nan, 0).astype(float)
    weights = com.append(exp).sort_index()
    weights_final = pd.DataFrame(data=np.empty((len(tickers), 2 * len(com))), index=tickers.index)
    for i in range(0, len(com)):
        weights_i = weights.loc[i].reset_index(drop=True).T
        weights_i = weights_i.groupby([0]).sum()
        weights_i = pd.merge(tickers, weights_i, left_index=True, right_index=True)
        weights_final.iloc[:, 2 * i] = weights_i.iloc[:, i]
        weights_final.iloc[:, 2 * i + 1] = np.array(weights_i.iloc[:, -1:])

    # Reduce data
    if freq == 'WEEKLY':
        sub_data = sub_data.asfreq(freq='W', method='ffill')
        index_data = index_data.asfreq(freq='W', method='ffill')
    elif freq == 'MONTHLY':
        sub_data = sub_data.asfreq('BM')
        index_data = index_data.asfreq('BM')
    else:
        sub_data = sub_data.asfreq('B')
        index_data = index_data.asfreq('B')

    # calculate returns
    sub_return = np.log(sub_data.astype(float)).diff().iloc[1:]
    index_return = np.log(index_data.astype(float)).diff().iloc[1:]
    sub_return.columns = sub_return.columns.str.replace(' Index', '')
    index_return.columns = index_return.columns.str.replace(' Index', '')

    # summing up monthly
    sub_return = sub_return.resample('M', label='right', closed='right').sum()
    index_return = index_return.resample('M', label='right', closed='right').sum()

    # calculate attribution
    attribution = pd.DataFrame(data=np.zeros((len(sub_return), len(tickers))), index=sub_return.index, columns=tickers.index)
    for i in range(0, len(com)):
        #sub_weights = np.array([(weights_final.iloc[:, 2 * i + 1])] * len(sub_return))
        sub_weights = np.array([(weights_final.iloc[:, 1])] * len(sub_return))
        sub_weights = pd.DataFrame(data=sub_weights, index=sub_return.index, columns=weights_final.iloc[:, 2 * i])
        sub_attribution = (sub_return * sub_weights.astype(float) / 100).dropna(axis=1)
        sub_attribution = sub_attribution[sub_weights.columns]
        sub_attribution.columns = tickers.index
        attribution = attribution + sub_attribution * (comca_weights.iloc[i, 0] - comca_weights.iloc[i, 1])
    attribution['COMCA'] = attribution.sum(axis=1)

    # combining index returns and attribution
    output = index_return.merge(attribution, left_index=True, right_index=True)

    # write output to excel
    last_row = wb.sheets['ModelOutput'].range('B' + str(wb.sheets['ModelOutput'].cells.last_cell.row)).end('up').row
    wb.sheets['ModelOutput'].range("B3:AZ" + str(last_row)).clear_contents()
    wb.sheets['ModelOutput'].range('rngOutput').value = output

    # Calculate final attribution
    _ = comca_att(workbook=wb,
                  input_data=output,
                  year=2020)

    return output


def calculate_factor():
    wb = xw.Book.caller()
    bbg = bloomberg.Bloomberg()

    # Get Excel inputs and format
    date_to = wb.sheets['Dashboard'].range('rngDate').value
    date_from = wb.sheets['Dashboard'].range('rngDateF').value
    freq = wb.sheets['Dashboard'].range('rngFreq').value
    rngIndices = wb.sheets['Dashboard'].range('rngIndices').value
    indices = pd.DataFrame(data=rngIndices)
    tickers = indices.iloc[1, 1:-1].map(lambda x: x + ' Index').tolist()
    for i in range(1, int(len(indices)/2)):
        tickers.extend(indices.iloc[2 * i + 1, 1:-1].map(lambda x: x + ' Index').tolist())

    # Get Bloomberg data and format
    index_data = bbg.historicalRequest(tickers, "PX LAST", date_from, date_to, periodicitySelection="DAILY", \
                            nonTradingDayFillOption="NON_TRADING_WEEKDAYS", nonTradingDayFillMethod="PREVIOUS_VALUE")
    index_data = pd.pivot_table(index_data, values='bbergvalue', index=['bbergdate'], columns=['bbergsymbol'], aggfunc=np.max)
    index_data = index_data[tickers]

    # Reduce data
    if freq == 'WEEKLY':
        index_data = index_data.asfreq(freq='W', method='ffill')
    elif freq == 'MONTHLY':
        index_data = index_data.asfreq('BM')
    else:
        index_data = index_data.asfreq('B')

    # calculate returns
    index_return = np.log(index_data.astype(float)).diff().iloc[1:]
    index_return.columns = index_return.columns.str.replace(' Index', '')

    # summing up monthly
    index_return = index_return.resample('M', label='right', closed='right').sum()

    # write output to excel
    last_row = wb.sheets['ModelOutput'].range('B' + str(wb.sheets['ModelOutput'].cells.last_cell.row)).end('up').row
    wb.sheets['ModelOutput'].range("B3:Z" + str(last_row)).clear_contents()
    wb.sheets['ModelOutput'].range('rngOutput').value = index_return

    # Calculate final attribution
    _ = factor_att(workbook=wb,
                   input_data=index_return,
                   year=2020,
                   ac_weights=[0.4, 0.425, 0.175, 0, -1, 19],
                   dev_weights=[0.4, 0.425, 0.175, 0, -1, 19],
                   eafe_weights=[0.4, 0.425, 0.175, 0, -1, 19])

    return index_return
