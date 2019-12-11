from game_model.interpreter.matcher import match
from game_model.parser.parser import parse
from collections import deque

registers = {}
stacks = {}
stacks['elementary'] = deque()
'''
def test_simple_parse():
    string = 'pass[elementary] = possession as @0 -> possession as @1 : @1 == @2 then push(pass, elementary, @0, @1)'

    expected = [
        {
            'condition': [
                {
                    'pattern': [
                            {
                                'type': 'possession'
                            },
                            '@0',
                            {
                                'type': 'possession'
                            },
                            '@1'
                        ],
                    'stack': 'elementary'
                }
            'constraints': lambda registers: registers['@1']==registers['@1']
            'action': lambda stacks, registers: stacks['elementary'].push(registers['@0'])
            ]
        }
    ]

    assert match(parse(string), expected)
'''