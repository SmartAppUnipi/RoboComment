# players 22 positions
# ball 1 position

import random
import math
import time
import requests
import pprint
import json
import sys

#    Pitch dimensions = 105 x 68


pass_time = float(str("%.2f" % (random.random() * 100)))
pass_ball_y = 20
direction = 'down'
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


def simulate_passage(x):

    global pass_time, pass_ball_y, pp, direction

    tmp = {
        "time": 0,
        "players": [],
        "ball": [], 
        "type": 'PACCHETTONE'
    }

    tmp['time'] = pass_time

    tmp['user_id'] = 0

    #REFREE
    tmp['players'].append(
        {
            "position": {
                "x": x - 10,
                "y": (0 + x/2)
            },
            "id": {
                "value": 99,
                "confidence": 1
            },
            "team": {
                "value": -1
            },
            "pose": ""
        }
    )


    tmp['players'].append(
        {
            "position": {
                "x": x,
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
                "x": x,
                "y": 20
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

    tmp['players'].append(
        {
            "position": {
                "x": x,
                "y": 30
            },
            "id": {
                "value": 2,
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
                "x": x,
                "y": 40
            },
            "id": {
                "value": 3,
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
                "x": x,
                "y": 50
            },
            "id": {
                "value": 4,
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
                "x": x + 20,
                "y": 25
            },
            "id": {
                "value": 11,
                "confidence": 1
            },
            "team": {
                "value": 1
            }
        }
    )

    tmp['players'].append(
        {
            "position": {
                "x": x + 20,
                "y": 35
            },
            "id": {
                "value": 12,
                "confidence": 1
            },
            "team": {
                "value": 1
            }
        }
    )

    tmp['players'].append(
        {
            "position": {
                "x": x + 20,
                "y": 45
            },
            "id": {
                "value": 13,
                "confidence": 1
            },
            "team": {
                "value": 1
            }
        }
    )



    tmp['ball'].append(
        {
            "position": {
                "x": x,
                "y": pass_ball_y
            },
            "speed": {
                "x": 1,
                "y": 1
            }
        }
    )
    pass_time += 0.05

    if pass_ball_y < 50 and direction == 'down':
        pass_ball_y += 1
    elif pass_ball_y == 50 and direction == 'down':
        pass_ball_y -= 1
        direction = 'up'
    elif pass_ball_y > 10 and direction == 'up':
        pass_ball_y -= 1
    else:
        pass_ball_y += 1
        direction = 'down'
    return tmp



url = "http://127.0.0.1:3001/positions"
if len(sys.argv) > 1:
    file_to_open = sys.argv[1]
    with open(file_to_open) as json_file:
        pos = json.load(json_file)
    for pass_ in pos:
        requests.post(url, json=pass_)
        time.sleep(0.25)
else:    
    #shot on target and goal
    pass_ball_y = 10

    #shot off target
    # pass_ball_y = 20

    x_ = 0
    for i in range(0,105):
        if (i < 40):
            x_ += 1
            pass_ = simulate_passage(x_)
            requests.post(url, json=pass_)
            time.sleep(0.1)
            
        else:
            x_ += 1
            pass_ = simulate_passage(x_)
            requests.post(url, json=pass_)
            time.sleep(0.1)

