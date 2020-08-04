def check_value(val, valid_values):
    if val not in valid_values:
        raise ValueError(f'{x} is not a valid value.'
                         f'It should be one of: {", ".join(valid_values)}')
