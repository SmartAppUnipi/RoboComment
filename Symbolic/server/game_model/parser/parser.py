import re
from ast import literal_eval

def _split(rule_string: str):
    name_and_stack, rules, constraints, action = re.split(' = | : | then ', rule_string
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
        # if re.match(match, name):
        #     parse_obj['condition'][-1]['pattern'].append(literal_eval(name))
        # else:
        #     parse_obj['condition'][-1]['pattern'].append(name)


#x = parse("pass[elementary] = @0 as {'type': 'possession'} -> .{0,4} -> @1 as {'type': 'possession'} -> @3 as ? : @0.player.team == @1.player.team then push('elementary', {'type': 'pass', 'from': @0, 'to': @1})"), consume('elementary')

#print(x)
