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


def _get_pattern(token, part):
    if token in ['possession', 'interception', 'ballOnTarget', 'ballOffTarget']:
        return {
            'type': token
        }
    elif token in ['.', r'.{\d,\d}']:
        return part

    raise Exception('Unrecognized token: ' + token)


def parse(rule_string):
    stack, rules = rule_string.split(' = ')
    rules, constraints = rules.split(' : ')

    parse_obj = {
        'condition': [],
        'action': None,
        'name': stack
    }
    for rule in rules.split(' & '):
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
    parse_obj['condition'].append({
        'pattern': [],
        'alias': []
    })

    for part in parts:
        for token in _tokens:
            if not _token_match(token, part):
                continue

            parse_obj['condition'][-1]['pattern'].append(
                _get_pattern(token, part)
            )
            
            parse_obj['condition'][-1]['alias'].append(
                part.split(' as ')[1] if 'as' in part else None
            )
            break


def _parse_stack(stack, parse_obj):
    parse_obj['condition'][-1]['stack'] = 'inner'


def _parse_constraints(constraints: str, parse_obj):
    for param in re.findall(r'@\d', constraints):
        index = param[-1]
        constraints = constraints.replace(param, _GLOBAL_ARRAY + '[{}]'.format(index))
    
    f = 'lambda: ' + constraints
    print(f)
    parse_obj['action'] = eval(f)

x1 = parse('pass = possession as @0 -> .{0,4} -> possession as @1 : @0.player.team == @1.player.team')
# x2 = parse('pass = possession(p1) -> .{0,8} -> possession(p2) : p1.team != p2.team')
# x3 = parse('shotOnTarget = possession(p1) -> ballOnTarget : p1.position in _awayhalf')
# x4 = parse('shotOffTarget = possession(p1) -> ballOffTarget : p1.position in _awayhalf')

# print([x1, x2, x3, x4])
print(x1)
