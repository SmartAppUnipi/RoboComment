import json
import pprint
dummy = [

    #JSON NUMBER 1
    {
                "time": 37.5,
                "camera": {
                    "position": {"x": 1.2, "y": 1.3, "z": 8.8},
                    "target": {"x": 7.8, "y": 7.9, "confidence": 0},
                    "zoom": 0.5
                },
                "players": [

                     {
                        "position": {"x": 2, "y": 45, "confidence": 0},
                        "speed": {"x": 40, "y": 69, "confidence": 0},
                        "id": {"value": 1,"confidence": 1},
                        "team": {"value": 0,"confidence": 1},
                        "pose": "T-Pose"
                    },

                    {
                        "position": {"x": 21, "y": 7.9, "confidence": 0},
                        "speed": {"x": 40, "y": 69, "confidence": 0},
                        "id": {"value": 2,"confidence": 1},
                        "team": {"value": 0,"confidence": 0.6},
                        "pose": "T-Pose"
                    },

                      {
                        "position": {"x": 20, "y": 80, "confidence": 0},
                        "speed": {"x": 10, "y": 10, "confidence": 0},
                        "id": {"value": 3,"confidence": 1},
                        "team": {"value": 0,"confidence": 1},
                        "pose": "T-Pose"
                    },

                      {
                        "position": {"x": 14, "y": 55, "confidence": 0},
                        "speed": {"x": 40, "y": 75, "confidence": 0},
                        "id": {"value": 4,"confidence": 1},
                        "team": {"value":0,"confidence": 1},
                        "pose": "T-Pose"
                    },
                    
                    {
                        "position": {"x": 14, "y": 35, "confidence": 0},
                        "speed": {"x": 40, "y": 75, "confidence": 0},
                        "id": {"value": 5,"confidence": 1},
                        "team": {"value":0,"confidence": 1},
                        "pose": "T-Pose"
                    },

                     {
                        "position": {"x": 52, "y": 45, "confidence": 0},
                        "speed": {"x": 10, "y": 10, "confidence": 0},
                        "id": {"value": 6,"confidence": 1},
                        "team": {"value": 0,"confidence": 1},
                        "pose": "T-Pose"
                    },

                    {
                        "position": {"x": 56, "y": 20, "confidence": 0},
                        "speed": {"x": 10, "y": 10, "confidence": 0},
                        "id": {"value": 7,"confidence": 1},
                        "team": {"value": 0,"confidence": 1},
                        "pose": "T-Pose"
                    },

                        {
                        "position": {"x": 56, "y": 80, "confidence": 0},
                        "speed": {"x": 10, "y": 10, "confidence": 0},
                        "id": {"value": 8,"confidence": 1},
                        "team": {"value": 0,"confidence": 1},
                        "pose": "T-Pose"
                    },
                    
                      {
                        "position": {"x": 90, "y": 45, "confidence": 0},
                        "speed": {"x": 40, "y": 69, "confidence": 0},
                        "id": {"value": 9,"confidence": 1},
                        "team": {"value": 0,"confidence": 0.6},
                        "pose": "T-Pose"
                    },

                      {
                        "position": {"x": 94, "y": 20, "confidence": 0},
                        "speed": {"x": 7.8, "y": 7.9, "confidence": 0},
                        "id": {"value": 10,"confidence": 0.6},
                        "team": {"value": 0,"confidence": 0.8},
                        "pose": "T-Pose"
                    },

                     {
                        "position": {"x": 95, "y": 80, "confidence": 0},
                        "speed": {"x": 7.8, "y": 7.9, "confidence": 0},
                        "id": {"value": 11,"confidence": 0.6},
                        "team": {"value": 0,"confidence": 0.8},
                        "pose": "T-Pose"
                    },
                    

                  
                 

                #----------------------------------------------------------------------
                    {
                        "position": {"x": 107, "y": 45, "confidence": 0},
                        "speed": {"x": 40, "y": 75, "confidence": 0},
                        "id": {"value": 1,"confidence": 1},
                        "team": {"value":1,"confidence": 1},
                        "pose": "T-Pose"
                    },

                     {
                        "position": {"x": 94, "y": 45, "confidence": 0},
                        "speed": {"x": 40, "y": 75, "confidence": 0},
                        "id": {"value": 2,"confidence": 1},
                        "team": {"value":1,"confidence": 1},
                        "pose": "T-Pose"
                    },

                     {
                        "position": {"x": 95, "y": 10, "confidence": 0},
                        "speed": {"x": 40, "y": 75, "confidence": 0},
                        "id": {"value": 3,"confidence": 1},
                        "team": {"value":1,"confidence": 1},
                        "pose": "T-Pose"
                    },

                       {
                        "position": {"x": 96, "y": 73, "confidence": 0},
                        "speed": {"x": 40, "y": 75, "confidence": 0},
                        "id": {"value": 4,"confidence": 1},
                        "team": {"value":1,"confidence": 1},
                        "pose": "T-Pose"
                    },

                      {
                        "position": {"x": 60, "y": 33, "confidence": 0},
                        "speed": {"x": 40, "y": 75, "confidence": 0},
                        "id": {"value": 5,"confidence": 1},
                        "team": {"value":1,"confidence": 1},
                        "pose": "T-Pose"
                    },

                     {
                        "position": {"x": 60, "y": 53, "confidence": 0},
                        "speed": {"x": 40, "y": 75, "confidence": 0},
                        "id": {"value": 6,"confidence": 1},
                        "team": {"value":1,"confidence": 1},
                        "pose": "T-Pose"
                    },

                     {
                        "position": {"x": 47, "y": 13, "confidence": 0},
                        "speed": {"x": 4, "y": 75, "confidence": 0},
                        "id": {"value": 7,"confidence": 1},
                        "team": {"value":1,"confidence": 1},
                        "pose": "T-Pose"
                    },

                     {
                        "position": {"x": 44, "y": 45, "confidence": 0},
                        "speed": {"x": 40, "y": 75, "confidence": 0},
                        "id": {"value": 8,"confidence": 1},
                        "team": {"value":1,"confidence": 1},
                        "pose": "T-Pose"
                    },

                     {
                        "position": {"x": 48, "y": 73, "confidence": 0},
                        "speed": {"x": 40, "y": 75, "confidence": 0},
                        "id": {"value": 9,"confidence": 1},
                        "team": {"value":1,"confidence": 1},
                        "pose": "T-Pose"
                    },

                    {
                        "position": {"x": 16, "y": 28, "confidence": 0},
                        "speed": {"x": 40, "y": 75, "confidence": 0},
                        "id": {"value": 10,"confidence": 1},
                        "team": {"value":1,"confidence": 1},
                        "pose": "T-Pose"
                    },

                    {
                        "position": {"x": 16, "y": 62, "confidence": 0},
                        "speed": {"x": 40, "y": 75, "confidence": 0},
                        "id": {"value": 11,"confidence": 1},
                        "team": {"value":1,"confidence": 1},
                        "pose": "T-Pose"
                    },
                       {
                        "position": {"x": 55, "y": 37, "confidence": 0},
                        "speed": {"x": 7.8, "y": 7.9, "confidence": 0},
                        "id": {"value": 4,"confidence": 0.8},
                        "team": {"value": -1,"confidence": 0.8},
                        "pose": "T-Pose"
                    },

                 

                ],
                "ball": [
                    {
                        "position": {"x": 55, "y": 45, "confidence": 0},
                        "speed": {"x": 7.8, "y": 7.9, "confidence": 0},
                        "midair": 0.1,
                        "owner": {"value": 4,"confidence": 0.1},
                        "owner team": {"value": 0,"confidence": 0.1}
                    }
                ]
            }            
]

pp = pprint.PrettyPrinter(indent=4)

def move_player(target_dict,id,team,dx,dy):
    players = target_dict['players']

    for p in players:
        if p['team']['value'] == team and p['id']['value'] == id:
            p['position']['x'] = p['position']['x'] + dx
            p['position']['y'] = p['position']['y']+ dy

    return target_dict

def move_ball(target_dict,dx,dy):
    ball = target_dict['ball'][0]
    ball['position']['x'] += dx
    ball['position']['y'] += dy
   
    return target_dict

def modify_id_confidence(target_dict,id,team,conf):
     players = target_dict['players']
     for p in players:
        if p['team']['value'] == team and p['id']['value'] == id:
            p['id']['confidence'] = conf
            return target_dict

def modify_team_confidence(target_dict,id,team,conf):
     players = target_dict['players']
     for p in players:
        if p['team']['value'] == team and p['id']['value'] == id:
            p['team']['confidence'] = conf
            return target_dict