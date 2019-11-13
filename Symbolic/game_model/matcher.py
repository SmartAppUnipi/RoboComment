import re
import types
numeric_types = (int, float)

def match(value, pattern):
    """
    Matches a generic pattern with a value. The match is found in 4 cases:
    - value and pattern are strings or number with the same value
    - String with the form "%opX", in this case the value returned is (X op value)
    - function call, the value returned must be a boolean and is the result of match
    - value and pattern are dictionaries. All the keys in pattern must be present in value and
        their content must be equal
    """
    # Case one, type of both pattern and value are int, floats or strings
    if (isinstance(pattern, str) and isinstance (value, str)) or \
            (isinstance(pattern, numeric_types) and isinstance(value, numeric_types)):
        return pattern == value

    # String with form %opValue, where percentage is a fixed placeholder for values 
    elif isinstance(pattern,str):
        if re.match("%<\d+", pattern):
            return value < pattern.split("<")[1]
        elif re.match("%>\d+", pattern):
            return value > pattern.split(">")[1]
        elif re.match("%=\d+", pattern):
            return value == pattern.split("=")[1]
        return False

    # function call
    elif type(pattern) == types.FunctionType:
        try:
            # apply pattern function
            ret = pattern(value)
            if isinstance(ret, bool):
                # assert that the returned value is boolean
                return ret
            else:
                return False
        except TypeError as e:
            return False
    
    # Case of object, checks that every key is present and every value is equal recursively
    elif isinstance(pattern, dict) and isinstance(value, dict):
        if not set(pattern.keys()).issubset(set(value.keys())):
            return False

        for key in pattern.keys():
            if not match(pattern[key], value[key]):
                return False

        return True

    # Not a match
    else:
        return False