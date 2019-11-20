from collections import deque
from game_model.exceptions import EmptyQueueError, InvalidIndexError, NotFoundElementError

class Stack:

    def __init__(self):
        self._stack = deque()

    def push(self,v,idx):
        self._stack.insert(idx,v)
    
    def push_front(self,v):
        self._stack.insert(0,v)

    def pop(self,idx):
        if self.size() == 0:
            raise EmptyQueueError('The queue is empty')
        
        if self.size() <= idx:
            raise InvalidIndexError("The element at index {} does not exist".format(idx))
        
        element_removed = self._stack[idx] 
        del self._stack[idx]
        return element_removed
    
    def pop_front(self):
        return self.pop(0)

    def get_stack(self):
        return list(self._stack)
    
    def get(self,idx):
        return list(self._stack)[idx]
    
    def get_top_k(self,idx):
        return list(self._stack)[:idx]

    def size(self):
        return len(self.get_stack())  
    
    def duplicate(self):
        new_stack = Stack()
        for i in reversed(range(len(list(self._stack)))):
            new_stack.push_front(self.get(i))
        return new_stack

    def clear(self):
       for i in range(self.size()):
           self.pop_front()

    def find(self,v):
        idx = 0
        N = self.size()

        while idx < N:
            elem = self.get(idx)
            if elem == v:
                return idx
            else:
                idx += 1
        raise NotFoundElementError("The element is not in the stack")