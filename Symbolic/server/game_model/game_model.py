from collections import deque
from game_model.parser import parser
import requests
import re
import json
import threading


class GameModel:

    @staticmethod
    def get_env():
        """returns stacks, registers and rules"""
        return {
            'stacks': U._stacks,
            'registers': U._registers,
            'rules': U._rules
        }

    @staticmethod
    def clean_reg():
        """cleans registers"""
        U._registers = {}

    def __clean_stack(self):
        """cleans stacks"""
        self._stacks = {}
        self._stacks['stdin'] = deque()
        self._stacks['stdout'] = deque()

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

        # parse rule file
        self._rules = []
        rules = self._get_rules_strings('game_model/rules/rules.txt')
        for rule in rules:
            parse_obj = parser.parse(rule)
            name = parse_obj['name']
            self._rules.append({
                'name': name,
                'type': 'rule',
                'condition': parse_obj['condition'],
                'action': parse_obj['action'],
                'constraints': parse_obj['constraints']
            })

    def new_positions(self, positions):
        """This function gets called by the app whenever new positions arrive"""
        self._stacks['stdin'].appendleft(positions)

        # Fields requested by the various groups
        if "user_id" in positions:
            self._user_id = positions['user_id']
        else:
            print("CAREFUL, USER_ID is  not present")
            self._user_id = None

        if "match_id" in positions:
            self._match_id = positions['match_id']
        else:
            print("CAREFUL, MATCH_ID is  not present")
            self._match_id = None

        self._match_url = None
        if "match_url" in positions:
            new_match_url = positions['match_url']
            if self._match_url and new_match_url != self._match_url:
                self.__clean_stack()
            self._match_url = new_match_url
        else:
            print("CAREFUL, MATCH URL is  not present")

    def to_comment_generation(self):
        """This method sends all the retrieved events to comment generation"""
        # get the whole stdout output
        to_send = list(self._stacks['stdout'])
        self._stacks['stdout'].clear()
        t = threading.Thread(target=self.__send_to_cg, args=(to_send,))
        t.start()

    def __send_to_cg(self, to_send):
        for e in to_send:
            jsn = e
            if self._user_id:
                jsn['user_id'] = self._user_id
            if self._match_id:
                jsn['match_id'] = self._match_id
            if self._match_url:
                jsn['match_url'] = self._match_url
            
            if(jsn['type'] != 'positions'):
                    with open("output_log.out", 'a') as out_log:
                        out_log.write(str(jsn) + "\n")
            try:
                x = requests.post(self._cg_url, json=jsn, timeout=1)
            except requests.Timeout:
                print("Unable to write to CommentGeneration: Timeout")
                return


    def _pythonize_rule(self, rule_str):
        """Transforms the rule from JS style (@0.player.id) to python style (@0['player']['id'])"""
        match = re.finditer(r"(\.[a-z|_]+)+", rule_str)

        for x in match:
            js_syntax = x.group()
            py_syntax = "['{}']".format(js_syntax[1:].replace(".", "']['"))
            rule_str = rule_str.replace(x.group(), py_syntax, 1)


        match = re.findall(r"[A-Z][A-Z_]+", rule_str)

        for x in match:
            obj = "{'type': '" + x.lower() + "'}"
            rule_str = rule_str.replace(x, obj)

        return rule_str

    def _get_rules_strings(self, filename):
        """Parse the rules file and build an array of rules strings
        - filename: file name of the rules"""
        rules = []
        with open(filename, 'r') as f:
            prev_rule = ""
            end = False
            while not end:
                next_line = f.readline()
                if next_line.startswith("//"):
                    continue

                if not next_line:
                    if len(prev_rule) > 0:
                        rule_pythonized = self._pythonize_rule(prev_rule.rstrip())
                        rules.append(rule_pythonized)
                    end = True
                else:
                    if not re.match(r'\s', next_line) and len(prev_rule) > 0:
                        rule_pythonized = self._pythonize_rule(prev_rule.rstrip())
                        rules.append(rule_pythonized)
                        prev_rule = next_line.strip()
                    else:
                        prev_rule += " " + next_line.strip()

        return rules


U = GameModel()
