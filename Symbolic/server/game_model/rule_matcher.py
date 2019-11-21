from boolean_matcher import boolean_matcher
import types

def rule_matcher(condition, action):
    if not isinstance(action, types.FunctionType):
        raise TypeError
    if boolean_matcher(condition):
        action()
    #     return True
    # return False
    #Probably return value is not needed since action is performed here