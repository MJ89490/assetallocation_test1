from data_etl.inputs_effect.import_process_data_effect import ProcessDataEffect

# -------------------------------------- Spot Carry and 3M implied Data lists ---------------------------------------- #
obj_import_data_times = ProcessDataEffect()

config_data = obj_import_data_times.parse_data_config_effect()

# Spot, Carry and 3M implied have the same length
length = len(config_data['spot_config'].values())

spot_config = list(config_data['spot_config'].values())
carry_config = list(config_data['carry_config'].values())
three_month_implied_config = list(config_data['3M_implied_config'].values())

CURRENCIES_SPOT, CURRENCIES_CARRY, CURRENCIES_IMPLIED = [], [], []

for item in range(length):
    length_tmp = len(spot_config[item])
    for name in range(length_tmp):
        CURRENCIES_SPOT.append(spot_config[item][name])
        CURRENCIES_CARRY.append(carry_config[item][name])
        CURRENCIES_IMPLIED.append(three_month_implied_config[item][name])

# -------------------------------------- Base Implied Data list ------------------------------------------------------ #
CURRENCIES_USD = config_data['spot_config']['currencies_spot_usd']
CURRENCIES_EUR = config_data['spot_config']['currencies_spot_eur']
