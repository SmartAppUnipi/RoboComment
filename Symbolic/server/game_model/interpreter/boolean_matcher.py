from game_model.interpreter.regex_matcher import regex_matcher

'''
This method picks a set of regexes and checks wether they all match in AND.
The regex is an object with the following structure:

Regex structure
{
    'pattern': [Object1, Object2, ...],
    'stack': Stack
}

This means that for each regex object this methods matches the pattern on the stack.
'''


def boolean_matcher(regexes, stacks, registers):
    # TODO Empty se true or false?
    if len(regexes) < 1:
        # Empty
        return False
    for regex in regexes:
        if not regex_matcher(regex['pattern'], stacks[regex['stack']], registers):
            return False
    return True
    
''''from regex_matcher import regex_matcher

def boolean_matcher(regexes):
    if len(regexes) < 1:
        # Empty
        return False
    outputs = []
    for regex in regexes:
        passed, out = regex_matcher(regex['pattern'], regex['stack'])
        if not passed:
            return False, None
        outputs.append()
    return True, outputs
    '''