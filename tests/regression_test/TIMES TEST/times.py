import pandas as pd
import numpy as np
import math
from pandas.tseries.offsets import BDay

import ARP as arp

# Parameters
TIMES_LAG = 2
settings = arp.dataimport_settings("Settings")

# Change the universe of markets that is being used
markets="Leverage_MATR"  # All "Leverage_all_markets" / Minimalist "Leverage_min"
# Leverage/scaling of individual markets
sleverage ="v"           #Equal(e) / Normative(n) / Volatility(v) / Standalone(s)

def signal (index):
    sig = pd.DataFrame()
    for column in index:
        sig1 = index[column].ewm(alpha=2/15).mean()/index[column].ewm(alpha=2/30).mean()-1
        sig2 = index[column].ewm(alpha=2/30).mean()/index[column].ewm(alpha=2/60).mean()-1
        sig3 = index[column].ewm(alpha=2/60).mean()/index[column].ewm(alpha=2/120).mean()-1
        sig[column] = (sig1/sig1.rolling(window=90).std()+sig2/sig2.rolling(window=90).std()+sig3/sig3.rolling(window=90).std())/3
        sig[column] = sig[column]*np.exp(-1*sig[column].pow(2)/6)/(math.sqrt(3)*math.exp(-0.5))
    sig = arp.discretise(sig, "weekly")
    sig = sig.shift(TIMES_LAG, freq="D")
    return sig


# Import data
future = pd.read_pickle("Future data.pkl")
index = pd.read_pickle("Data.pkl")
series = ["S&P 500",	"Euro Stoxx 50",	"Nikkei 225",	"Hang Seng",	"Treasury",	"Gilt",	"Bund",	"Cad10",	"Yen",	"Euro",	"Aus",	"CanDollar", "Sterling"]

data = pd.read_pickle("Data.pkl")

future = future[series]
index = index[series]
 
sig = signal(index)
costs = settings.loc["Costs"]
marketselect = settings.loc[markets]

if sleverage == 'e' or sleverage == 's':
    leverage = 0*future+1
    leverage[marketselect.index[marketselect > 0]] = 1
elif sleverage == 'n':
    leverage = 0*future+marketselect
elif sleverage == 'v':
    leverage=1/future.ewm(alpha=1/150, min_periods=10).std()
else:
    raise Exception('Invalid entry')
leverage[marketselect.index[marketselect.isnull()]] = np.nan
leverage = leverage.shift(periods=TIMES_LAG, freq='D', axis=0).reindex(future.append(pd.DataFrame(index=future.iloc[[-1]].index+BDay(2))).index,method='pad')

if sleverage == 's':
    (ret, R, positioning) = arp.returnTS(sig, future, leverage, 0*costs, 0)
    ret1 = ret
    R1 = R
    positioning1 = positioning
else:
    (ret, R, positioning) = arp.returnTS(sig, future, leverage, 0*costs, 1)
    (ret1, R1, positioning1) = arp.rescale(ret, R, positioning, "Total", 0.01)

    # import data to csv files
    ret1.to_csv('ret1_old', encoding='utf-8', index=False)
    R1.to_csv('R1_old', encoding='utf-8', index=False)
    positioning1.to_csv('positioning1_old', encoding='utf-8', index=False)
    sig.to_csv('signals_old', encoding='utf-8', index=False)


