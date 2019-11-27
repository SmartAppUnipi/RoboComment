import math
import random

# TODO
# Retrieve those methods
# possession      = ___ball_owner
# ballOnTarget    = ___ball_on_target
# ballOffTarget   = ___ball_off_target
# fastBall        = ___fast_ball


_dummy = {
    "players": [],
    "ball": {}
}


def _deltaPlayersBall(pos=None):
    # returns a list of players ordered by distance from the ball

    if not pos:
        pos = _dummy

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


def _create_dummy():
    # Creating players of team A
    for i in range(0, 11):
        _dummy['players'].append(
            {
                "position": {
                    "x": str("%.2f" % (random.random() * 100)),
                    "y": str("%.2f" % (random.random() * 100))
                },
                "id": {
                    "value": str(i)
                },
                "team": {
                    "value": "0"
                }
            }
        )

    # Creating players of team b
    for i in range(0, 11):
        _dummy['players'].append(
            {
                "position": {
                    "x": str("%.2f" % (random.random() * 100)),
                    "y": str("%.2f" % (random.random() * 100))
                },
                "id": {
                    "value": str(i)
                },
                "team": {
                    "value": "1"
                }
            }
        )

    _dummy['ball'].update(
        {
            "position": {
                "x": str("%.2f" % (random.random() * 100)),
                "y": str("%.2f" % (random.random() * 100))
            }
        }
    )

    # pprint.pprint(_dummy)


def ball_owner(pos):
    data = _deltaPlayersBall(pos)['players']
    
    min = math.inf
    for player in data:
        if player['delta'] < min:
            min = player['delta']
    
    closest = data['delta' == min]

    return closest


def ___ball_on_target(positions):
    """
    Compute the position of the ball with respect to the goal

    Pitch dimensions = 105 x 68
    1. Cut it at one half

    """


if __name__ == '__main__':
    _create_dummy()
    ball_owner(_dummy)

