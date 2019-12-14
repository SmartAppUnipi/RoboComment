from game_model.interpreter.rule_matcher import rule_matcher
from game_model.game_model import GameModel

def set_rule_matcher():
    rules = GameModel.get_env()['rules']
    any = False
    for rule in rules.values():
        if rule_matcher(rule['condition'], rule['action'], rule['constraints']):
            # At least one rule matched
            any = True
    return any