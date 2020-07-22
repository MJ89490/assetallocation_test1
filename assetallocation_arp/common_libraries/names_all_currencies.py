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




from data_etl.inputs_effect.import_process_data_effect import ProcessDataEffect


def test():

    obj_import_data_times = ProcessDataEffect()

    config_data = obj_import_data_times.parse_data_config_effect()

    s = list(zip(config_data['spot_config'].values()))


if __name__ == "__main__":
    test()
