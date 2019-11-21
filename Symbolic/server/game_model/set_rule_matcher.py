from rule_matcher import rule_matcher

#I assumed a rule as an object with:
#Condition to satisfy
#Action to perform

def set_rule_matcher(rules):
    for rule in rules:
        rule_matcher(rule.condition, rule.action)