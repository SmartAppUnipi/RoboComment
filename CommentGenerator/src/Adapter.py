import json

try:
    from .Filler import Filler
    from .Picker_grammar import Picker
except Exception:
    from Filler import Filler
    from Picker_grammar import Picker

class Adapter:
    def __init__(self):
        # this is only to remember our structure
        self.structure = {
            "user_id": -1,
            "time": {"start": -1,
                     "end": -1
                     },
            "type": "elementary",
            "details": {}
        }

    def adapt(self, jsonobj):
        """
        Transform the input json in a format recognized by our module
        :param jsonobj:
        :return:
        """
        new_json = {}
        new_json["user_id"] = jsonobj["user_id"]

        new_json["time"] = {}
        new_json["time"]["start"] = jsonobj["start_time"]
        new_json["time"]["end"] = jsonobj["end_time"]

        new_json["type"] = "elementary"
        new_json["details"] = {}

        json_keys = jsonobj.keys()

        if "player_active" in json_keys:
            if "id" in jsonobj["player_active"].keys():
                new_json["details"]["player1"] = jsonobj["player_active"]["id"]["value"]
            if "team" in jsonobj["player_active"].keys():
                new_json["details"]["team1"] = jsonobj["player_active"]["team"]
        if "player_passive" in json_keys:
            if "id" in jsonobj["player_active"].keys():
                new_json["details"]["player2"] = jsonobj["player_passive"]["id"]["value"]
            if "team" in jsonobj["player_active"].keys():
                new_json["details"]["team2"] = jsonobj["player_passive"]["team"]

        if "type" in json_keys:
            new_json["details"]["subtype"] = jsonobj["type"]
        
        return new_json

