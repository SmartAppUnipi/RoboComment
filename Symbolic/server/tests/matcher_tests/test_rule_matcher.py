from game_model.interpreter.rule_matcher import rule_matcher
from game_model.game_model import U
from collections import deque

action = 'True'
constraints = 'True'

registers = {}

model = U

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

U._stacks = stacks

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
    'constraints': constraints,
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
    'constraints': constraints,
    'action': action
}

def test_rule_match_single():
    assert rule_matcher(single_rule['condition'], single_rule['action'], single_rule['constraints'])

def test_rule_match_double():
    assert rule_matcher(double_rule['condition'], double_rule['action'], double_rule['constraints'])
