from game_model.interpreter.matcher import match
import re

'''
This method picks a pattern (regex) and a stack and matches the pattern on the stack.
The pattern has to be a stack of objects identifying what I expect to find on the stack
An Object may be a generic object to be matched or a wildcard string among the ones defined below
'''

_any = '?'
_anyseq = '.'
#bounded_anyseq = '.{int, int}'
_kleene = '*'
_register = '@'


def consume(iter):
    return next(iter)


def regex_matcher(regex, stack, registers):
    # TODO empty regex always/never match?

    pred_reg = None
    pred_stack = None
    reg_iter = enumerate(regex)
    stack_iter = enumerate(stack)
    for (stack_index, stack_el), (reg_index, reg_el) in zip(stack_iter, reg_iter):
        # Any singleton value is ok, iterate
        if match(reg_el, _any):
            continue

        if type(reg_el) is str:
            # Case '@num', save into registers the element of the stack matched previously
            if re.match('@[0-9]+', reg_el):
                registers[reg_el] = pred_stack
                consume(reg_iter)
            
            # Case '.' or '.{num, num}'
            if re.match('.({[0-9]+,[0-9]+})?', reg_el):
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
                    reg_index, reg_el = consume(reg_iter)
                except StopIteration:
                    # If last is anyseq for sure will match bounded or not
                    return True
                    
                if corpus is None:    
                    # Match any element in stack until I match next
                    while not match(stack_el, reg_el):
                        try:
                            stack_index, stack_el = consume(stack_iter)
                        except StopIteration:
                            # Stack finished, next element not matched
                            return False
                else:
                    # Match any element in stack until I match next
                    count = 0
                    '''Starting with timestamps
                    while True:
                        PASTE FROM BELOW
                        if stack_el['time']-reg_el['time'] >= round(lower/1000):
                            # Reached lower bound for elapsed time
                            break
                        DELETE COUNT
                    TODO Timestamp considered as ms from epoch
                    '''
                    while count < lower:
                        #Consume lower elements (don't care what they are)
                        try:
                            stack_index, stack_el = consume(stack_iter)
                        except StopIteration:
                            # Stack finished, next element not matched
                            return False
                        count+=1
                    
                    '''Starting with timestamps
                    while not match(stack_el, reg_el):
                        PASTE FROM BELOW
                        if stack_el['time']-reg_el['time'] > round(upper/1000):
                            # Matched or surpassed upper bound for time elapsed
                            return False
                        DELETE COUNT
                        DELETE if count > upper BELOW
                    '''
                    while not match(stack_el, reg_el) and count <= upper:
                        #Consume elements until I match or until I am too far
                        try:
                            stack_index,stack_el = consume(stack_iter)
                        except StopIteration:
                            # Stack finished, next element not matched
                            return False
                        count+=1
                    
                    if count > upper:
                        #Next element not found in at most upper steps
                        return False
                # Matched first, any bounded or unbounded sequence, second
                continue    

            if match(reg_el, _kleene) and pred_reg is None:
                raise Exception('Regex starting with kleene')

            '''#TODO Incomplete
            if match(reg_el, _kleene) and pred_reg is not None:
                while match(stack_el, pred_reg):
                    try:
                        stack_el = consume(stack_iter)
                    except StopIteration:
                        continue
            '''

        if not match(stack_el, reg_el):
            # One element did not match
            return False

        pred_reg = reg_el
        # Save reference to previous stack element
        pred_stack = stack[stack_index]
    # May have finished regex or finished stack
    # Check any other element in the regex
    saved = False
    for reg_index, reg_el in reg_iter:
        # If it is any element not string, not matched
        if saved or not isinstance(reg_el, str):
            return False
        # If it is one save in register, do it and continue. The next one will cause not match
        if isinstance(reg_el, str):
            if re.match('@[0-9]+', reg_el):
                registers[reg_el] = pred_stack
                saved = True
    # Regex finished, everything matched
    return True