from game_model.interpreter.rule_matcher import rule_matcher
from game_model.game_model import GameModel

def set_rule_matcher():
    rules = GameModel.get_env()['rules']
    for rule in rules.values():
        rule_matcher(rule['condition'], rule['action'], rule['constraints'])