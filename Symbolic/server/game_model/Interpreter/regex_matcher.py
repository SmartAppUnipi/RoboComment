from game_model.interpreter.matcher import match

'''Regex structure
{
    'pattern': [Object1, Object2, ...],
    'stack': None
}
An Object may be a generic object to be matched or a wildcard among the define below
'''

_any = '?'
_anyseq = '.'
#bounded_anyseq = '.{int, int}'
_kleene = '*'


def consume(iter):
    return next(iter)


def regex_matcher(regex, stack):
    # TODO empty regex always/never match?

    pred = None
    reg_iter = iter(regex)
    stack_iter = iter(stack)
    for stack_el, reg_el in zip(stack_iter, reg_iter):
        # Any singleton value is ok, iterate
        if match(reg_el, _any):
            continue

        if type(reg_el) is str:
            first_split = reg_el.split('{')
            corpus = None
            if len(first_split) == 1:
                special = first_split[0]
            else:
                special = first_split[0]
                #Remove '}' and split on ','
                corpus = first_split[1].split('}')[0].split(',')
                #TODO consider lower and upper as timestamps, not number of objects
                lower = int(corpus[0])
                upper = int(corpus[1])

            if match(special, _anyseq):
                # Check next element of regex, look-ahead
                try:
                    reg_el = consume(reg_iter)
                except StopIteration:
                    # If last is anyseq for sure will match bounded or not
                    return True
                    
                if corpus is None:    
                    # Match any element in stack until I match next
                    while not match(stack_el, reg_el):
                        try:
                            stack_el = consume(stack_iter)
                        except StopIteration:
                            # Stack finished, next element not matched
                            return False
                else:
                    # Match any element in stack until I match next
                    count = 0
                    '''Starting with timestamps
                    while True:
                        PASTE FROM BELOW
                        if stack_el['timestamp']-reg_el['timestamp'] >= round(lower/1000):
                            # Reached lower bound for elapsed time
                            break
                        DELETE COUNT
                    TODO Timestamp considered as ms from epoch
                    '''
                    while count < lower:
                        #Consume lower elements (don't care what they are)
                        try:
                            stack_el = consume(stack_iter)
                        except StopIteration:
                            # Stack finished, next element not matched
                            return False
                        count+=1
                    
                    '''Starting with timestamps
                    while not match(stack_el, reg_el):
                        PASTE FROM BELOW
                        if stack_el['timestamp']-reg_el['timestamp'] > round(upper/1000):
                            # Matched or surpassed upper bound for time elapsed
                            return False
                        DELETE COUNT
                        DELETE if count > upper BELOW
                    '''
                    while not match(stack_el, reg_el) and count <= upper:
                        #Consume elements until I match or until I am too far
                        try:
                            stack_el = consume(stack_iter)
                        except StopIteration:
                            # Stack finished, next element not matched
                            return False
                        count+=1
                    
                    if count > upper:
                        #Next element not found in at most upper steps
                        return False
                # Matched first, any bounded or unbounded sequence, second
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
    # If finished regex everything matched
    try:
        consume(reg_iter)
    except StopIteration:
        return True
    # Otherwise stack was finished before regex e.g. regex=a.b, stack=a,b,b,b
    return False
