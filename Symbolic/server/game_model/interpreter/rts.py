from game_model.game_model import GameModel
from collections import deque
import re
import json
import pdb
import math

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
    for key in sorted(element):
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

def distance(a, b):
    ax = float(a['x'])
    ay = float(a['y'])
    bx = float(b['x'])
    by = float(b['y'])
    distance = math.sqrt(((ax - bx)**2)+((ay - by)**2))
    return distance

def push_closest(stack_name, pos):
    ball_x = float(pos['ball'][0]['position']['x'])
    ball_y = float(pos['ball'][0]['position']['y'])

    for player in pos['players']:
        # check that player is not the referee
        if player['team'] != -1:
            x = float(player['position']['x'])
            y = float(player['position']['y'])
            distance = math.sqrt(((ball_x - x)**2)+((ball_y - y)**2))
            player['delta'] = distance
    
    min_delta = min([a['delta'] for a in pos['players']])

    closest = None
    for player in pos['players']:
        current = player['delta']
        if (current == min_delta):
            closest = player

    to_push = {
        'type': 'closest',
        'time': pos['time'],
        'id': closest['id'],
        'team': closest['team'],
        'position': closest['position']
    }
    push(stack_name, to_push)