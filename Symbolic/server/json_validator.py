from schema import Schema, And, Or, Use, Optional, SchemaError
# https://github.com/keleshev/schema

# Video Processing JSON

uncertain_float_schema = Schema({
    "value": float,
    "confidence": And(float, lambda x: x >= 0 and x <= 1)
})

uncertain_int_schema = Schema({
    "value": int,
    "confidence": And(float, lambda x: x >= 0 and x <= 1)
})

uncertain_zero_one_schema = Schema({
    "value": And(int, lambda x: x == 0 or x == 1),
    "confidence": And(float, lambda x: x >= 0 and x <= 1)
})

coordinate_schema = Schema({
    "x": float,
    "y": float,
    "confidence": And(float, lambda x: x >= 0 and x <= 1)
})

coordinate_3D_schema = Schema({
    "x": float,
    "y": float,
    "z": float
})

positions_schema = Schema({
    Optional("camera"): {
        "position": Use(lambda x: coordinate_3D_schema.validate(x)),
        "target": Use(lambda x: coordinate_schema.validate(x)),
        "zoom": float
    },
    "players": [
        {
            "position": Use(lambda x: coordinate_schema.validate(x)),
            "speed": Use(lambda x: coordinate_schema.validate(x)),
            "id": Use(lambda x: uncertain_int_schema.validate(x)),
            "team": Use(lambda x: uncertain_zero_one_schema.validate(x)),
        }
    ],
    "ball": [
        {
            "position": Use(lambda x: coordinate_schema.validate(x)),
            "speed": Use(lambda x: coordinate_schema.validate(x)),
            "midair": And(float, lambda x: x >= 0 or x <= 1),
            "owner": Use(lambda x: uncertain_int_schema.validate(x)),
            "owner team": Use(lambda x: uncertain_zero_one_schema.validate(x)),
        }
    ],
    "referee": [
        {
            "position": Use(lambda x: coordinate_schema.validate(x)),
            "pose": str
        }
    ]
})

# Comment generation JSON

event_types = ["elementary", "scenario", "strategy"]
elementary = ["pass","shot","holderMove","move","possession","cross","foul","duel","clearance","possession_lost","interception"]
scenario = ["penalty","corner","offside","throwin","kickoff","free_kick","half_time","end_of_game"]
strategy = ["counter-attack","melina","catenaccio","defence","attack"]

event_schema = Schema({
    "time" : {
        "start": And(int, lambda x: x >= 0),
        "end": And(int, lambda x: x >= 0) 
    },
    "type": And(str, Use(lambda x : x in event_types)),
    "details":
    {
        "team1": str,
        "team2": str,
        "player1": str,
        "player2": str,
        "field-zone": str,
        "subtype": And(str, lambda x: x in elementary or x in scenario or x in strategy),
        "confidence": And(float, lambda x: x >= 0 and x <= 1)
    }
})

class Validator(object):

    @staticmethod
    def validate_positions(to_validate):
        try:
            positions_schema.validate(to_validate)
        except SchemaError as e:
            return False

        return True

    @staticmethod
    def validate_event(to_validate):
        try:
            event_schema.validate(to_validate)
        except SchemaError as e:
            return False

        return True
