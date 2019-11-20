from collections import deque
from matcher import match
from exceptions import EmptyQueueError, InvalidIndexError, NotFoundElementError
from stack import Stack

#We assume rule to be
#Rule {
#   k = Number of elements
#   pattern = list of elements to match
#   newblock(argument): {
#       Instantiate class relative to the rule
#       e.g. Pass rule instantiate PassBlock(argument)
#   }
# }

def generic_matcher(lower_queue, upper_queue, rules):
    if (type(lower_queue) is not Stack):
        raise TypeError
    if (type(upper_queue) is not Stack):
        raise TypeError
    if lower_queue.size() < 1:
        raise EmptyQueueError
    # Match argument rules on lower_queue
    for rule in rules:
        k = rule.k  #ToDo number of elements required by the rule
        if match(lower_queue.get_top_k(k), rule.pattern):
            new_elem = rule.newblock()
    # Push elementary event
    upper_queue.append(new_elem)