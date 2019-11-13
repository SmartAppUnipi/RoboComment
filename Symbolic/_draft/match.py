#!/bin/python

value = {
    'x1': {
        'x1.1': 5
    },
    'x2': 7
}

pattern = {
    'x1': {
        'x1.1': 5
    },
    'x2': 7
}

def match(value, pattern):

    if isinstance(pattern, int):
        return pattern == value
    
    if isinstance(pattern, dict) \
       and not set(pattern.keys()).issubset(set(value.keys())):
        return False

    for key in pattern.keys():
        if not match(pattern[key], value[key]):
            return False

    return True


print(match(value, pattern))
