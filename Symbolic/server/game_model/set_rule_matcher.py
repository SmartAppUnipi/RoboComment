from rule_matcher import rule_matcher


def set_rule_matcher(rules):
    for rule in rules:
        if not rule_matcher(rule.condition, rule.action):
            return False
    return True