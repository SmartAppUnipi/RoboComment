from game_model.interpreter.rule_matcher import rule_matcher


def set_rule_matcher(rules, stacks):
    for rule in rules:
        rule_matcher(rule.condition, rule.action, stacks)