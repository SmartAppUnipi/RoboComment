from regex_matcher import regex_matcher

'''Regex structure
{
    'pattern': [None],
    'stack': None
}
'''

def boolean_matcher(regexes):
    # TODO Empty se true or false?
    if len(regexes) < 1:
        # Empty
        return False
    for regex in regexes:
        if not regex_matcher(regex['pattern'], regex['stack']):
            return False
    return True
