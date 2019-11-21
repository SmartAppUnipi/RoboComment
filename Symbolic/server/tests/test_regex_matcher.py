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


test_regex_match_single_string()
test_regex_match_single_string_int()
test_regex_match_objects()