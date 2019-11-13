# players 22 positions
# ball 1 position

import random
import pprint
import math


dummy = {
    "players": [],
    "ball": {}
}


def createDummy():
    # Creating players of team A
    for i in range(0, 11):
        dummy['players'].append(
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
        dummy['players'].append(
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

    dummy['ball'].update(
        {
            "position": {
                "x": str("%.2f" % (random.random() * 100)),
                "y": str("%.2f" % (random.random() * 100))
            }
        }
    )

    # pprint.pprint(dummy)


def deltaPlayersBall():
    # returns a list of players ordered by distance from the ball

    retList = []

    ball_x = float(dummy['ball']['position']['x'])
    ball_y = float(dummy['ball']['position']['y'])

    for player in dummy['players']:
        x = float(player['position']['x'])
        y = float(player['position']['y'])
        distance = math.sqrt(((ball_x - x)**2)+((ball_y - y)**2))
        
        retList.append(str(distance) + player['id']['value'])

        # diz = {"distance":str("%.4f" % distance)}
        print(str("%.4f" % distance) + " p:" + player['id']['value'] + " t:" + player['team']['value'])
    

    


def stackOwnership():
    # create the stack of ownership
    return 0


if __name__ == '__main__':
    createDummy()
    deltaPlayersBall()
