from game_model.interpreter.boolean_matcher import boolean_matcher
import types

'''Rule structure
{
    'condition': [regex1, regex2, ...],
    'action': function()
}
A regex is an object as define in regex_matcher.py
'''


def rule_matcher(condition, action):
    if not isinstance(action, types.FunctionType):
        raise TypeError
    if boolean_matcher(condition):
        action()
        return True
    return False
    # Probably return value is not needed since action is performed here
