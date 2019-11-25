import re

_tokens = [
    'possession',
    r'.{\d,\d}',
    '.',
    'interception',
    'ballOnTarget',
    'ballOffTarget'
]


def _get_pattern(token, part):
    if token in ['possession', 'interception', 'ballOnTarget', 'ballOffTarget']:
        return {
            'type': token
        }
    elif token in ['.', r'.{\d,\d}']:
        return part

    raise Exception('Unrecognized token: ' + token)


def parse(rule_string):
    stack, rule = rule_string.split(' = ')
    rule, constraints = rule.split(' : ')

    parse_obj = {
        'condition': {},
        'action': None
    }

    _parse_rule(rule, parse_obj)
    _parse_stack(stack, parse_obj)
    _parse_constraints(constraints, parse_obj)

    return parse_obj


def _token_match(token, part):
    if token == r'.{\d,\d}':
        return len(re.findall(token, part)) != 0

    return token in part


def _parse_rule(rule, parse_obj):
    parts = rule.split(' -> ')
    parse_obj['condition']['pattern'] = []

    for part in parts:
        for token in _tokens:
            if not _token_match(token, part):
                continue

            parse_obj['condition']['pattern'].append(
                _get_pattern(token, part)
            )
            break


def _parse_stack(stack, parse_obj):
    parse_obj['condition']['stack'] = stack


def _parse_constraints(constraints, parse_obj):
    params = list(
        map(
            lambda s: s[:-1],
            re.findall(r'[a-z][a-z0-9]*\.', constraints)
        )
    )

    f = 'lambda ' + ', '.join(params) + ': ' + constraints
    print(f)
    parse_obj['action'] = eval(f)


x1 = parse('pass = possession(p1) -> .{0,8} -> possession(p2) : p1.team == p2.team')
x2 = parse('pass = possession(p1) -> .{0,8} -> possession(p2) : p1.team != p2.team')
x3 = parse('shotOnTarget = possession(p1) -> ballOnTarget : p1.position in _awayhalf')
x4 = parse('shotOffTarget = possession(p1) -> ballOffTarget : p1.position in _awayhalf')

print([x1, x2, x3, x4])
