from game_model.interpreter.boolean_matcher import boolean_matcher
import types

'''
This method picks a rule with the following structure:

Rule structure
{
    'condition': [regex1, regex2, ...],
    'action': function()
}

if all the conditions match in AND then the action is executed
'''


def rule_matcher(condition, action, constraints, stacks, registers):
    '''
    if not isinstance(action, types.FunctionType):
        raise TypeError
    '''
    if boolean_matcher(condition, stacks, registers):
        if constraints(registers):
            action(registers)
            return True
    return False
    # Probably return value is not needed since action is performed here
