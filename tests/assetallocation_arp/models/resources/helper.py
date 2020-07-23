from pathlib import Path
from typing import Dict, Any
import os

import pandas as pd


def save_inputs_outputs(test_dir: Path):
    def decorator(func):
        def wrapper(**kwargs):
            if not os.path.exists(str(test_dir)):
                os.mkdir(str(test_dir))

            for k, v in kwargs.items():
                write_to_csv(v, k, test_dir, 'in')

            out = func(**kwargs)
            if isinstance(out, tuple):
                for counter, v in enumerate(out):
                    write_to_csv(v, counter, test_dir, 'out')

            else:
                write_to_csv(out, 0, test_dir, 'out')

            return out

        return wrapper
    return decorator


def write_to_csv(value, name, test_dir, prefix):
    if isinstance(value, pd.DataFrame) or isinstance(value, pd.Series):
        value.to_csv(test_dir / f'{prefix}_{name}.csv')

    else:
        pd.DataFrame([[value]]).to_csv(test_dir / f'{prefix}_{name}_scalar.csv')


def read_inputs_outputs(test_dir: Path):
    inputs = dict()
    outputs = dict()

    for f in test_dir.iterdir():
        if f.name.endswith('scalar.csv'):
            if f.name.startswith('in'):
                inputs[f.name[3:-11]] = pd.read_csv(f, header=0, index_col=0, parse_dates=True).iat[0, 0]

            elif f.name.startswith('out'):
                outputs[f.name[4:-11]] = pd.read_csv(f, header=0, index_col=0, parse_dates=True).iat[0, 0]

        else:
            if f.name.startswith('in'):
                inputs[f.name[3:-4]] = pd.read_csv(f, header=0, index_col=0, parse_dates=True)

            elif f.name.startswith('out'):
                outputs[f.name[4:-4]] = pd.read_csv(f, header=0, index_col=0, parse_dates=True)

    return inputs, outputs


def assert_equal(counter: str, expected: Dict[str, Any], v: Any):
    if isinstance(v, pd.Series):
        pd.testing.assert_series_equal(expected[counter], v, check_names=False)
    elif isinstance(v, pd.DataFrame):
        pd.testing.assert_frame_equal(expected[counter], v, check_names=False)
    else:
        assert expected[counter] == v
