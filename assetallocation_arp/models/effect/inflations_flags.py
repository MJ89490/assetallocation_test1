
import pandas as pd

def inflation_release():

    imf_weo = ['Apr2006', 'Sep2006']

    weo = pd.DataFrame(imf_weo, index=['19/04/2006', '14/09/2006'])

    weo.index = pd.to_datetime(weo.index)

    weo.loc['19/04/2006']
    print()

if __name__=="__main__":
    inflation_release()





