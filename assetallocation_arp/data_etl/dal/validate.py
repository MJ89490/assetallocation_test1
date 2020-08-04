def validate_enum(val, valid_vals):
    if val not in valid_vals:
        raise ValueError(f'{x} is not a valid value.'
                         f'It should be one of: {", ".join(valid_vals}}')
