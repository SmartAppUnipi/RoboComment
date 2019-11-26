from game_model.interpreter.rule_matcher import rule_matcher


def set_rule_matcher(rules):
    for rule in rules:
        rule_matcher(rule.condition, rule.action)