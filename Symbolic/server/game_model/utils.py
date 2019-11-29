# players 22 positions
# ball 1 position

import random
import math
import time
import requests
import pprint


#    Pitch dimensions = 105 x 68


pass_time = float(str("%.2f" % (random.random() * 100)))
pass_ball_y = 10
pp = pprint.PrettyPrinter(indent=4)


dummy = {
    "time": 0,
    "user_id": 0,
    "players": [],
    "ball": []
}


def createDummy():

    dummy['time'] = float(str("%.2f" % (random.random() * 100)))
    dummy['user_id'] = 0

    # Creating players of team A
    for i in range(0, 11):
        dummy['players'].append(
            {
                "position": {
                    "x": float(str("%.2f" % (random.random() * 100))),
                    "y": float(str("%.2f" % (random.random() * 100)))
                },
                "id": {
                    "value": i,
                    "confidence": 1
                },
                "team": {
                    "value": 0
                }
            }
        )

    # Creating players of team b
    for i in range(0, 11):
        dummy['players'].append(
            {
                "position": {
                    "x": float(str("%.2f" % (random.random() * 100))),
                    "y": float(str("%.2f" % (random.random() * 100)))
                },
                "id": {
                    "value": i,
                    "confidence": 1
                },
                "team": {
                    "value": 1
                }
            }
        )

    dummy['ball'].append(
        {
            "position": {
                "x": float(str("%.2f" % (random.random() * 100))),
                "y": float(str("%.2f" % (random.random() * 100))),
            },
            "speed": {
                "x": float(str("%.2f" % (random.random() * 100))),
                "y": float(str("%.2f" % (random.random() * 100))),
            }
        }
    )


def simulate_passage():

    global pass_time, pass_ball_y, pp

    tmp = {
        "time": 0,
        "players": [],
        "ball": [], 
        "type": 'PACCHETTONE'
    }

    tmp['time'] = pass_time

    tmp['user_id'] = 0

    tmp['players'].append(
        {
            "position": {
                "x": 10,
                "y": 10
            },
            "id": {
                "value": 0,
                "confidence": 1
            },
            "team": {
                "value": 0
            }
        }
    )

    tmp['players'].append(
        {
            "position": {
                "x": 10,
                "y": 30
            },
            "id": {
                "value": 1,
                "confidence": 1
            },
            "team": {
                "value": 0
            }
        }
    )

    tmp['ball'].append(
        {
            "position": {
                "x": 10,
                "y": pass_ball_y
            },
            "speed": {
                "x": 1,
                "y": 1
            }
        }
    )
    pass_time += 1
    pass_ball_y += 1
    return tmp


if __name__ == '__main__':
    url = "http://127.0.0.1:3001/positions"
    while True:
        pass_ = simulate_passage()
        requests.post(url, json=pass_)
        time.sleep(0.5)
