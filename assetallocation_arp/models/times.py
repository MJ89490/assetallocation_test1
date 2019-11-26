import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

import assetallocation_arp.models.ARP as arp

#testing the git commit
# Parameters
TIMES_LAG=3
settings=arp.dataimport_settings("Settings")

# Change the universe of markets that is being used
markets="Leverage_MATR"  # All "Leverage_all_markets" / Minimalist "Leverage_min"
# Leverage/scaling of individual markets
sleverage ="v"           #Equal(e) / Normative(n) / Volatility(v) / Standalone(s)

def signal (index):
    sig=pd.DataFrame()
    for column in index:
        sig1= index[column].ewm(alpha=2/15).mean()/index[column].ewm(alpha=2/30).mean()-1
        sig2= index[column].ewm(alpha=2/30).mean()/index[column].ewm(alpha=2/60).mean()-1
        sig3= index[column].ewm(alpha=2/60).mean()/index[column].ewm(alpha=2/120).mean()-1
    
        #sig[column]=(sig1/sig1.ewm(alpha=1/30).std()+sig2/sig2.ewm(alpha=1/30).std()+sig3/sig3.ewm(alpha=1/30).std())/3
        sig[column]=(sig1/sig1.rolling(window=90).std()+sig2/sig2.rolling(window=90).std()+sig3/sig3.rolling(window=90).std())/3
        # S-curve cut out for large movement, alternative curve without cutoff: sig[column]=2/(1+math.exp(-2*sig[column]))-1
        sig[column]=sig[column]*np.exp(-1*sig[column].pow(2)/6)/(math.sqrt(3)*math.exp(-0.5))
    sig=arp.discretise(sig,"weekly")
    sig=sig.shift(TIMES_LAG,freq="D")
    return sig


# Import data
future=pd.read_pickle("Future data.pkl")
index=pd.read_pickle("Data.pkl")

sig=signal(index)
costs=settings.loc["Costs"]
marketselect=settings.loc[markets]

if sleverage=='e' or sleverage=='s':
    leverage=0*future+1
    leverage[marketselect.index[marketselect>0]]=1
elif sleverage=='n':
    leverage=0*future+marketselect
elif sleverage=='v':
    leverage=1/future.ewm(alpha=1/150, min_periods=10).std()
else:
    raise Exception('Invalid entry')
leverage[marketselect.index[marketselect.isnull()]] = np.nan
leverage=leverage.shift(periods=TIMES_LAG, freq='D', axis=0).reindex(future.append(sig.iloc[-1]).index,method='pad')

if sleverage=='s':
    (ret, R, positioning)=arp.returnTS(sig,future,leverage,0*costs,0)
    ret1=ret
    R1=R
    positioning1=positioning
else:
    (ret, R, positioning)=arp.returnTS(sig,future,leverage,0*costs,1)
    (ret1, R1, positioning1)=arp.rescale(ret,R,positioning,"Total",0.01)

# Add more markets manually if we have more equity markets
averageEquityAllocation = (sig['S&P 500'] + sig['Euro Stoxx 50'] + sig['Nikkei 225'] + sig['Hang Seng'])/4
averageBondAllocation = (sig['Treasury'] + sig['Gilt'] + sig['Bund'] + sig['Cad10'])/4

print(positioning1.iloc[-1])

# Plotting average equity allocation
pltAverageEquityAllocation = plt.subplots(figsize=(6, 5))
pltAverageEquityAllocation = averageEquityAllocation.iloc[-150:].plot(title='Average alloc. to S&P 500, EuroStoxx 50, Nikkei 225, Hang Seng', ylim=(-1,1))
pltAverageEquityAllocation.axes.axhline(y=0.85, color='r')
pltAverageEquityAllocation.axes.axhline(y=-0.85, color='r')
plt.show()

# Plotting average bond allocation
pltAverageBondAllocation = plt.subplots(figsize=(6, 5))
pltAverageBondAllocation = averageBondAllocation.iloc[-150:].plot(title='Average alloc. to Treasury, Gilt, Bund, CAD10', ylim=(-1,1))
pltAverageBondAllocation.axes.axhline(y=0.85, color='r')
pltAverageBondAllocation.axes.axhline(y=-0.85, color='r')
plt.show()
