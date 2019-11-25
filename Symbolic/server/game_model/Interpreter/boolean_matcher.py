from regex_matcher import regex_matcher

def boolean_matcher(regexes):
    # TODO Empty se true or false?
    if len(regexes) < 1:
        # Empty
        return False
    for regex in regexes:
        if not regex_matcher(regex['pattern'], regex['stack']):
            return False
            #return False
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