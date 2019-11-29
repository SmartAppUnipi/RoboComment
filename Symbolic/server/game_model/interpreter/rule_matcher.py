from game_model.interpreter.boolean_matcher import boolean_matcher
from game_model.interpreter.rts import check, fire
from game_model.game_model import GameModel
import types
from collections import deque    #Used by action

'''
This method picks a rule with the following structure:

Rule structure
{
    'condition': [regex1, regex2, ...],
    'action': function()
}

if all the conditions match in AND then the action is executed
'''


def rule_matcher(condition, action, constraints):
    if not isinstance(action, str) or not isinstance(constraints, str):
        raise TypeError
    stacks, registers = GameModel.get_env()
    if boolean_matcher(condition, stacks, registers):
        if check(constraints):
            fire(action)
            return True
    return False
    # Probably return value is not needed since action is performed here
