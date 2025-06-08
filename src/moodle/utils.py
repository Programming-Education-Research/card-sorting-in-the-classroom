from collections import defaultdict


def join_by(key, *args):
    key_to_result = defaultdict(dict)
    for col in args:
        for item in col:
            key_to_result[item[key]] |= item
    return list(key_to_result.values())