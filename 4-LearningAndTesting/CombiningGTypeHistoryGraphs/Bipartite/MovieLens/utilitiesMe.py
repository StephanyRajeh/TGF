# Source: https://www.freecodecamp.org/news/how-to-flatten-a-dictionary-in-python-in-4-different-ways/
from collections.abc import MutableMapping

def _flatten_dict_gen(d, parent_key, sep):
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            yield from flatten_dict(v, new_key, sep=sep).items()
        else:
            yield new_key, v


def flatten_dict(d: MutableMapping, parent_key: str = '', sep: str = '.'):
    return dict(_flatten_dict_gen(d, parent_key, sep))
    
# Testing --> flatten_dict({'a': 1, 'c': {'a': 2, 'b': {'x': 3, 'y': 4, 'z': 5}}, 'd': [6, 7, 8]})
# Output  --> {'a': 1, 'c.a': 2, 'c.b.x': 3, 'c.b.y': 4, 'c.b.z': 5, 'd': [6, 7, 8]}