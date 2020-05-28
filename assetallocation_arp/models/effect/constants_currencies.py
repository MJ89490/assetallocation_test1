import pandas as pd


class Currencies:

    def __init__(self):
        self.currencies_usd = {}
        self.currencies_eur = {}

    def currencies_data(self):

        self.currencies_usd = {
                                "currencies_usd_tickers": ["BRLUSD Curncy", "BRLUSDCR Curncy", "BCNI3M Curncy", "US0003M Index",
                                                           "ARSUSD Curncy", "ARSUSDCR Curncy", "APNI3M Curncy", "US0003M Index",
                                                           "MXNUSD Curncy", "MXNUSDCR Curncy", "MXNI3M Curncy", "US0003M Index",
                                                           "COPUSD Curncy", "COPUSDCR Curncy", "CLNI3M Curncy", "US0003M Index",
                                                           "CLPUSD Curncy", "CLPUSDCR Curncy", "CHNI3M Curncy", "US0003M Index",
                                                           "PENUSD Curncy", "PENUSDCR Curncy", "PSNI3M Curncy", "US0003M Index",
                                                           "TRYUSD Curncy", "TRYUSDCR Curncy", "TRYI3M Curncy", "US0003M Index",
                                                           "RUBUSD Curncy", "RUBUSDCR Curncy", "RUBI3M Curncy", "US0003M Index",
                                                           "ZARUSD Curncy", "ZARUSDCR Curncy", "ZARI3M Curncy", "US0003M Index",
                                                           "CNYUSD Curncy", "CNYUSDCR Curncy", "CCNI3M Curncy", "US0003M Index",
                                                           "KRWUSD Curncy", "KRWUSDCR Curncy", "KWNI3M Curncy", "US0003M Index",
                                                           "MYRUSD Curncy", "MYRUSDCR Curncy", "MRNI3M Curncy", "US0003M Index",
                                                           "IDRUSD Curncy", "IDRUSDCR Curncy", "IHNI3M Curncy", "US0003M Index",
                                                           "INRUSD Curncy", "INRUSDCR Curncy", "IRNI3M Curncy", "US0003M Index",
                                                           "PHPUSD Curncy", "PHPUSDCR Curncy", "PPNI3M Curncy", "US0003M Index",
                                                           "TWDUSD Curncy", "TWDUSDCR Curncy", "NTNI3M Curncy", "US0003M Index",
                                                           "THBUSD Curncy", "THBUSDCR Curncy", "THBI3M Curncy", "US0003M Index"
                                                           ]
                              }

        self.currencies_eur = {
                                "currencies_eur_tickers": ["CZKEUR Curncy", "CZKEURCR Curncy", "CZKI3M Curncy", "EUR0003M Index",
                                                           "HUFEUR Curncy", "HUFEURCR Curncy", "HUFI3M Curncy", "EUR0003M Index",
                                                           "PLNEUR Curncy", "PLNEURCR Curncy", "PLNI3M Curncy", "EUR0003M Index"
                                                           ]

                               }
        return pd.DataFrame(self.currencies_usd), pd.DataFrame(self.currencies_eur)


