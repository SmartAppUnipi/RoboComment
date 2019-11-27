from game_model.interpreter.rule_matcher import rule_matcher

def action():
    print('Correct')

registers = {}

stacks = {
    'first_stack':[
        {
            'first': 'ok',
            'last': 'knock'
        }
    ],
    'second_stack':[
        {
            'test': 'I',
            'second': 'hope'
        },
        {
            'third': 'it',
            'last': 'works'
        }
    ]
}

single_rule = {
    'condition': [
        {
            'pattern': [
                {
                    'first': 'ok'
                }
            ],
            'stack': 'first_stack'
        }
    ],
    'action': action
}

double_rule = {
    'condition': [
        {
            'pattern': [
                {
                    'first': 'ok'
                }
            ],
            'stack': 'first_stack'
        },
        {
            'pattern': [
                {
                    'test': 'I',
                    'second': 'hope'
                },
                '?'
            ],
            'stack': 'second_stack'
        }
    ],
    'action': action
}

def test_rule_match_single():
    assert rule_matcher(single_rule['condition'], single_rule['action'], stacks, registers)

def test_rule_match_double():
    assert rule_matcher(double_rule['condition'], double_rule['action'], stacks, registers)
