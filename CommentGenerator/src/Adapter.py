import json


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
        for key, values in jsonobj.items():
            new_json = {}
            new_json["user_id"] = values["user_id"]
            new_json["time"] = values["time"]
            new_json["type"] = "elementary"
            new_json["details"] = {}

            if "player_active" in values and "id" in values["player_active"] and "value" in values["player_active"]["id"]:
                new_json["details"]["player1"] = values["player_active"]["id"]["value"]
            if "player_passive" in values and "id" in values["player_passive"] and "value" in values["player_passive"]["id"]:
                new_json["details"]["player2"] = values["player_passive"]["id"]["value"]
            if "player_active" in values and "team" in values["player_active"]:
                new_json["details"]["team1"] = values["player_active"]["team"]
            if "player_passive" in values and "team" in values["player_passive"]:
                new_json["details"]["team2"] = values["player_passive"]["team"]
            if "type" in values:
                new_json["details"]["subtype"] = values["type"]

        return new_json


if __name__ == '__main__':
    adapter = Adapter()

    with open("CommentGenerator/assets/input_real1.json", 'r') as input1_json:
        input_json = json.load(input1_json)
        print("INPUT:", input_json)
        jsonobj = adapter.adapt(input_json)
        print("\nFINAL comment:", jsonobj)

    # TODO idea, use a model to rephrase the comment to obtain human readable and grammar spell checks
    # check python paraphrase sentence and evaluate if split correction to paraphrase
