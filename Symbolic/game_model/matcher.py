import re
import types
numeric_types = (int, float)

def match(value, pattern):

    # Case one, type of both pattern and value are int, floats or strings
    if (isinstance(pattern, str) and isinstance (value, str)) or \
            (isinstance(pattern, numeric_types) and isinstance(value, numeric_types)):
        return pattern == value

    #
    elif isinstance(pattern,str):
        if re.match("%<\d+", pattern):
            return value < pattern.split("<")[1]
        elif re.match("%>\d+", pattern):
            return value > pattern.split(">")[1]
        return False

    #
    elif type(pattern) == types.FunctionType:
        try:
            return pattern(value)
        except TypeError as e:
            return False
    
    #
    elif isinstance(pattern, dict) and isinstance(value, dict):
        if not set(pattern.keys()).issubset(set(value.keys())):
            return False

        for key in pattern.keys():
            if not match(pattern[key], value[key]):
                return False

        return True

    #
    else:
        return False