# players 22 positions
# ball 1 position

import random
import pprint


dummy = {
    "players": [
        # {
        #     "position": {"x": 7.8, "y": 7.9, "confidence": 0},
        #     "speed": {"x": 7.8, "y": 7.9, "confidence": 0},
        #     "id": {"value": 2, "confidence": 1},
        #     "team": {"value": 1, "confidence": 0.1},
        #     "pose": "T-Pose"
        # }
    ],
    "ball": [
        # {
        #     "position": {"x": 7.8, "y": 7.9, "confidence": 0},
        #     "speed": {"x": 7.8, "y": 7.9, "confidence": 0},
        #     "midair": 0.1,
        #     "owner": {"value": 4, "confidence": 0.1},
        #     "owner team": {"value": 0, "confidence": 0.1}
        # }
    ]
}


if __name__ == '__main__':
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

    pprint.pprint(dummy)


def deltaPlayersBall():
    # returns a list of players ordered by distance from the ball

    retList = []
    for player in playersList:
        retList.append(delta(player, ball))


def stackOwnership():
    # create the stack of ownership
    return 0
