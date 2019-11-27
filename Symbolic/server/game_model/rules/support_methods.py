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
    ball_x = float(pos['ball']['position']['x'])
    ball_y = float(pos['ball']['position']['y'])

    for player in pos['players']:
        # check that player is not the referee
        if player['team'] != -1:
            x = float(player['position']['x'])
            y = float(player['position']['y'])
            distance = math.sqrt(((ball_x - x)**2)+((ball_y - y)**2))
            player['delta'] = distance

    return pos


def ball_owner(pos):
    """
        Returns the ball owner given the list of position
    """
    data = __deltaPlayersBall(pos)['players']
    min_delta = min([x['delta'] for x in data])
    closest = data['delta' == min_delta]
    return closest


def ball_on_target(positions):
    """
    Compute the position of the ball with respect to the goal

    Pitch dimensions = 105 x 68
    1. Cut it at one half

    """
