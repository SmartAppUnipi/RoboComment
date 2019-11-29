import re

def _token_match(token: str, part: str):
    if token == r'.{\d,\d}':
        return len(re.findall(token, part)) != 0

    return token in part


def _split(rule_string: str):
    name_and_stack, rules, constraints, action = re.split(' = | : | then ', rule_string)
    name, stack = re.findall('[a-z]+', name_and_stack)
    return name, stack, rules, constraints, action


def parse(rule_string: str):
    try:
        out = _split(rule_string)
    except:
        name_and_stack, rules = rule_string.split(' = ')
        name, stack = re.findall('[a-z]+', name_and_stack)
        return {
            'name': name,
            'function': rules[3:],
            'stack': stack
        }

    name, stack, rules, constraints, action = out

    parse_obj = {
        'condition': [],
        'action': None,
        'constraints': None,
        'name': name
    }

    for rule in rules.split(' & '):
        _parse_rule(rule, parse_obj)
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
        name, *alias = part.split(' as ')
        parse_obj['condition'][-1]['pattern'].append(name)

        if len(alias) > 0:
            parse_obj['condition'][-1]['pattern'].append(
                alias[0]
            )


# x = parse("pass[elementary] = {'type': 'possession'} as @0 -> .{0,4} -> {'type': 'possession'} as @1 : @0.player.team == @1.player.team then push('elementary', {'type': 'pass', 'from': @0, 'to': @1})")
# print(x)
