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
            "details":[]
        }

    def adapt(self, jsonobj):
        for key, values in jsonobj.items():
            new_json = {}
            new_json["user_id"] = values["user_id"]
            new_json["time"] = values["time"]
            new_json["type"] = "elementary"
            new_json["details"] = {
                "player1" : values["player_active"]["id"]["value"],
                "team1": values["player_active"]["team"],
                "player2" : values["player_passive"]["id"]["value"],
                "team2": values["player_passive"]["team"],
                "subtype" : values["type"],
                # field zone for now not taken, they pass a relative position
                #"field_zone" : values["position"]
            }

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