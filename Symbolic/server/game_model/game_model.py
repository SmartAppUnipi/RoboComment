from collections import deque
from game_model.parser import parser
from game_model.interpreter import set_rule_matcher

class GameModel:
    def __init__(self):
        self._stacks = {}
        self._rules = []
        with open('rules/rules.txt', 'r') as rules:
            for rule in rules:
                name = rule.split('=')[0].strip()
                if(len(name) > 0):
                    self._stacks[name] = {
                        "stack": deque(),
                        "str": rule
                    }
            
        if ' stdin'not in self._stacks:
            self._stacks['stdin'] = deque()
            a = deque()

    def new_positions(self, positions):
        """This function gets called by the app whenever new positions arrive"""
        self._stacks['stdin'].append(positions)


    def to_comment_generation(self, begin_time, end_time):
        """This method gets called every now and then (I.E. 5 seconds) and it needs 
        to return the list of the rules that matched in the past timeframe
        - begin_time: the game second of the last packet sent
        - end_time: the current game second"""
        #TODO 

    def try_match_loop(self):
        """This is the function that loops indefinitely and tries to match each rule and update the stacks"""
        while True:
            pass
