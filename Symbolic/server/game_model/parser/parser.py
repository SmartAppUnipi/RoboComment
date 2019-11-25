
_tokens = {
    'possession': lambda: {'type': 'possession'}
}


def parse(rule_string):
    stack, rule = rule_string.split(' = ')
    rule, constraints = rule.split(' : ')

    parse_obj = {
        'condition': {},
        'action': None
    }

    parse_rule(rule, parse_obj)
    parse_stack(stack, parse_obj)
    parse_constraints(constraints, parse_obj)

    return parse_obj


def parse_rule(rule, parse_obj):
    parts = rule.split(' -> ')
    parse_obj['condition']['pattern'] = []

    for part in parts:
        for tok in _tokens.keys():
            if tok not in part:
                continue

            parse_obj['condition']['pattern'].append(
                _tokens[tok]()
            )
            break


def parse_stack(stack, parse_obj):
    parse_obj['condition']['stack'] = stack


def parse_constraints(constraints, parse_obj):
    import re
    params = list(
        map(
            lambda s: s[:-1],
            re.findall(r'[a-z][a-z0-9]*\.', constraints)
        )
    )

    f = 'lambda ' + ', '.join(params)+ ': ' + constraints
    print(f)
    parse_obj['action'] = eval(f)


s = 'pass = possession(p1) -> possession(p2) : p1.team == p2.team'
print(parse(s))
# {
#     'condition': [
#         { //regex
#             'pattern': [
#                 {
#                     type: 'possession'
#                 },
#                 .{0,1},
#                 {
#                     type: 'possession'
#                 }
#             ],
#             'stack': 'pass',
#         }
#     ],
#     'action': lambda p1, p2: p1.team == p2.team
# }
