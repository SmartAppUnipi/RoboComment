from collections import deque
from game_model.parser import parser
from game_model.interpreter import rule_matcher as RM
import game_model.rules.support_methods as support
import requests
import re
import json

class GameModel:

    @staticmethod
    def get_env():
        return U._stacks, U._registers

    def __init__(self):
        """Initializes the game model by parsing the rule file"""
        # some important app wise variables

        with open('../../routes.json', 'r') as f:
            config = json.load(f)
            self._cg_url = config['tale']
        self._user_id = 0

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
        rules = self._get_rules_strings('game_model/rules/rules.txt')
        for rule in rules:
            parse_obj = parser.parse(rule.strip())
            name = parse_obj['name']
            if 'function' in parse_obj:
                # it means that the object is a special case
                function_name = parse_obj['function'].strip()
                method_to_call = getattr(support, function_name)
                self._rules[name] = {
                    'type': 'function',
                    'function': method_to_call, 
                    'stack': parse_obj['stack']
                }
            else:
                # this means that it is a regular rule (with action and condition)
                self._rules[name] = {
                    'type': 'rule', 
                    'condition': parse_obj['condition'], 
                    'action': parse_obj['action'],
                    'constraints': parse_obj['constraints']
                }
                    

    def new_positions(self, positions):
        """This function gets called by the app whenever new positions arrive"""
        self._stacks['stdin'].append(positions)
        self._user_id = positions['user_id']
        for rule in self._rules.values():
            if rule['type'] == 'function':
                to_call = rule['function']
                ret_code, ret_list = to_call(self._stacks[rule['stack']])
                if ret_code:
                    for e in ret_list:
                        self._stacks['elementary'].append(e)
        self.try_match_loop()


    def to_comment_generation(self):
        """This method sends all the retrieved events to comment generation"""
        # get the whole stdout output
        to_send = list(self._stacks['stdout'])
        # clear the stdout for next iteration
        self._stacks['stdout'].clear()
        for e in to_send:
            jsn = e
            jsn['user_id'] = self._user_id
            requests.post(self._cg_url, json=jsn)


    def try_match_loop(self):
        """This is the function that loops indefinitely and tries to match each rule and update the stacks"""
        for rule in self._rules.values():
            if rule['type'] != 'function':
                RM.rule_matcher(rule['condition'], rule['action'], rule['constraints'], self._stacks, self._registers)
        
        self.to_comment_generation()

    def _get_rules_strings(self, filename):
        """Parse the rules file and build an array or rules strings
        - filename: file name of the rules"""
        rules = []
        with open(filename, 'r') as f:
            prev_rule = ""
            end = False
            while not end:
                next_line = f.readline()
                if not next_line:
                    end = True
                else:
                    if not re.match(r'\s', next_line) and len(prev_rule) > 0:
                        rules.append(prev_rule.rstrip())
                        prev_rule = next_line.strip()
                    else:
                        prev_rule += next_line.strip()

            rules.append(prev_rule.strip())
            for e in rules:
                print("a->", e)
        return rules

U = GameModel()