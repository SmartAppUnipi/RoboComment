from matcher import match

_any = '?'
_anyseq = '.'
_kleene = '*'

def consume(iter):
    return next(iter)

def regex_matcher(regex, stack):
    # TODO empty regex always/never match?
    #TODO check this assertion
    if len(regex) > len(stack):
        return False

    pred = None
    reg_iter = iter(regex)
    stack_iter = iter(stack)
    for reg_el, stack_el in zip(reg_iter, stack_iter):
        if match(reg_el, _any):
            #Any value is ok, iterate
            continue
        
        if match(reg_el, _anyseq):
            #Check next element of regex
            try:
                reg_el = consume(reg_iter)
            except StopIteration:
                #If last is anyseq for sure will match
                return True
            #Match any elemnt in stack until I match next
            while not match(stack_el, reg_el):
                try:
                    stack_el = consume(stack_iter)
                except StopIteration:
                    #Stack finished, next element not matched
                    return False
            #Matched first, any sequence, second
            continue

        if match(reg_el, _kleene) and pred is None:
            raise Exception('Regex starting with kleene')
        
        '''#TODO Incomplete
        if match(reg_el, _kleene) and pred is not None:
            while match(stack_el, pred):
                try:
                    stack_el = consume(stack_iter)
                except StopIteration:
                    continue
        '''

        if not match(stack_el, reg_el):
            # One element did not match
            return False

        pred = reg_el
    # May have finished regex or finished stack
    #If finished regex everything matched
    try:
        consume(reg_iter)
    except StopIteration:
        return True
    # Otherwise stack was finished before regex e.g. regex=a.b, stack=a,b,b,b
    return False
