from typing import Dict


def format_versions(versions: Dict[int, str]) -> Dict[str, int]:
    versions_dict = {}
    for key, value in versions.items():
        if value == '':
            value = 'no description'
        versions_dict[str(key) + ": " + value] = key

    return {k: v for k, v in sorted(versions_dict.items(), key=lambda item: item[1], reverse=True)}

