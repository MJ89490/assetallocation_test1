from common_libraries.names_currencies_spot import CurrencySpot
from common_libraries.names_currencies_carry import CurrencyCarry
from common_libraries.names_currencies_implied import CurrencyImplied

CURRENCIES_SPOT = [currency.value for currency in CurrencySpot]
CURRENCIES_IMPLIED = [currency.value for currency in CurrencyImplied]
CURRENCIES_CARRY = [currency.value for currency in CurrencyCarry]