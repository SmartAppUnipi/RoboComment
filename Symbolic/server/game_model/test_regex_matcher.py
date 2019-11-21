from regex_matcher import regex_matcher

#Regex same size of stack
def test_regex_match_single_string():
    regex = [{'first': 'elem'}]
    stack = [{'first': 'elem'}]
    
    assert regex_matcher(regex, stack)

#Regex same size of stack
def test_regex_match_single_string_int():
    regex = [
        {
            'first': 'elem',
            'second': 2.0
        }
    ]
    stack = [
        {
            'first': 'elem',
            'second': 2.0
        }
    ]
        
    assert regex_matcher(regex, stack)
#Regex (and its element) fewer elements than stack (and its elements)
def test_regex_match_objects():
    regex = [
        {
            'first': {
                'inner': 'elem'
            }
        }
    ]
    stack = [
        {
            'first': {
                'inner': 'elem'
            },
            'second': 'help'
        },
        {
            'third': 2.0
        }
    ]
        
    assert regex_matcher(regex, stack)

def test_regex_match_any():
    regex = [
        {
            'first': 'elem'
        },
        '?',
        {
            'third': 'last',
        }
    ]
    stack = [
        {
            'first': 'elem'
        },
        {
            'second': 'skip',
        },
        {
            'third': 'last'
        }
    ]
    
    assert regex_matcher(regex, stack)

def test_regex_match_any_seq_last():
    regex = [
        {
            'first': 'elem'
        },
        '.'
    ]
    stack = [
        {
            'first': 'elem'
        },
        {
            'second': 'skip',
        },
        {
            'secondhalf': 'skipagain'
        },
        {
            'third': 'last'
        }
    ]
    
    assert regex_matcher(regex, stack)


def test_regex_match_any_seq_mid():
    regex = [
        {
            'first': 'elem'
        },
        '.',
        {
            'last': 'newelem'
        }
    ]
    stack = [
        {
            'first': 'elem'
        },
        {
            'second': 'skip',
        },
        {
            'secondhalf': 'skipagain'
        },
        {
            'last': 'newelem'
        }
    ]
    
    assert regex_matcher(regex, stack)


def test_regex_match_start_kleene():
    regex = [
        '*',
        {
            'first': 'elem'
        }
    ]
    stack = [
        {
            'first': 'elem'
        }
    ]
    
    try:
        assert regex_matcher(regex, stack)
    except:
        print('Exception correctly generated')

def test_regex_match_kleene():
    regex = [
        {
            'first': 'elem'
        },
        '*',
        {
            'second': 'last'
        }
    ]
    stack = [
        {
            'first': 'elem'
        },
        {
            'first': 'elem'
        },
        {
            'first': 'elem'
        },
        {
            'second': 'last'
        }
    ]
    
    assert regex_matcher(regex, stack)

def test_regex_match_incomplete_kleene():
    regex = [
        {
            'first': 'elem'
        },
        '*',
        {
            'second': 'last'
        }
    ]
    stack = [
        {
            'first': 'elem'
        },
        {
            'first': 'elem'
        },
        {
            'first': 'elem'
        }
    ]
    
    assert regex_matcher(regex, stack)

test_regex_match_single_string()
test_regex_match_single_string_int()
test_regex_match_objects()
test_regex_match_any()
test_regex_match_any_seq_last()
test_regex_match_any_seq_mid()
test_regex_match_start_kleene()
test_regex_match_kleene()
test_regex_match_incomplete_kleene()