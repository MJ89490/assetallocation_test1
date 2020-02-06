import math
import pandas as pd
import numpy as np
import itertools as it
from pandas.tseries.offsets import BDay

def dataimport_settings (file):
    data=pd.read_excel(file+".xlsx",sheet_name="Sheet1", index_col=[0], header=0)
    return data

def discretise(data, freq):
    # Reduce frequency of a series, used to reflect weekly implementation of a strategy
    sig=pd.DataFrame()
    if freq=="monthly":
        data=data.reindex()
        rng=pd.date_range(start=data.index[0],end=data.index[-1],freq='M')
        sig=data.reindex(rng,method='pad')
    elif freq=="weekly":
        data=data.reindex()
        rng=pd.date_range(start=data.index[0],end=data.index[-1],freq='W-TUE')
        sig=data.reindex(rng,method='pad')
    elif freq=="daily":
        sig=data
    else:
        raise Exception('Frequency not supported')
    return sig

def rescale(ret,R,positioning,column,vol):
    # Calibrate series to a target volatility, uses full historic time series
    mreturn=R[column].diff(periods=21) # 24 in Octave, should be just a monthly data difference
    retscaled=ret/(mreturn.std()*math.sqrt(12))*vol
    positioningscaled=positioning/(mreturn.std()*math.sqrt(12))*vol
    Rscaled=retscaled.cumsum()
    return (retscaled, Rscaled, positioningscaled)

def returnTS(sig, future, leverage, costs, cummul):
    # Implement trading signal in a time-series context and as standalone for every series
    positioning=pd.DataFrame()
    ret=pd.DataFrame()
    R=pd.DataFrame()
    #sig=sig.reindex(future.index,method='pad').append(sig.iloc[-1])#.append(sig.iloc[-1]) # not clean, assumes last data point isn't captured by the reindex
    sig=sig.reindex(future.append(pd.DataFrame(index=future.iloc[[-1]].index+BDay(2))).index,method='pad')
    if cummul==1:
        positioning=sig.divide(future.multiply(leverage).count(axis=1),axis=0)
        positioning.iloc[-1:]=sig.iloc[-1:]/sig.iloc[-1].multiply(leverage.iloc[-1]).count()
    else:
        positioning=sig
    for column in sig:
        positioning[column]=leverage[column]*positioning[column]
        ret[column]=future[column]*positioning[column]
        # Trading costs
        ret[column].iloc[1:]=ret[column].iloc[1:]-costs[column]*pd.DataFrame.abs(positioning[column].diff(periods=1))
        R[column]=ret[column].cumsum()
    ret['Total']=ret.sum(axis=1)
    R['Total']=ret['Total'].cumsum()
    return (ret, R, positioning)

def returnXSall(sig, future, leverage, costs, cummul):
    # Implement trading signal in the cross section over all series
    positioning=pd.DataFrame()
    ret=pd.DataFrame()
    R=pd.DataFrame()
    sig=sig.reindex(future.index,method='pad').append(sig.iloc[-1]) # not clean, assumes last data point isn't captured by the reindex
    
    # Rank markets
    positioning=sig.rank(axis=1, na_option='keep')-0.5
    no_markets=positioning.count(axis=1)
    positioning=positioning.subtract(0.5*no_markets,axis=0)
    
    # Scale gross notional to be constant over time
    sum_markets=positioning.abs().sum(axis=1)
    positioning=positioning.divide(sum_markets,axis=0)

    for column in positioning:
        positioning[column]=leverage[column]*positioning[column]
        ret[column]=future[column]*positioning[column]
        # Trading costs
        ret[column].iloc[1:]=ret[column].iloc[1:]-costs[column]*pd.DataFrame.abs(positioning[column].diff(periods=1))
        R[column]=ret[column].cumsum()
    ret['Total']=ret.sum(axis=1)
    R['Total']=ret['Total'].cumsum()    
    return (ret, R, positioning)

def returnXStop(sig, future, leverage, costs, cummul, top):
    # Implement trading signal for the #top crosses
    positioning=pd.DataFrame()
    ret=pd.DataFrame()
    R=pd.DataFrame()
    sig=sig.reindex(future.index,method='pad').append(sig.iloc[-1]) # not clean, assumes last data point isn't captured by the reindex
    
    crosses=list(it.permutations(sig.columns,2))
    sig_t=pd.DataFrame()
    for x in crosses:
        # Calculate signals across all crosses
        sig_t[x]=(1+sig[x[0]])/(1+sig[x[1]])-1
    
    # Rank crosses
    pos_t=sig_t.rank(axis=1, na_option='bottom')
    # Collect top x crosses
    pos_t[pos_t <= top] = 1     
    pos_t[pos_t > top] = 0
    
    ret=0*future
    positioning=0*future
    
    for x in crosses:
        # Iterate over the long legs
        ret[x[0]]=ret[x[0]]-future[x[0]]*leverage[x[0]]*pos_t[x]
        positioning[x[0]]=positioning[x[0]]+leverage[x[0]]*pos_t[x]
        # Iterate over the short legs
        ret[x[1]]=ret[x[1]]+future[x[1]]*leverage[x[1]]*pos_t[x]
        positioning[x[1]]=positioning[x[1]]+leverage[x[1]]*pos_t[x]

    for column in sig:
        # Trading costs
        ret[column].iloc[1:]=ret[column].iloc[1:]-costs[column]*pd.DataFrame.abs(positioning[column].diff(periods=1))
        R[column]=ret[column].cumsum()
    ret['Total']=ret.sum(axis=1)
    R['Total']=ret['Total'].cumsum()    
    return (ret, R, positioning)

def returnXSblacklitterman(sig, future, leverage, costs, assets):
    positioning=future*np.NaN
    ret=pd.DataFrame()
    R=pd.DataFrame()
    
    #check if signal is lagged
    
    cov=future.ewm(alpha=.005).cov()
    assets=len(leverage.columns)
    # Risk aversion parameter - this will cancel out if the strategy is recalibrated to a vol target
    delta=2.5
    # tau is a scalar, original  BlackLitterman specification. Meucci model removes  tau but has different formulas
    tau=0.05
    w0=np.zeros((assets,1)).flatten()

    # Iterate over dates
    for i in future.index:
        # Find  markets with data
        idx=np.logical_and(leverage.loc[i].notna().values,sig.loc[i].notna().values)
        
        if sum(idx)>0:
            # Views: the value  signal  per  asset  class
            Q=sig[leverage.columns[idx]]
            Q=Q.loc[i].values.astype(np.float)
            # Volatility of the views Q
            Omega=0.1*np.eye(sum(idx))
            # Only absolute signals
            P=np.eye(sum(idx))

            #Sigma=P[:,idx]
            #Sigma=Sigma[idx,:]
            #l=leverage.iloc[-1].values.astype(np.float)
            #Sigma=P/(l[idx].T*l[idx])
            Sigma=cov.loc[i]
            Sigma=Sigma.loc[leverage.columns[idx],leverage.columns[idx]]
            Sigma=250*Sigma.values.astype(np.float)

            
            # Standard Black Litterman formulas   
            # Market returns as implied by the weights0: zero weights and zero return here
            Ret0=delta*np.matmul(Sigma,w0[idx]).flatten()

            # Expected (subjective) return and covariance matrix estimate           
            M=np.linalg.inv(np.linalg.inv(tau*Sigma)+np.matmul(P.T,np.matmul(np.linalg.inv(Omega),P)))
            SigmaExp=Sigma+M
            RetExp=np.matmul(M,(np.matmul(np.linalg.inv(tau*Sigma),Ret0)+np.matmul(P.T,np.matmul(np.linalg.inv(Omega),Q))).flatten())
            # Solve mean-variance optimisation
            positioning.loc[i,leverage.columns[idx]]=np.matmul(np.linalg.inv(delta*SigmaExp),RetExp)
    ret=positioning*future

    ret['Total']=ret.sum(axis=1)
    R['Total']=ret['Total'].cumsum()
    return(ret, R, positioning)