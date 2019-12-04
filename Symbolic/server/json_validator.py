from schema import Schema, And, Or, Use, Optional, SchemaError
import json
# https://github.com/keleshev/schema

# Video Processing JSON

uncertain_number_schema = Schema({
    "value": Or(int, float),
    Optional("confidence"): And(Or(int, float))
})

uncertain_string_schema = Schema({
    "value": str,
    Optional("confidence"): And(Or(int, float))
})

coordinate_schema = Schema({
    "x": Or(int, float),
    "y": Or(int, float),
    Optional("confidence"): And(Or(int, float), lambda x: x >= 0 and x <= 1)
})

coordinate_3D_schema = Schema({
    "x": Or(int, float),
    "y": Or(int, float),
    "z": Or(int, float)
})

positions_schema = Schema({
    "user_id": Or(int, str),
    "time": And(Or(float, int), lambda t: t >= 0),
    Optional("camera"): {
        "position": Use(lambda x: coordinate_3D_schema.validate(x)),
        "target": Use(lambda x: coordinate_schema.validate(x)),
        "zoom": Or(int, float)
    },
    "players": [
        {
            "position": Use(lambda x: coordinate_schema.validate(x)),
            Optional("speed"): Use(lambda x: coordinate_schema.validate(x)),
            "id": Use(lambda x: uncertain_number_schema.validate(x)),
            "team": Use(lambda x: uncertain_number_schema.validate(x)),
            Optional("pose"): str
        }
    ],
    "ball": [
        {
            "position": Use(lambda x: coordinate_schema.validate(x)),
            "speed": Use(lambda x: coordinate_schema.validate(x)),
            Optional("midair"): Use(lambda x: uncertain_string_schema.validate(x)),
            Optional("owner"): Use(lambda x: uncertain_number_schema.validate(x)),
            Optional("owner team"): Use(lambda x: uncertain_number_schema.validate(x)),
        }
    ],
})

# Comment generation JSON

event_types = ["elementary", "scenario", "strategy"]
elementary = ["pass","shot","holderMove","move","possession","cross","foul","duel","clearance","possession_lost","interception"]
scenario = ["penalty","corner","offside","throwin","kickoff","free_kick","half_time","end_of_game"]
strategy = ["counter-attack","melina","catenaccio","defence","attack"]

event_schema = Schema({
    "time" : {
        "start": And(Or(int, float), lambda x: x >= 0),
        "end": And(Or(int, float), lambda x: x >= 0) 
    },
    "type": And(str, Use(lambda x : x in event_types)),
    "details":
    {
        "team1": str,
        "team2": str,
        "player1": str,
        "player2": str,
        "field_zone": str,
        "subtype": And(str, lambda x: x in elementary or x in scenario or x in strategy),
        "confidence": And(Or(int, float), lambda x: x >= 0 and x <= 1)
    }
})

class Validator(object):

    @staticmethod
    def validate_positions(to_validate):
        try:
            positions_schema.validate(to_validate)
        except SchemaError as e:
            print(e)
            return False

        return True

    @staticmethod
    def validate_event(to_validate):
        try:
            event_schema.validate(to_validate)
        except SchemaError as e:
            return False

        return True