import pandas as pd


class Currencies:

    def __init__(self):
        self.currencies_usd = {}
        self.currencies_eur = {}

    def currencies_data(self):

        self.currencies_usd = {
                                "currencies_usd_tickers": ["BRLUSD Curncy", "BRLUSDCR Curncy", "BCNI3M Curncy", "US0003M Index",
                                                           "ARSUSD Curncy", "ARSUSDCR Curncy", "APNI3M Curncy",
                                                           "MXNUSD Curncy", "MXNUSDCR Curncy", "MXNI3M Curncy",
                                                           "COPUSD Curncy", "COPUSDCR Curncy", "CLNI3M Curncy",
                                                           "CLPUSD Curncy", "CLPUSDCR Curncy", "CHNI3M Curncy",
                                                           "PENUSD Curncy", "PENUSDCR Curncy", "PSNI3M Curncy",
                                                           "TRYUSD Curncy", "TRYUSDCR Curncy", "TRYI3M Curncy",
                                                           "RUBUSD Curncy", "RUBUSDCR Curncy", "RUBI3M Curncy",
                                                           "ZARUSD Curncy", "ZARUSDCR Curncy", "ZARI3M Curncy",
                                                           "CNYUSD Curncy", "CNYUSDCR Curncy", "CCNI3M Curncy",
                                                           "KRWUSD Curncy", "KRWUSDCR Curncy", "KWNI3M Curncy",
                                                           "MYRUSD Curncy", "MYRUSDCR Curncy", "MRNI3M Curncy",
                                                           "IDRUSD Curncy", "IDRUSDCR Curncy", "IHNI3M Curncy",
                                                           "INRUSD Curncy", "INRUSDCR Curncy", "IRNI3M Curncy",
                                                           "PHPUSD Curncy", "PHPUSDCR Curncy", "PPNI3M Curncy",
                                                           "TWDUSD Curncy", "TWDUSDCR Curncy", "NTNI3M Curncy",
                                                           "THBUSD Curncy", "THBUSDCR Curncy", "THBI3M Curncy",
                                                           ]
                              }

        self.currencies_eur = {
                                "currencies_eur_tickers": ["CZKEUR Curncy", "CZKEURCR Curncy", "CZKI3M Curncy", "EUR003M Curncy",
                                                           "HUFEUR Curncy", "HUFEURCR Curncy", "HUFI3M Curncy",
                                                           "PLNEUR Curncy", "PLNEURCR Curncy", "PLNI3M Curncy"
                                                           ]

                               }
        return pd.DataFrame(self.currencies_usd), pd.DataFrame(self.currencies_eur)



