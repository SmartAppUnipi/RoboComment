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


def parse(rule_string: str):
    name, rules = rule_string.split(' = ')

    if ':' not in rules:
        return {
            'name': name,
            'function': rules[3:]
        }

    rules, constraints = rules.split(' : ')

    parse_obj = {
        'condition': [],
        'action': None,
        'name': name
    }
    for rule in rules.split(' & '):
        _parse_rule(rule, parse_obj)
        _parse_stack(name, parse_obj)
    _parse_constraints(constraints, parse_obj)

    return parse_obj


def _token_match(token: str, part: str):
    if token == r'.{\d,\d}':
        return len(re.findall(token, part)) != 0

    return token in part


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


def _parse_stack(stack: str, parse_obj):
    parse_obj['condition'][-1]['stack'] = 'inner'


def _parse_constraints(constraints: str, parse_obj):
    for param in re.findall(r'@\d', constraints):
        constraints = constraints.replace(
            param, "registers['{}']".format(param))

    f = 'lambda registers: ' + constraints
    # print(f)
    parse_obj['action'] = eval(f)


# x1 = parse('pass = possession as @0 -> .{0,4} -> possession as @1 : @0.player.team == @1.player.team')
# x2 = parse('pass = possession(p1) -> .{0,8} -> possession(p2) : p1.team != p2.team')
# x3 = parse('shotOnTarget = possession(p1) -> ballOnTarget : p1.position in _awayhalf')
# x4 = parse('shotOffTarget = possession(p1) -> ballOffTarget : p1.position in _awayhalf')
# x = parse('possession = ___ball_owner')
# print(x)
# print([x1, x2, x3, x4])
# print(x1)
