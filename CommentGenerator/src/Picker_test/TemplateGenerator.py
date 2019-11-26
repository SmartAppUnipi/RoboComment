import random


class TemplateGenerator:
    """
    Find the most depth path from the keywords passed.
    # TODO add support to nested node in a recursive way
    """

    "Position 0 always phrase for empty, position 1 always position with content"

    def __init__(self):
        self.leaf = {
            "Subject_player":[
                ["a player", ""],
                ["{placeholder}"]
            ],
            "Team_player": [],
            "Action_player": [],
            "Action_zone_from": [],
            "Action_zone_in": [],
            "Receiver_player": [],
            "Team_receiver": []
        }
    def generate(self, sentence_tagged):
        list_comment = []
        for key in sentence_tagged:
            if sentence_tagged[key] == "{empty}":
                # pick from empty random subtemplate
                list_comment.append(random.sample(self.leaf[key][0]))
                # pick from content random subtemplate
            else:
                # and fill the placeholder position with content
                list_comment.append(random.sample(self.leaf[key][1]))

        return list_comment