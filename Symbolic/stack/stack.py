from collections import deque

class Stack:

    def __init__(self):
        self._stack = deque()
    
    def push(self,v,idx):  #Ci saranno già immagino push & pop in deque!!!
        print("Push v at index idx")
    
    def pop(self,idx):
        print("Pop element at index idx")
    
    def match(self,patterns):
        print("Match some patterns....")
    
    def duplicate(self):
        print("Duplicate the queue")
    
    def delete(self):
        print("Deleting elements...") #C'è già la pop!!!

    def activate_rule(self,rule):
        print("Launch the rule in some way and modifies the stack...")

    def find(self,v):
        print("Search for an element v in the stack")
    
    