from game_model.interpreter.matcher import match as gen_match
import re
import pdb

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
    if len(regex) < 1:
        return True
    pred_reg = None
    pred_stack = None
    reg_iter = enumerate(regex)
    stack_iter = enumerate(stack)
    for (stack_index, stack_el), (reg_index, reg_el) in zip(stack_iter, reg_iter):
        if type(reg_el) is str:
            # Case '@num', save into registers the element of the stack matched previously
            while re.match('@[0-9]+', reg_el):
                if stack_index == 0:
                    # Regex cannot start with '@\d'
                    return False
                registers[reg_el] = stack[stack_index-1]
                try:
                    reg_index, reg_el = consume(reg_iter)
                except:
                    #TODO CHECK
                    return True
                if not isinstance(reg_el, str):
                    break
        if type(reg_el) is str:
            # Any singleton value is ok, iterate
            if gen_match(reg_el, _any):
                continue
            
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
                    # Lower and upper are seconds
                    lower = int(corpus[0])
                    upper = int(corpus[1])

            if gen_match(special, _anyseq):
                # Check next element of regex, look-ahead
                try:
                    reg_index, reg_el = consume(reg_iter)
                except StopIteration:
                    # If last is anyseq for sure will match bounded or not
                    return True
                    
                if corpus is None:    
                    # Match any element in stack until I match next
                    while not gen_match(stack_el, reg_el):
                        try:
                            stack_index, stack_el = consume(stack_iter)
                        except StopIteration:
                            # Stack finished, next element not matched
                            return False
                else:
                    # Match any element in stack until lower seconds have passed
                    if stack_index == 0:
                        start_time = 0
                    else:
                        start_time = stack[stack_index-1]['time']
                    '''Starting with timestamps'''
                    if lower > 0:
                        while True:
                            #Consume lower elements (don't care what they are)
                            try:
                                stack_index, stack_el = consume(stack_iter)
                            except StopIteration:
                                # Stack finished, next element not matched
                                return False

                            if abs(stack_el['time']-start_time) >= lower:
                                # Reached lower bound for elapsed time
                                break
                    if abs(stack_el['time']-start_time) > upper:
                        # Surpassed upper bound for time elapsed
                        return False
                    '''
                    while count < lower:
                        #Consume lower elements (don't care what they are)
                        try:
                            stack_index, stack_el = consume(stack_iter)
                        except StopIteration:
                            # Stack finished, next element not matched
                            return False
                        count+=1
                    '''
                    '''Starting with timestamps'''
                    while not gen_match(stack_el, reg_el):
                        #Consume elements until I match or until I am too far
                        try:
                            stack_index,stack_el = consume(stack_iter)
                        except StopIteration:
                            # Stack finished, next element not matched
                            return False

                        if abs(stack_el['time']-start_time) > upper:
                            # Surpassed upper bound for time elapsed
                            return False
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
                    '''
                # Matched first, any bounded or unbounded sequence, second
                continue    

            if gen_match(reg_el, _kleene) and pred_reg is None:
                raise Exception('Regex starting with kleene')

            '''#TODO Incomplete
            if match(reg_el, _kleene) and pred_reg is not None:
                while match(stack_el, pred_reg):
                    try:
                        stack_el = consume(stack_iter)
                    except StopIteration:
                        continue
            '''

        if not gen_match(stack_el, reg_el):
            # One element did not match
            return False

        pred_reg = reg_el
        # Save reference to previous stack element
        pred_stack = stack[stack_index]
    # May have finished regex or finished stack
    # Check any other element in the regex
    for reg_index, reg_el in reg_iter:
        # If it is any element not string, not matched
        if not isinstance(reg_el, str):
            return False
        # If it is a save do it, otherwise go on
        if isinstance(reg_el, str):
            if re.match('@[0-9]+', reg_el):
                registers[reg_el] = stack[-1]
    # Regex finished, everything matched
    return True