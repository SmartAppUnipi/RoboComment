from game_model.interpreter.boolean_matcher import boolean_matcher

stacks = {
    'firstsecondlast': [
        {
            'first': 'elem',
            'second': 'second'
        },
        {
            'last': 'last'
        }
    ],
    'firstsecond': [
        {
            'first': 'elem',
            'second': 'second'
        }
    ]
}

first = {
    'pattern': [
        {
            'first': 'elem',
            'second': 'second'
        },
        '?'
    ],
    'stack': 'firstsecondlast'
}

second = {
    'pattern': [
        {
            'first': 'elem',
            'second': 'second'
        },
        {
            'last': 'last'
        }
    ],
    'stack': 'firstsecond'
}

def test_boolean_match_singletrue_regex():
    assert boolean_matcher([first], stacks)

def test_boolean_match_singlefalse_regex():
    assert not boolean_matcher([second], stacks)

def test_boolean_match_copy_regex():
    assert boolean_matcher([first, first], stacks)

def test_boolean_match_truefalse_regex():
    assert not boolean_matcher([first, second], stacks)


test_boolean_match_singletrue_regex()
test_boolean_match_singlefalse_regex()
test_boolean_match_copy_regex()
test_boolean_match_truefalse_regex()