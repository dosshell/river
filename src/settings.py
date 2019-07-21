import json


def read_settings(file) -> dict:
    with open(file) as f:
        return json.load(f)
    return {}
