import math
from game_model.game_model import GameModel
from collections import deque
from fuzzy_logic.fuzzy_set import FuzzySet

def push(push_to, element):
    tmp = []
    if not isinstance(push_to, list):
        tmp.append(push_to)
    else:
        tmp = push_to
    stacks = GameModel.get_env()['stacks']
    for stack_name in tmp:
        # If stack does not exist create it
        if stack_name not in stacks.keys():
            # Push as first
            stacks[stack_name] = deque([element])
            continue
        #pdb.set_trace()
        # First element has time smaller
        if len(stacks[stack_name]) < 1 or stacks[stack_name][0]['time'] <= element['time']:
            stacks[stack_name].appendleft(element)
            continue

        # Find position to insert
        for index, obj in enumerate(stacks[stack_name]):
            if obj['time'] < element['time']:
                # Insert element in the correct position
                # After the last element with time greater than it
                stacks[stack_name].insert(index-1, element)
                break
        stacks[stack_name].insert(len(stacks[stack_name])-1, element)

def consume(stack_name, element):
    stacks = GameModel.get_env()['stacks']
    stack = stacks[stack_name]
    stack.remove(element)

def update(stack_name, value, new_entries):
    """changes the value in stack name by updating the entries specified in new_entries"""
    stacks = GameModel.get_env()['stacks']
    stack = stacks[stack_name]
    leng = len(stack)
    idx = stack.index(value)
    old = stack[idx]
    for e in new_entries.keys():
        old[e] = new_entries[e]
    stack[idx] = old

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
                a['time'] = trunc(element['time'])
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
        'time': trunc(pos['time']),
        'id': closest['id'],
        'team': closest['team'],
        'position': closest['position']
    }
    push(stack_name, to_push)

def ball_on_target(pos):
    """
    Compute the position of the ball with respect to the goal

    Pitch dimensions = 105 x 68
    1. Cut it at one half
    """
    _field_width = 105
    _field_height = 68

    _goal_height = 7

    _threshold = 1

    #pos = queue[-1]
    
    ball_pos_x = pos['ball'][0]['position']['x']
    ball_pos_y = pos['ball'][0]['position']['y']

    if (_field_height / 2 - _goal_height / 2) <= ball_pos_y <=  (_field_height / 2 + _goal_height / 2):
        if  0 <= ball_pos_x <= _threshold or _field_width - _threshold <= ball_pos_x <= _field_width:
            return True
    
    return False           

def trunc(a):
    return int(a * 10000) / 10000

def mean(a,b):
    return (a+b)/2

#TODO
def fast_ball(queue):
    pass

def ciao(a):
    pass