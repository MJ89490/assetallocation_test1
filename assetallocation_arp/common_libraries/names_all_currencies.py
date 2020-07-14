from common_libraries.names_currencies_spot import CurrencySpot
from common_libraries.names_currencies_carry import CurrencyCarry
from common_libraries.names_currencies_implied import CurrencyImplied
from common_libraries.names_all_currencies_data import Currencies

CURRENCIES_SPOT = [currency.value for currency in CurrencySpot]
CURRENCIES_IMPLIED = [currency.value for currency in CurrencyImplied]
CURRENCIES_CARRY = [currency.value for currency in CurrencyCarry]

obj_currencies = Currencies()
currency_usd, currency_eur = obj_currencies.currencies_data()
CURRENCIES_USD = currency_usd.loc[:, "currencies_usd_tickers"].tolist()
CURRENCIES_EUR = currency_eur.loc[:, "currencies_eur_tickers"].tolist()

