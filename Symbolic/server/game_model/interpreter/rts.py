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

def push(stack, element):
    print("=================================================")
    stacks = GameModel.get_env()['stacks']
    # If stack does not exist create it
    if stack not in stacks.keys():
        stacks[stack] = deque()
    stacks[stack].append(element)

def spacchettpush(stack, element):
    registers = GameModel.get_env()['registers']
    push(stack, element)