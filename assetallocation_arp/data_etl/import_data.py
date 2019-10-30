import pandas as pd
import assetallocation_arp.models.ARP as arp

def dataimport_future (file):
    data=pd.read_excel(file+".xlsx",sheet_name="Data", index_col=[0], header=3,skiprows=[4,5,6,7])
    data.index = pd.to_datetime(data.index, format='%d.%m.%Y %H:%M:%S')
    data["SterlingEUR"]=(1+data["Sterling"])/(1+data["Euro"])-1
    data["SkronaEUR"]=(1+data["Skrona"])/(1+data["Euro"])-1
    data["NokronaEUR"]=(1+data["Nokrona"])/(1+data["Euro"])-1
    data["SwissFrancEUR"]=(1+data["SwissFranc"])/(1+data["Euro"])-1 
    return data

def dataimport_index (file):
    data=pd.read_excel(file+".xlsx",sheet_name="Data1", index_col=None, header=1,skiprows=[2,3,4],usecols=[0]+list(range(1,60,4)))
    data2=pd.read_excel(file+".xlsx",sheet_name="Data2", index_col=None, header=1,skiprows=[2,3,4],usecols=list(range(0,64,4)))
    data3=pd.read_excel(file+".xlsx",sheet_name="Data3", index_col=None, header=1,skiprows=[2,3,4],usecols=list(range(0,60,4)))
    data=pd.concat([data, data2, data3], axis=1)
    data.index = pd.to_datetime(data['Index'], format='%Y-%m-%d')
    data=data.drop('Index',axis=1)
    data["SterlingEUR"]=data["Sterling"]/data["Euro"]
    data["SkronaEUR"]=data["Skrona"]/1+data["Euro"]
    data["NokronaEUR"]=data["Nokrona"]/data["Euro"]
    data["SwissFrancEUR"]=data["SwissFranc"]/data["Euro"]
    return data

def dataimport_CARRY (file):
    data=pd.read_excel(file+".xlsx",sheet_name="Data1", index_col=None, header=1,skiprows=[2,3,4],usecols=[0]+list(range(3,60,4)))
    data2=pd.read_excel(file+".xlsx",sheet_name="Data2", index_col=None, header=1,skiprows=[2,3,4],usecols=list(range(2,64,4)))
    data3=pd.read_excel(file+".xlsx",sheet_name="Data3", index_col=None, header=1,skiprows=[2,3,4],usecols=list(range(2,60,4)))
    data=pd.concat([data, data2, data3], axis=1)
    data.index  = pd.to_datetime(data['Index'], format='%Y-%m-%d')
    data=data.drop('Index',axis=1)
    data.columns=[x[:-2] for x in data.columns]
    return data

def dataimport_VALUE (file):
    data=pd.read_excel(file+".xlsx",sheet_name="Data1", index_col=None, header=1,skiprows=[2,3,4],usecols=[0]+list(range(4,60,4)))
    data2=pd.read_excel(file+".xlsx",sheet_name="Data2", index_col=None, header=1,skiprows=[2,3,4],usecols=list(range(3,64,4)))
    data3=pd.read_excel(file+".xlsx",sheet_name="Data3", index_col=None, header=1,skiprows=[2,3,4],usecols=list(range(3,60,4)))
    data=pd.concat([data, data2, data3], axis=1)
    data.index = pd.to_datetime(data['Index'], format='%Y-%m-%d')
    data=data.drop('Index',axis=1)
    data.columns=[x[:-2] for x in data.columns]
    return data

def dataimport_FICarry (file,market):
    data=pd.read_excel(file+".xlsx",sheet_name=market, index_col=None, header=12,skiprows=[13])
    data.index = pd.to_datetime(data['Index'], format='%Y-%m-%d')
    data=data.drop('Index',axis=1)
    return data

def dataimport_FR (file):
    data=pd.read_excel(file+".xlsx",sheet_name="Sheet1", index_col=[0], header=0)
    data.index = pd.to_datetime(data.index, format='%d.%m.%Y %H:%M:%S')
    return data

def datacheck (future,file,diff):
    # Check missing data and repeated numbers for last 20 days
    print("Missing data")
    print("**********************************")
    test=future.iloc[-15:]
    for column in test:
        if len(test[test[column].isnull()][column])>0:
                print(test[test[column].isnull()][column])
    print("")
    print("Stale data") 
    print("**********************************")
    test=future-future.diff(periods=1)[-15:]
    for column in test:
        if len(test[(test[column]==0)][column])>0:
            print(test[(test[column]==0)][column])
    print("")    
    
    # Check for outliers (>2 stdev)
    print("Outliers")
    print("**********************************")
    if diff:
        test=test.diff(periods=1)
    else:
        test=future
    test=test.iloc[-15:]/test.std(axis=0)
    test=test[((test<-2) | (test>2))]
    for column in test:
        if len(test[test[column].notnull()][column])>0:
            print(test[test[column].notnull()][column])
    print("")
    
    # Check for data revisions (>0.5stdev compared to historic data)
    print("Data revisions")
    print("**********************************")
    test=pd.read_pickle(file+".pkl")
    test=(test-future)/future.std(axis=0)
    test=test[((test<-0.2) | (test>0.2))]
    for column in test:
        if len(test[test[column].notnull()][column])>0:
            print(test[test[column].notnull()][column])


future=dataimport_future("Future data")
datacheck(future,"Future data",False)
accept_data = input('Accept updated data? (y/n): ')
if accept_data=='y':
    future.to_pickle("Future data.pkl")
    print('Future data imported')
else:
    print('Future data NOT imported')

index=dataimport_index("Data")
datacheck(index,"Data",True)
accept_data = input('Accept updated data? (y/n): ')
if accept_data=='y':
    index.to_pickle("Data.pkl")
    print('Index data imported')
else:
    print('Index data NOT imported')
    
settings=arp.dataimport_settings("Settings")
#settings.to_pickle("Settings.pkl")

