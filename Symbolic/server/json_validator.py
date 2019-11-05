import schema # https://github.com/keleshev/schema

positions_schema = schema.Schema({
    "players": [
        {
            "x": schema.And(int, lambda x: x >= 0 and x < 100),
            "y": schema.And(int, lambda y: y >= 0 and y < 100),
            schema.Optional("id"): int,
            schema.Optional("team"): schema.And(int, lambda t: t == 1 or t == 2)
        }
    ],
    "ball": [
        {
            "x": schema.And(int, lambda x: x >= 0 and x < 100),
            "y": schema.And(int, lambda y: y >= 0 and y < 100),
            schema.Optional("owner"): int
        }
    ],
    "referee": [
        {
            "x": schema.And(int, lambda x: x >= 0 and x < 100),
            "y": schema.And(int, lambda y: y >= 0 and y < 100),
            schema.Optional("pose"): str 
        }
    ]
})

elem_evt_schema = schema.Schema({
    "type": str,
    "actor": int,
    schema.Optional("actors"): [int],
    "timestamp": int
})

strategy_schema = schema.Schema({
    "type": str,
    "actor": int,
    schema.Optional("actors"): [int],
    "timestamp": int
})

scenario_schema = schema.Schema({
    "type": str,
    "actor": int,
    "timestamp": int
})

class Validator(object):

    @staticmethod
    def validate_positions(to_validate):
        try:
            positions_schema.validate(to_validate)
        except schema.SchemaError as e:
            return False

        return True

    @staticmethod
    def validate_scenario(to_validate):
        try:
            scenario_schema.validate(to_validate)
        except schema.SchemaError as e:
            return False

        return True

    @staticmethod
    def validate_elementary(to_validate):
        try:
            elem_evt_schema.validate(to_validate)
        except schema.SchemaError as e:
            return False

        return True

    @staticmethod
    def validate_strategy(to_validate):
        try:
            strategy_schema.validate(to_validate)
        except schema.SchemaError as e:
            return False

        return True
