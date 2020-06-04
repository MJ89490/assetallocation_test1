from typing import Dict, Union, Any, Set, Optional, List, Tuple

import re

import json

from numpy import inf

import pandas as pd


class Compare:
    int_regex = r'(?:[-+]?[\d]+)'

    float_regex = r'(?:\.?[\d]+)'

    e_pow_regex = f'(?:[eE]{int_regex})'

    will_it_float = re.compile(f"^{int_regex}{float_regex}?{e_pow_regex}?$")

    def __init__(self, strip: bool, tolerance: float, absolute: bool, ignore_missing: bool=False, ignore_unexpected: bool=False,

                 full_missing_unexpected: bool=True) -> None:
        self.absolute = absolute

        self.strip = strip

        self.tolerance = tolerance

        self.ignore_missing = ignore_missing

        self.ignore_unexpected = ignore_unexpected

        self.full_missing_unexpected = full_missing_unexpected


class CompareJSON(Compare):

    def __init__(self, json_original: str, json_new: str, strip: bool = True, tolerance: float = 0,

                 field_tolerances: Optional[Dict[str, float]] = None, ignore_fields: Optional[Set[str]] = None,

                 absolute: bool = True, nested: bool = True, ignore_missing: bool = False,

                 ignore_unexpected: bool = False, full_missing_unexpected: bool = True):

        super().__init__(strip, tolerance, absolute, ignore_missing, ignore_unexpected, full_missing_unexpected)

        self.__altered = False

        self.json_original = json_original

        self.json_new = json_new

        self.field_tolerances = field_tolerances

        self.ignore_fields = ignore_fields

        self.nested = nested

        self._diff = None

    @property
    def json_original(self):

        return self._json_original

    @json_original.setter
    def json_original(self, json_original: str):

        self._json_original = json.loads(json_original)

        self.__altered = True

    @property
    def json_new(self):

        return self._json_new

    @json_new.setter
    def json_new(self, json_new: str):

        self._json_new = json.loads(json_new)

        self.__altered = True

    @property
    def field_tolerances(self):

        return self._field_tolerances

    @field_tolerances.setter
    def field_tolerances(self, field_tolerances: Optional[Dict[str, float]]):

        self._field_tolerances = field_tolerances or {}

        self.__altered = True

    @property
    def ignore_fields(self):

        return self._ignore_fields

    @ignore_fields.setter
    def ignore_fields(self, ignore_fields: Optional[Set[str]]):

        self._ignore_fields = set(ignore_fields) or set()

        self.__altered = True

    @property
    def nested(self):

        return self._nested

    @nested.setter
    def nested(self, nested: bool):

        self._nested = nested

        self.__altered = True

    @property
    def diff(self) -> Union[List, Dict]:

        if self._diff is None or self.__altered:
            self._diff = self.compare_json()

        return self._diff

    def compare_json(self) -> Union[List, Dict]:

        if self._nested:

            return self._compare_nested_json()



        else:

            return self._compare_flat_json()

    def _compare_nested_json(self) -> Union[List, Dict]:

        j_diff = []

        if isinstance(self._json_original, list) and isinstance(self._json_new, list):

            json_list = self._comp_json_list(self._json_original, self._json_new)

            j_diff = json_list

        elif isinstance(self._json_original, dict) and isinstance(self._json_new, dict):

            j_diff = self._comp_json_dict(self._json_original, self._json_new)

        else:

            j_diff.append(self._compare_vals(self._json_original, self._json_new, self.tolerance))

        return j_diff

    def _comp_json_list(self, j1: List[Any], j2: List[Any]) -> List:

        list_diff = []

        len_j1, len_j2 = len(j1), len(j2)

        shared_index = min(len_j1, len_j2)

        missing = [{'missing': j1[i]} for i in range(shared_index, len_j1)]

        unexpected = [{'unexpected': j2[i]} for i in (range(shared_index, len_j2))]

        for i in range(shared_index):

            r1, r2 = j1[i], j2[i]

            if isinstance(r1, list) and isinstance(r2, list):

                diff = self._comp_json_list(r1, r2)



            elif isinstance(r1, dict) and isinstance(r2, dict):

                diff = self._comp_json_dict(r1, r2)



            else:

                diff = self._compare_vals(r1, r2, self.tolerance)

            if diff:
                list_diff.append(diff)

        list_diff.extend(missing)

        list_diff.extend(unexpected)

        return list_diff

    def _comp_json_dict(self, r1: Dict, r2: Dict) -> Dict:

        shared_keys, missing, unexpected = self._compare_keys(r1, r2)

        dict_diff = {**missing, **unexpected}

        for key in shared_keys:

            if isinstance(r1[key], list) and isinstance(r2[key], list):

                diff = self._comp_json_list(r1[key], r2[key])



            elif isinstance(r1[key], dict) and isinstance(r2[key], dict):

                diff = self._comp_json_dict(r1[key], r2[key])



            else:

                key_tol = self._field_tolerances.get(key, self.tolerance)

                diff = self._compare_vals(r1[key], r2[key], key_tol)

            if diff:
                dict_diff[key] = diff

        if any(dict_diff.values()):

            return dict_diff



        else:

            return {}

    def _compare_flat_json(self) -> List:

        j_diff = []

        for i in range(len(self._json_original)):

            r1, r2 = self._json_original[i], self._json_new[i]

            shared_keys, missing, unexpected = self._compare_keys(r1, r2)

            diff = {**missing, **unexpected}

            for key in shared_keys:

                key_tol = self._field_tolerances.get(key, self.tolerance)

                val_diff = self._compare_vals(r1[key], r2[key], key_tol)

                if val_diff:
                    diff[key] = val_diff

            if any(diff.values()):
                diff['record_no'] = i

                j_diff.append(diff)

        return j_diff

    def _compare_keys(self, r1, r2) -> Tuple[List, Dict, Dict]:

        shared_keys = [key for key in r1 if key in r2 and key not in self._ignore_fields]

        if not self.ignore_missing:

            if self.full_missing_unexpected:

                missing = {key: {'missing': r1[key]} for key in r1 if
                           key not in shared_keys and key not in self._ignore_fields}
            else:

                missing = {key: 'missing' for key in r1 if key not in shared_keys and key not in self._ignore_fields}
        else:

            missing = {}

        if not self.ignore_unexpected:

            if self.full_missing_unexpected:

                unexpected = {key: {'unexpected': r2[key]} for key in r2 if
                              key not in shared_keys and key not in self._ignore_fields}
            else:

                unexpected = {key: 'unexpected' for key in r2 if
                              key not in shared_keys and key not in self._ignore_fields}
        else:

            unexpected = {}

        return shared_keys, missing, unexpected

    def _compare_vals(self, v1: object, v2: object, tolerance: float) -> str:

        if self.strip and isinstance(v1, str) and isinstance(v2, str):
            v1, v2 = v1.strip(), v2.strip()

        if v1 == v2:

            return ''

        elif self.will_it_float.fullmatch(str(v1)) is not None and self.will_it_float.fullmatch(str(v2)) is not None:

            if self.absolute:

                diff = float(v2) - float(v1)
            else:

                diff = (float(v2) - float(v1)) / float(v1) if float(v1) != 0 else inf

            return f'1: {v1} 2: {v2} diff: {diff}' if abs(diff) > tolerance else ''

        elif pd.isnull(v1) and pd.isnull(v2):

            return ''

        else:

            return f'1: {v1} 2: {v2}'


class CompareCsv(Compare):

    def __init__(self, csv_original: str, csv_new: str, csv_diff: str, strip: bool = True, tolerance: float = 0,

                 col_tolerances: Optional[Dict[int, float]] = None, absolute: bool = True) -> None:

        super().__init__(strip, tolerance, absolute)

        self.csv1 = csv_original

        self.csv2 = csv_new

        self.csv_diff = csv_diff

        self.col_tolerances = col_tolerances or {}

    def _compare_strs(self, v1: str, v2: str, tolerance: float) -> str:

        if self.strip:
            v1, v2 = v1.strip(), v2.strip()

        if v1 == v2:

            return ''

        elif self.will_it_float.fullmatch(v1) is not None and self.will_it_float.fullmatch(v2) is not None:

            if self.absolute:

                diff = (float(v2) - float(v1))

            else:

                diff = (float(v2) - float(v1)) / float(v1)

            return str(diff) if abs(diff) > tolerance else ''

        else:

            return f'-"{v1}" +"{v2}"'

    def compare_csvs_by_line(self):

        with open(self.csv1) as f1:

            with open(self.csv2) as f2:

                with open(self.csv_diff, 'a+') as f3:

                    l1, l2 = f1.readline().rstrip().split(','), f2.readline().rstrip().split(',')

                    line_no = 0

                    while any(l1) and any(l2):

                        d = []

                        for i in range(len(l1)):
                            i_tol = self.col_tolerances.get(i, self.tolerance)

                            d.append(self._compare_strs(l1[i], l2[i], i_tol))

                        if any(d):
                            f3.write(f'{line_no},' + ','.join(d) + '\n')

                        line_no += 1

                        l1, l2 = f1.readline().rstrip().split(','), f2.readline().rstrip().split(',')

if __name__ =="__main__":
    csv1 = r"C:\Users\AJ89720\PycharmProjects\assetallocation_arp\tests\assetallocation_arp\models\resources\effect\outputs_origin\trend_spot_origin.csv"
    csv2 = r"C:\Users\AJ89720\PycharmProjects\assetallocation_arp\tests\assetallocation_arp\models\resources\effect\outputs_to_test\trend_spot_to_test.csv"
    csv3 = r"C:\Users\AJ89720\PycharmProjects\assetallocation_arp\tests\assetallocation_arp\models\resources\diff2.csv"
    obj = CompareCsv(csv_original=csv1, csv_new=csv2, csv_diff=csv3, strip=True, tolerance=1)
    obj.compare_csvs_by_line()
