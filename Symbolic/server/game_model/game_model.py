from collections import deque
from game_model.parser import parser
from game_model.interpreter import rule_matcher as RM
import game_model.rules.support_methods as support

class GameModel:
    def __init__(self, cg_url):
        """Initializes the game model by parsing the rule file"""
        # initialize queues and global registers
        self._registers = {}
        self._stacks = {}
        self._stacks['stdin'] = deque()
        self._stacks['stdout'] = deque()
        self._stacks['elementary'] = deque()
        self._stacks['scenario'] = deque()
        self._stacks['strategy'] = deque()
                        
        # parse rule file
        self._rules = {}
        with open('game_model/rules/rules.txt', 'r') as rules:
            # every line is a rule
            for rule in rules:
                if(len(rule) > 0):
                    parse_obj = parser.parse(rule)
                    name = parse_obj['name']
                    if 'function' in parse_obj:
                        # it means that the object is a special case
                        function_name = parse_obj['function'].strip()
                        method_to_call = getattr(support, function_name)
                        self._rules[name] = {
                            'type': 'function',
                            'function': method_to_call
                        }
                    else:
                        # this means that it is a regular rule (with action and condition)
                        self._rules[name] = {
                            'type': 'rule', 
                            'condition': parse_obj['condition'], 
                            'action': parse_obj['action']
                        }
                    

    def new_positions(self, positions):
        """This function gets called by the app whenever new positions arrive"""
        self._stacks['stdin'].append(positions)
        for rule in self._rules:
            if rule['type'] == 'function':
                to_call = rule['function']
                ret = to_call(self._stacks['stdin'])
                self._stacks['elementary']
        self.try_match_loop()


    def to_comment_generation(self):
        """This method gets called every now and then (I.E. 5 seconds) and it needs 
        to return the list of the rules that matched in the past timeframe
        - begin_time: the game second of the last packet sent
        - end_time: the current game second"""
        # get the whole stdout output
        to_ret = list(self._stacks['stdout'])
        # clear the stdout for next iteration
        self._stacks['stdout'].clear()
        return to_ret


    def try_match_loop(self):
        """This is the function that loops indefinitely and tries to match each rule and update the stacks"""
        for k, rule in self._rules:
            if rule['type'] != 'function':
                RM.rule_matcher(rule['condition'], rule['action'], self._stacks, self._registers)
