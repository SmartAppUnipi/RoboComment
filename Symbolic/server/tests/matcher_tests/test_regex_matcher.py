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
            'time': 20
        },
        {
            'second': 'skip',
            'time': 20.01
        },
        {
            'secondhalf': 'skipagain',
            'time': 21
        },
        {
            'second3quarter': 'tripleskip',
            'time': 22
        },
        {
            'last': 'newelem',
            'time': 23
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
            'time': 0
        },
        {
            'second': 'skip',
            'time': 1
        },
        {
            'secondhalf': 'skipagain',
            'time': 1.5
        },
        {
            'last': 'newelem',
            'time': 2
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
            'time': 1
        },
        {
            'last': 'newelem',
            'time': 1.5
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
            'time': 1
        },
        {
            'second': 'skip',
            'time': 1.01
        },
        {
            'secondhalf': 'skipagain',
            'time': 1.02
        },
        {
            'secondhalfhalf': 'skipagain',
            'time' : 1.03
        },
        {
            'second3quarter': 'tripleskip',
            'time': 1.04
        },
        {
            'last': 'newelem',
            'time': 7
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
            'time': 1
        },
        {
            'last': 'newelem',
            'time': 2
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
            'first': 'elem',
            'second': 'hope',
            'third': {
                'inner': ['aia', 'ciao']
            }
        }
    ]

    assert regex_matcher(regex, stack, reg)
    assert reg['@0'] == {
                            'first':'elem',
                            'second':'hope',
                            'third': {
                                'inner':['aia', 'ciao']
                            }
                        }

def test_regex_match_register_multisave():
    reg = {}
    regex = [
    {
        'first': 'elem'
    },
    '@0',
    '@1'
    ]
    stack = [
        {
            'first': 'elem'
        }
    ]

    assert regex_matcher(regex, stack, reg)
    assert reg['@0'] == {'first':'elem'}
    assert reg['@1'] == {'first':'elem'}

def test_regex_match_register_emptysave():
    reg = {}
    regex = [
        '@0',
        {
        'first': 'elem'
        }
    ]
    stack = [
        {
            'first': 'elem'
        }
    ]

    assert not regex_matcher(regex, stack, reg)

def test_regex_match_register_reference_save():
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

    assert regex_matcher(regex, stack, reg)
    assert reg['@0'] is stack[0]    # It is by reference

def test_regex_match_register_remove():
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

    assert regex_matcher(regex, stack, reg)
    assert reg['@0'] is stack[0]
    stack.remove(reg['@0'])
    assert len(stack) == 0

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