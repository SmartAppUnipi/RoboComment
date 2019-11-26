from game_model.interpreter.boolean_matcher import boolean_matcher

first = {
    'pattern': [
        {
            'first': 'elem',
            'second': 'second'
        },
        '?'
    ],
    'stack': [
        {
            'first': 'elem',
            'second': 'second'
        },
        {
            'last': 'last'
        }
    ]
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
    'stack': [
        {
            'first': 'elem',
            'second': 'second'
        }
    ]
}

def test_boolean_match_singletrue_regex():
    assert boolean_matcher([first])

def test_boolean_match_singlefalse_regex():
    assert not boolean_matcher([second])

def test_boolean_match_copy_regex():
    assert boolean_matcher([first, first])

def test_boolean_match_truefalse_regex():
    assert not boolean_matcher([first, second])


test_boolean_match_singletrue_regex()
test_boolean_match_singlefalse_regex()
test_boolean_match_copy_regex()
test_boolean_match_truefalse_regex()