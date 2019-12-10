import re
from ast import literal_eval

def _split(rule_string: str):
    name_and_stack, rules, constraints, action = re.split(' = | : | then ', rule_string)
    action_list = action.split(';')

    name, stack = re.findall('[a-z|_]+', name_and_stack)

    return name, stack, rules, constraints, action_list


def parse(rule_string: str):
    name, stack, rules, constraints, action  = _split(rule_string)

    parse_obj = {
        'condition': [],
        'action': None,
        'constraints': None,
        'name': name
    }

    for rule in rules.split(' & '):
        _parse_rule(rule, parse_obj)
        list.reverse(parse_obj['condition'][-1]['pattern'])
        parse_obj['condition'][-1]['stack'] = stack

    parse_obj['constraints'] = constraints
    parse_obj['action'] = action
    return parse_obj


def _parse_rule(rule: str, parse_obj):
    parts = rule.split(' -> ')
    parse_obj['condition'].append({
        'pattern': []
    })
    for part in parts:
        *alias, name = part.split(' as ')

        if len(alias) > 0:
            parse_obj['condition'][-1]['pattern'].append(
                alias[0]
            )

        parse_obj['condition'][-1]['pattern'].append(
            literal_eval(name) if re.match(r'\{.*\}', name) else name
        )
