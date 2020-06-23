from common_libraries.names_currencies_spot import CurrencySpot
from common_libraries.names_currencies_carry import CurrencyCarry
from common_libraries.names_currencies_implied import CurrencyImplied
from common_libraries.constants_currencies import Currencies

CURRENCIES_SPOT = [currency.value for currency in CurrencySpot]
CURRENCIES_IMPLIED = [currency.value for currency in CurrencyImplied]
CURRENCIES_CARRY = [currency.value for currency in CurrencyCarry]

# def t():
#     obj_currencies = Currencies()
#     currency_usd, currency_eur = obj_currencies.currencies_data()
#     CURRENCIES_USD = [currency for currency in currency_usd.loc[0].tolist()]
#     CURRENCIES_EUR = [currency for currency in currency_eur.loc[0].tolist()]
#
# if __name__ == "__main__":
#     t()