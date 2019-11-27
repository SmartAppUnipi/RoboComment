# players 22 positions
# ball 1 position

import random
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