from models.effect.import_data_effect import ImportDataEffect
from models.effect.constants_currencies import Currencies
import pandas as pd

class DataProcessingEffect(ImportDataEffect):

    def __init__(self):
        super().__init__()
        self.data_currencies_usd = pd.DataFrame()
        self.data_currencies_eur = pd.DataFrame()

    def data_processing_effect(self):

        obj_currencies = Currencies()
        currencies_usd, currencies_eur = obj_currencies.currencies_data()

        # start_date = '1999-01-06'
        self.data_currencies_usd = self.data_currencies[currencies_usd.currencies_usd_tickers].loc[:]
        self.data_currencies_eur = self.data_currencies[currencies_eur.currencies_eur_tickers].loc[:]