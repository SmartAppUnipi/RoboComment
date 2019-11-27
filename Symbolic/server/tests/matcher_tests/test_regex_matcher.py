from game_model.interpreter.regex_matcher import regex_matcher

registers = {}

#Regex same size of stack
def test_regex_match_single_string():
    regex = [{'first': 'elem'}]
    stack = [{'first': 'elem'}]
    
    assert regex_matcher(regex, stack, registers)

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
        
    assert regex_matcher(regex, stack, registers)

#Regex (and its element) fewer elements than stack (and its elements)
def test_regex_match_objects():
    regex = [
        {
            'first': {
                'inner': 'elem'
            },
            'second': 'help'
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
        
    assert regex_matcher(regex, stack, registers)

def test_regex_longer():
    regex = [
        {
            'first': {
                'inner': 'elem'
            }
        },
        {
            'second': 'exist'
        }
    ]
    stack = [
        {
            'first': {
                'inner': 'elem'
            }
        }
    ]

    assert not regex_matcher(regex, stack, registers)

def test_regex_match_stackfirst():
    regex = ['a', '.', 'c']
    stack = ['a', 'b', 'b', 'b', 'b']

    assert not regex_matcher(regex, stack, registers)

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
    
    assert regex_matcher(regex, stack, registers)

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
    
    assert regex_matcher(regex, stack, registers)


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
    
    assert regex_matcher(regex, stack, registers)


def test_regex_match_any_seq_bounded_upper():
    regex = [
        {
            'first': 'elem'
        },
        '.{2,3}',
        {
            'last': 'newelem'
        }
    ]
    stack = [
        {
            'first': 'elem',
            'time': 20000
        },
        {
            'second': 'skip',
            'time': 20001
        },
        {
            'secondhalf': 'skipagain',
            'time': 21000
        },
        {
            'second3quarter': 'tripleskip',
            'time': 22000
        },
        {
            'last': 'newelem',
            'time': 23000
        }
    ]
    
    assert regex_matcher(regex, stack, registers)

def test_regex_match_any_seq_bounded_lower():
    regex = [
        {
            'first': 'elem'
        },
        '.{2,3}',
        {
            'last': 'newelem'
        }
    ]
    stack = [
        {
            'first': 'elem',
            'time': 20000
        },
        {
            'second': 'skip',
            'time': 21000
        },
        {
            'secondhalf': 'skipagain',
            'time': 21500
        },
        {
            'last': 'newelem',
            'time': 22000
        }
    ]
    
    assert regex_matcher(regex, stack, registers)

def test_regex_match_any_seq_bounded_short():
    regex = [
        {
            'first': 'elem'
        },
        '.{2,3}',
        {
            'last': 'newelem'
        }
    ]
    stack = [
        {
            'first': 'elem',
            'time': 0
        },
        {
            'second': 'skip',
            'time': 1000
        },
        {
            'last': 'newelem',
            'time': 1500
        }
    ]
    
    assert not regex_matcher(regex, stack, registers)

def test_regex_match_any_seq_bounded_long():
    regex = [
        {
            'first': 'elem'
        },
        '.{2,3}',
        {
            'last': 'newelem'
        }
    ]
    stack = [
        {
            'first': 'elem',
            'time': 0
        },
        {
            'second': 'skip',
            'time': 1
        },
        {
            'secondhalf': 'skipagain',
            'time': 2
        },
        {
            'secondhalfhalf': 'skipagain',
            'time' : 3
        },
        {
            'second3quarter': 'tripleskip',
            'time': 4
        },
        {
            'last': 'newelem',
            'time': 4000
        }
    ]
    
    assert not regex_matcher(regex, stack, registers)


def test_regex_match_any_seq_bounded_zero():
    regex = [
        {
            'first': 'elem'
        },
        '.{0,3}',
        {
            'last': 'newelem'
        }
    ]
    stack = [
        {
            'first': 'elem',
            'time': 10
        },
        {
            'last': 'newelem',
            'time': 10
        }
    ]
    
    assert regex_matcher(regex, stack, registers)

def test_regex_match_any_seq_bounded_zero_one():
    regex = [
        {
            'first': 'elem'
        },
        '.{0,3}',
        {
            'last': 'newelem'
        }
    ]
    stack = [
        {
            'first': 'elem',
            'time': 0
        },
        {
            'second': 'here',
            'time': 1000
        },
        {
            'last': 'newelem',
            'time': 2000
        }
    ]
    
    assert regex_matcher(regex, stack, registers)

def test_regex_match_register_save():
    reg = {}
    regex = [
    {
        'first': 'elem'
    },
    '@0'
    ]
    stack = [
        {
            'first': 'elem'
        }
    ]

    assert regex_matcher(regex, stack, registers)
    #assert registers['@0'] == {'first':'elem'}

'''
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
'''