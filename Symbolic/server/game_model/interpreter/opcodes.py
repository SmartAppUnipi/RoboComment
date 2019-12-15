import math
from game_model.game_model import GameModel
from collections import deque
from fuzzy_logic.fuzzy_set import FuzzySet
import numpy as np

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

def clear(stack_name):
    stacks = GameModel.get_env()['stacks']
    stack = stacks[stack_name]
    stack.clear()

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

def _multiple_closest(pos, num):
    ball_x = float(pos['ball'][0]['position']['x'])
    ball_y = float(pos['ball'][0]['position']['y'])

    for player in pos['players']:
        # check that player is not the referee
        if player['team'] != -1:
            x = float(player['position']['x'])
            y = float(player['position']['y'])
            distance = math.sqrt(((ball_x - x)**2)+((ball_y - y)**2))
            player['delta'] = distance


    players = sorted(pos['players'], key=lambda x: x['delta'])
    return players[:num]

def _closest(pos):
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

    return closest

def push_closest(stack_name, pos):
    closest = _closest(pos)
    to_push = {
        'type': 'closest',
        'time': trunc(pos['time']),
        'id': closest['id'],
        'team': closest['team'],
        'position': closest['position']
    }
    push(stack_name, to_push)

def is_pressed(pos):
    closest = _closest(pos)

    threshold = 2
    no_player_in_closest_area = 0

    for player in pos['players']:
        if player['team'] == -1:
            continue
        if player['team'] == closest['team']:
            continue

        d = distance(player['position'], closest['position'])
        if d < 2:
            no_player_in_closest_area += 1

    return no_player_in_closest_area > 1

def push_pressed(stack_name, pos, is_pressed):
    closest = _closest(pos)
    to_push = {
        'type': 'player_pressed' if is_pressed else 'player_not_pressed',
        'start_time': trunc(pos['time']),
        'end_time': trunc(pos['time']),
        'time': trunc(pos['time']),
        'player': closest
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

    ball_pos_x = pos['ball'][0]['position']['x']
    ball_pos_y = pos['ball'][0]['position']['y']

    if (_field_height / 2 - _goal_height / 2) <= ball_pos_y <=  (_field_height / 2 + _goal_height / 2):
        if  0 <= ball_pos_x <= _threshold or _field_width - _threshold <= ball_pos_x <= _field_width:
            return True

    return False

def ball_off_target(pos):
    _field_width = 105
    _field_height = 68

    _goal_height = 7

    ball_pos_x = pos['ball'][0]['position']['x']
    ball_pos_y = pos['ball'][0]['position']['y']

    if (ball_pos_y > (_field_height / 2) + (_goal_height / 2) or ball_pos_y < (_field_height / 2) - (_goal_height / 2)) and (ball_pos_x <= 0):
        return True
    elif (ball_pos_y > (_field_height / 2) + (_goal_height / 2) or ball_pos_y < (_field_height / 2) - (_goal_height / 2)) and (ball_pos_x >= _field_width):
        return True

    return False

def ball_goal(pos):
    _field_width = 105
    _field_height = 68

    _goal_height = 7

    ball_pos_x = pos['ball'][0]['position']['x']
    ball_pos_y = pos['ball'][0]['position']['y']

    if (_field_height / 2 - _goal_height / 2) <= ball_pos_y <=  (_field_height / 2 + _goal_height / 2):
        if  ball_pos_x <= 0 or ball_pos_x >= _field_width:
            return True

    return False

def is_penalty(pos):
    _field_width = 68
    _field_height = 105

    _goal_area_height = 16
    _goal_area_width  = 40

    no_players_in_goal_area = 0
    no_players_out_of_goal_area = 0

    for p in pos['players']:
        if p["team"] == -1: # p is referee
            continue

        x = p["position"]["x"]
        y = p["position"]["y"]

        if 0 <= x <= _goal_area_height and \
           (_field_width / 2 + _goal_area_width / 2 <= y <= \
            _field_width / 2 - _goal_area_width / 2) \
           or _field_height - _goal_area_height >= x and \
           (_field_width / 2 + _goal_area_width / 2 <= y <= \
            _field_width / 2 - _goal_area_width / 2):

            no_players_in_goal_area += 1
            continue

        if _goal_area_height - 2 >= x >= _goal_area_height + 2 or \
           (_goal_area_height - 2) <= _field_height - x <= _goal_area_height + 2:
            no_players_out_of_goal_area += 1

    if no_players_in_goal_area == 2 and no_players_out_of_goal_area >= 4:
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

def _barycenter(array):
    arr = np.asarray(array)
    length = arr.shape[0]
    sum_x = np.sum(arr[:, 0])
    sum_y = np.sum(arr[:, 1])
    return [sum_x/length, sum_y/length]


def compute_bari_diam(stack_name, pos):
    team0 = []
    team1 = []
    for player in pos['players']:
        x = float(player['position']['x'])
        y = float(player['position']['y'])
        current_team = player['team']['value']
        if current_team == 0:
            team0.append([x,y])
        if current_team == 1:
            team1.append([x,y])

    bary0 = _barycenter(team0)
    bary1 = _barycenter(team1)

    diam0 = []
    diam1 = []

    for player in pos['players']:
        x = float(player['position']['x'])
        y = float(player['position']['y'])
        current_team = player['team']['value']
        if current_team == 0:
            distance = math.sqrt(((bary0[0] - x)**2)+((bary0[1] - y)**2))
            diam0.append(distance)
        if current_team == 1:
            distance = math.sqrt(((bary1[0] - x)**2)+((bary1[1] - y)**2))
            diam1.append(distance)

    meanDist0 = np.asarray(diam0).mean()
    meanDist1 = np.asarray(diam1).mean()

    to_push = {
        'type': 'barycenter',
        'position' : {'x': bary0[0], 'y': bary0[1]},
        'time': trunc(pos['time']),
        'team': {'value': 0},
        'mean_distance': {'value': trunc(meanDist0)}
    }
    push(stack_name, to_push)

    to_push = {
        'type': 'barycenter',
        'position' : {'x': bary1[0], 'y': bary1[1]},
        'time': trunc(pos['time']),
        'team': {'value': 1},
        'mean_distance': {'value': trunc(meanDist1)}
    }
    push(stack_name, to_push)

def checkTackle(pos):
    players = _multiple_closest(pos, 2)

    threshold = 0.5
    return players[0]['team'] != players[1]['team'] and distance(players[0]['position'], players[1]['position'] <= threshold) and players[0]['team'] != -1 and players[1]['team'] != -1

def pushTackle(stacks, pos):
    players = _multiple_closest(pos, 2)

    to_push = {
        'type': 'duel',
        'time': trunc(pos['time']),
        'defender': players[0],
        'def_team': players[0]['team'],
        'attacker': players[1],
        'att_team': players[1]['team'],
        'position': players[1]['position']
    }
    for stack in stacks:
        push(stack, to_push)
