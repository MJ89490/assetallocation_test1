# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 11:07:38 2019

@author: SP99914
"""


def func():
    import scipy.io as spio
    import numpy as np
    import pandas as pd
    import time
    from datetime import date
    import xlrd
    import math
    import xlwings as xw
    import pickle

    starttime = time.time()

    # Paramters for data

    location = r'\\inv\lgim\FrontOffice\Structured Products\Solutions Group\SIRM\Shared\Siddhi\EFFECT\effect3.xlsm'
    location2 = r'\\inv\lgim\FrontOffice\Structured Products\Solutions Group\SIRM\Shared\Siddhi\EFFECT\Inflation estimate.xlsm'
    pickleLoc1 = r'\\inv\lgim\FrontOffice\Structured Products\Solutions Group\SIRM\Shared\Siddhi\EFFECT\masterDfCurrent.pkl'
    pickleLoc2 = r'\\inv\lgim\FrontOffice\Structured Products\Solutions Group\SIRM\Shared\Siddhi\EFFECT\masterDfFuture.pkl'
    book = xlrd.open_workbook(location)
    book2 = xlrd.open_workbook(location2)
    InfSheets = book2.sheet_names()
    indexNos2 = []
    for q in InfSheets:
        if q == "Sheet1" or q == "Sheet2" or q == "IMF Publish":
            indexNos = InfSheets.index(q)
            indexNos2.append(indexNos)
    InfDataSheet = [i for j, i in enumerate(InfSheets) if j not in indexNos2]
    infData2 = pd.read_excel(location2, sheet_name=InfDataSheet)
    realTimeList = pd.read_excel(location, sheet_name='Parameters', skiprows=3, usecols=[13, 14],
                                 header=None).dropna().reset_index(drop=True)
    realTimeList.columns = range(realTimeList.shape[1])
    first_sheet = book.sheet_by_name('Parameters')
    shortMA = int(first_sheet.cell(8, 1).value)
    longMA = int(first_sheet.cell(9, 1).value)
    TrendIndval = first_sheet.cell(7, 1).value
    avgdatapoint = shortMA
    CarryType = first_sheet.cell(16, 1).value
    weekcalc = (52 / 10)
    totalMonths = 12
    cutoff = float(first_sheet.cell(14, 1).value)
    cutoffs = float(first_sheet.cell(15, 1).value)
    incl_shorts = first_sheet.cell(11, 1).value
    closingthresh = float(first_sheet.cell(19, 1).value)
    comboT = cutoff - closingthresh
    combosT = cutoffs + closingthresh
    startDate = first_sheet.cell(4, 1).value
    realTimeInf = first_sheet.cell(18, 1).value
    bidAsk = first_sheet.cell(26, 1).value
    stdDevWindow = int(first_sheet.cell(23, 1).value)
    riskWeight = first_sheet.cell(22, 1).value

    df1 = pd.read_excel(location, sheet_name="Parameters", skiprows=3, usecols=[7, 9, 10, 11])
    regionSplit = df1['Region'].dropna().tolist()
    Curncylist = df1['Curncy'].dropna().unique().tolist()
    # Including Spot
    incl_spot = " Curncy"
    spotList = [s + incl_spot for s in Curncylist]
    # Including Carry
    incl_carry = "CR Curncy"
    carryList = [x + incl_carry for x in Curncylist]
    # Main 3M implied
    NDFlist = df1['NDF?'].dropna().tolist()
    incl_3M = 'I3M Curncy'
    main3M = [x + incl_3M for x in NDFlist]
    # Base 3M implied
    baselist = df1['Base currency'].dropna().tolist()
    baselistMain = ['US' if r == 'USD' else r for r in baselist]
    base_3M = "0003M Curncy"
    base3M = [x + base_3M for x in baselistMain]
    base3M = ['US0003M Index' if t == 'US0003M Curncy' else t for t in base3M]
    base3M = ['EUR003M Curncy' if w == 'EUR0003M Curncy' else w for w in base3M]
    masterList = base3M + main3M + carryList + spotList

    # the +1 is temporary for curncyNumber as COP isn't in currency list for now (for Attribution purpose)

    curncyNumber = len(Curncylist) + 1

    z = spio.loadmat(
        r'\\inv\lgim\FrontOffice\Structured Products\Solutions Group\SIRM\Shared\Simone\ARP\Data\matlabData.mat')
    b = z['dataTable']
    a = z['updatedInstruments']
    c = z['dates']
    c = pd.DataFrame(c)
    c = c.iloc[:, 0].apply(lambda x: xlrd.xldate_as_datetime(x, book.datemode))
    c = pd.DataFrame({'Date': c})
    c['Date'] = pd.to_datetime(c['Date'])
    b = pd.DataFrame(b)
    a = pd.DataFrame(a)
    a = a.iloc[:, 2].str.get(0)
    a = a.tolist()
    a = a[1:]
    tickerList = a
    b.columns = a
    EffectData = b
    EffectData = pd.concat([EffectData, c], axis=1)
    EffectData.set_index('Date', inplace=True)

    startDate2 = xlrd.xldate_as_datetime(startDate, book.datemode)
    c = c['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    c3 = pd.Index(list(c))
    startIndexNo = c3.get_loc(startDate2.strftime('%Y-%m-%d'))

    # Converting to Weekly frequency

    if startDate == float(36164):
        xyz = 'W-MON'
    elif startDate == float(36165):
        xyz = 'W-TUE'
    elif startDate == float(36166):
        xyz = 'W-WED'
    elif startDate == float(36167):
        xyz = 'W-THU'
    elif startDate == float(36168):
        xyz = 'W-FRI'

    weeklyFreq = pd.date_range(start=EffectData.index[startIndexNo], end=EffectData.index[-1], freq=xyz)
    weeklyFreq = pd.DataFrame({'Date': list(weeklyFreq)})
    weeklyData = EffectData.merge(weeklyFreq, on='Date')
    weeklyData.set_index('Date', inplace=True)
    monthlyFreq = pd.date_range(start=weeklyFreq['Date'][stdDevWindow], end=weeklyFreq['Date'][len(weeklyFreq) - 1],
                                freq='M')
    monthlyFreq = pd.DataFrame({'Date': list(monthlyFreq)})

    dateList = pd.DataFrame({'Date': list(weeklyData.index)})
    realTimeList = realTimeList.rename(columns={0: 'Date'})
    infRelease = pd.merge_asof(dateList, realTimeList, on='Date', allow_exact_matches=True)
    infRelease[1] = infRelease[1].shift(1, axis=0).fillna("Latest")
    infRelease = infRelease.rename(columns={1: 'InfTimePeriod'})
    Curncylist3 = [x[:3] for x in Curncylist]
    baseNameUnique = np.unique(baselist).tolist()
    Curncylist2 = Curncylist3 + baseNameUnique
    emptyDf = pd.DataFrame(columns=Curncylist2)
    mainDf1 = pd.concat([infRelease, emptyDf], axis=1)
    # Current Year
    currentYear = pd.Series(weeklyData.index.year).rename("currentYear")
    currentYear = currentYear.shift(1, axis=0)
    masterDfCurrent = pd.concat([currentYear, mainDf1], axis=1).drop(columns=['Date'])
    # Future Year
    futureYear = currentYear + 1
    futureYear = futureYear.rename("futureYear")
    masterDfFuture = pd.concat([futureYear, mainDf1], axis=1).drop(columns=['Date'])

    if realTimeInf == "Yes":

        # if startDate == float(36166) and len(Curncylist) == 17:
        #
        #     pickle_in1 = open(pickleLoc1, 'rb')
        #     pickle_in2 = open(pickleLoc2, 'rb')
        #     masterDfCurrent = pickle.load(pickle_in1)
        #     masterDfFuture = pickle.load(pickle_in2)
        #
        # else:
        #
        #     totalRows = masterDfCurrent.shape[0]
        #     for g in emptyDf.columns:
        #         colNo = masterDfCurrent.columns.get_loc(g)
        #         for h in range(1, totalRows):
        #             dataType = infData2.get(masterDfCurrent.iloc[h, 1])
        #             colLocInf = dataType.columns.get_loc(g)
        #             rowLocInf1 = pd.Index(dataType['Date']).get_loc(masterDfCurrent.iloc[h, 0])
        #             rowLocInf2 = pd.Index(dataType['Date']).get_loc(masterDfFuture.iloc[h, 0])
        #             masterDfCurrent.iloc[h, colNo] = dataType.iloc[rowLocInf1, colLocInf]
        #             masterDfFuture.iloc[h, colNo] = dataType.iloc[rowLocInf2, colLocInf]
        #             output1 = open(pickleLoc1, 'wb')
        #             output2 = open(pickleLoc2, 'wb')
        #             pickle.dump(masterDfCurrent, output1)
        #             pickle.dump(masterDfFuture, output2)
        #             output1.close()
        #             output2.close()
        #             pickle_in1 = open(pickleLoc1, 'rb')
        #             pickle_in2 = open(pickleLoc2, 'rb')
        #             masterDfCurrent = pickle.load(pickle_in1)
        #             masterDfFuture = pickle.load(pickle_in2)

        carry = []
        trend = []
        signal = []
        returns = []
        returns2 = []
        spotxcosts = []
        spotcosts = []
        sigTR = []
        sigSR = []
        inverseVolatility = []
        sigTRLn = []
        attribution = []

        m = len(Curncylist)
        n = len(Curncylist)

        for i in range(m):

            curncyData = []
            curncyData.append([Curncylist[i][:3], masterList[i], masterList[i + n], masterList[(2 * (i + n)) - i],
                               masterList[(3 * (i + n)) - (i * 2)]])
            curncyData = curncyData[0]
            curncyName = curncyData[0]
            baseName = baselist[i]
            spotRate2 = weeklyData.iloc[:, weeklyData.columns.get_loc(curncyData[4])]
            carryRate2 = weeklyData.iloc[:, weeklyData.columns.get_loc(curncyData[3])]
            NDF3MRate2 = weeklyData.iloc[:, weeklyData.columns.get_loc(curncyData[2])]
            base3MRate2 = weeklyData.iloc[:, weeklyData.columns.get_loc(curncyData[1])]
            spotRate = spotRate2.shift(1, axis=0)
            carryRate = carryRate2.shift(1, axis=0)
            NDF3MRate = NDF3MRate2.shift(1, axis=0)
            base3MRate = base3MRate2.shift(1, axis=0)

            # Trend calculation

            if TrendIndval == "Spot":

                shortrolling = pd.Series(spotRate).rolling(shortMA).mean()
                longrolling = pd.Series(spotRate).rolling(longMA).mean()
                trendval = (shortrolling / longrolling) - 1

            elif TrendIndval == "Total Return":

                shortrolling = pd.Series(carryRate).rolling(shortMA).mean()
                longrolling = pd.Series(carryRate).rolling(longMA).mean()
                trendval = (shortrolling / longrolling) - 1

                trend.append(trendval)

            # Inflation Differential calculation

            monthData = weeklyData.index.month
            monthData = pd.Series(monthData)
            yearData = weeklyData.index.year
            yearData = pd.Series(yearData).shift(1, axis=0)
            yearDataDf = pd.DataFrame(yearData)
            futYearData = yearData + 1
            futYearData = pd.DataFrame(futYearData)

            laggedmonthdata = monthData.shift(1, axis=0)

            monthsleft = (12 - laggedmonthdata) / 12
            monthscomplete = laggedmonthdata / 12

            if realTimeInf == "No":

                InfData = infData2.get("Latest")

                lookuplist = InfData[['Date', curncyName]]
                infRateP = lookuplist.merge(yearDataDf, on='Date')
                infRateF = lookuplist.merge(futYearData, on='Date')
                infRateP = pd.Series(infRateP[curncyName])
                infRateF = pd.Series(infRateF[curncyName])

                lookupbase = InfData[['Date', baseName]]
                baseRateP = lookupbase.merge(yearDataDf, on='Date')
                baseRateF = lookupbase.merge(futYearData, on='Date')
                baseRateP = pd.Series(baseRateP[baseName])
                baseRateF = pd.Series(baseRateF[baseName])

            elif realTimeInf == "Yes":

                infRateP = masterDfCurrent[curncyName[:3]]
                infRateF = masterDfFuture[curncyName[:3]]
                baseRateP = masterDfCurrent[baseName]
                baseRateF = masterDfFuture[baseName]

                mainc = (monthsleft * infRateP) + (monthscomplete * infRateF)
                basec = (monthsleft * baseRateP) + (monthscomplete * baseRateF)

                InfDiff = (mainc - basec) / 100

                InfDiffDates = pd.DataFrame({'Date': list(weeklyData.index)})
                InfDiff = pd.concat([InfDiffDates, InfDiff], axis=1)
                InfDiff.set_index('Date', inplace=True)




if __name__ == "__main__":
    func()