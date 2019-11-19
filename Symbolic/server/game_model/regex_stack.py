from stack import Stack

class RegexStack:
    def __init__(self):
        self._stack = Stack()

    def to_string(self, idx):
        """returns a string describing all the cells in the stack from idx up"""
        if idx == 0: # last element
            return ""
        else: 
            rule = self._stack().get(idx)
            # recursive case, do the same but for the one element closer to the top of the stack
            return rule.description_str() + "(" + self.to_string(idx-1) + ")" 

    def match(self, rule):
        matched = True
        for i in range(rule.size(), 0, -1):
            if not rule.match(self._stack.get(i)):
                matched = False

    def consume(self, idx, new_rule = None):
        for i in range(0, idx):
            self._stack.pop_front()
        if new_rule:
            self._stack.push_front(new_rule)
