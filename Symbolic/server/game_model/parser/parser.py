import re

_tokens = [
    'possession',
    r'.{\d,\d}',
    '.',
    'interception',
    'ballOnTarget',
    'ballOffTarget'
]

_GLOBAL_ARRAY = '_global_array'


def _get_pattern(token: str, part: str):
    if token in ['possession', 'interception', 'ballOnTarget', 'ballOffTarget']:
        return {
            'type': token
        }
    elif token in ['.', r'.{\d,\d}']:
        return part

    raise Exception('Unrecognized token: ' + token)


def _token_match(token: str, part: str):
    if token == r'.{\d,\d}':
        return len(re.findall(token, part)) != 0

    return token in part


def _split(rule_string: str):
    if ' : ' not in rule_string:
        raise Exception('Not a rule.')

    name_and_stack, rules_and_more = rule_string.split(' = ')
    name, stack = re.findall('[a-z]+', name_and_stack)
    rules, constraints_and_more = rules_and_more.split(' : ')
    constraints, action = constraints_and_more.split(' then ')

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
        for token in _tokens:
            if not _token_match(token, part):
                continue

            parse_obj['condition'][-1]['pattern'].append(
                _get_pattern(token, part)
            )

            if 'as' in part:
                parse_obj['condition'][-1]['pattern'].append(
                    part.split(' as ')[1]
                )
            break
