import enum


class CurrencySpot(enum.Enum):
    """
    Enum class which creates a list of currencies names for the spot
    """

    BRLUSD = "BRLUSD Curncy"
    ARSUSD = "ARSUSD Curncy"
    MXNUSD = "MXNUSD Curncy"
    COPUSD = "COPUSD Curncy"
    CLPUSD = "CLPUSD Curncy"
    PENUSD = "PENUSD Curncy"
    TRYUSD = "TRYUSD Curncy"
    RUBUSD = "RUBUSD Curncy"
    ZARUSD = "ZARUSD Curncy"
    CNYUSD = "CNYUSD Curncy"
    KRWUSD = "KRWUSD Curncy"
    MYRUSD = "MYRUSD Curncy"
    IDRUSD = "IDRUSD Curncy"
    INRUSD = "INRUSD Curncy"
    PHPUSD = "PHPUSD Curncy"
    TWDUSD = "TWDUSD Curncy"
    THBUSD = "THBUSD Curncy"
    CZKEUR = "CZKEUR Curncy"
    HUFEUR = "HUFEUR Curncy"
    PLNEUR = "PLNEUR Curncy"


class CurrencyBaseSpot(enum.Enum):
    """
    Enum class which creates a list of base names currencies
    """
    USD = 'USD'
    EUR = 'EUR'
    USD_Base = 'USD_Base'
    EUR_Base = 'EUR_Base'

