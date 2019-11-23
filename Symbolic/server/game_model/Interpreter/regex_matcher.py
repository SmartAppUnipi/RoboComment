from matcher import match

'''Regex structure
{
    'pattern': [Object1, Object2, ...],
    'stack': None
}
An Object may be a generic object to be matched or a wildcard among the define below
'''

_any = '?'
_anyseq = '.'
_kleene = '*'


def consume(iter):
    return next(iter)


def regex_matcher(regex, stack):
    # TODO empty regex always/never match?
    # TODO check this assertion
    if len(regex) > len(stack):
        return False

    pred = None
    reg_iter = iter(regex)
    stack_iter = iter(stack)
    for reg_el, stack_el in zip(reg_iter, stack_iter):
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
                lower = corpus[0]
                upper = corpus[1]

            if match(special, _anyseq):
                # Check next element of regex
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
                    while count < int(lower):
                        #Consume lower elements (don't care what they are)
                        try:
                            stack_el = consume(stack_iter)
                        except StopIteration:
                            # Stack finished, next element not matched
                            return False
                        count+=1

                    while not match(stack_el, reg_el) and count <= int(upper):
                        #Consume elements until I match or until I am too far
                        try:
                            stack_el = consume(stack_iter)
                        except StopIteration:
                            # Stack finished, next element not matched
                            return False
                        count+=1

                    if count > int(upper):
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
