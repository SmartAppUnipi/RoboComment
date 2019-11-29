import math
import random

# TODO
# Retrieve those methods
# possession      = ___ball_owner
# ballOnTarget    = ___ball_on_target
# ballOffTarget   = ___ball_off_target
# fastBall        = ___fast_ball


def __deltaPlayersBall(pos):
    """
        Returns a list of players with delta wrt the ball
    """
    ball_x = float(pos['ball'][0]['position']['x'])
    ball_y = float(pos['ball'][0]['position']['y'])

    for player in pos['players']:
        # check that player is not the referee
        if player['team'] != -1:
            x = float(player['position']['x'])
            y = float(player['position']['y'])
            distance = math.sqrt(((ball_x - x)**2)+((ball_y - y)**2))
            player['delta'] = distance

    return pos


def ball_owner(queue):
    """
        Returns the ball owner given the list of position
    """
    threshold = 1
    pos = queue[-1]
    data = __deltaPlayersBall(pos)['players']
    min_delta = min([x['delta'] for x in data])
    
    closest = None
    for player in data:
        current = player['delta']
        if (current == min_delta) and (current < threshold):
            closest = player

    return closest


def ball_on_target(queue):
    """
    Compute the position of the ball with respect to the goal

    Pitch dimensions = 105 x 68
    1. Cut it at one half
    """
    _field_width = 105
    _field_height = 68

    _goal_height = 7

    _threshold = 2

    pos = queue[-1]
    
    ball_pos_x = pos['ball'][0]['position']['x']
    ball_pos_y = pos['ball'][0]['position']['y']

    if (_field_height / 2 - _goal_height / 2) <= ball_pos_y <=  (_field_height / 2 + _goal_height / 2):
        if  0 <= ball_pos_x <= _threshold or _field_width - _threshold <= ball_pos_x <= _field_width:
            return True
    
    return False           


    
