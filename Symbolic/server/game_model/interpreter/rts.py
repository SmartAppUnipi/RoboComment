from game_model.game_model import GameModel
from collections import deque
import re
import json
import pdb

def _resolve_placeholders(s):
    registers = GameModel.get_env()['registers']
    for param in re.findall(r'@\d', s):
        s = s.replace(param, json.dumps(registers[param]))
    return s

def check(constraints):
    if len(constraints) < 1:
        return True
    constraints_prime = _resolve_placeholders(constraints)
    registers = GameModel.get_env()['registers']
    return eval(constraints_prime)

def fire(actions):
    actions_prime = _resolve_placeholders(actions)
    stacks = GameModel.get_env()['stacks']
    registers = GameModel.get_env()['registers']
    eval(actions_prime)

def push(push_to, element):
    tmp = []
    if not isinstance(push_to, list):
        tmp.append(push_to)
    else:
        tmp = push_to
    stacks = GameModel.get_env()['stacks']
    # If stack does not exist create it
    for stack_name in tmp:
        if stack_name not in stacks.keys():
            stacks[stack_name] = deque()
        stacks[stack_name].appendleft(element)

def spacchettpush(stack, element):
    for key in element:
        value = element[key]
        if isinstance(value, list):
            for e in value:
                a = e
                if key == 'players':
                    a['type'] = 'player'
                else:
                    a['type'] = key
                a['time'] = element['time']
                push(stack, a)