import random


class TemplateGenerator:

    def __init__(self):
        self.leaf = {
            "Active_player": {
                "empty" : ["a player"],
                "no_empty": ["{p}"]
            },
            "Passive_player": {
                "empty": ["a player"],
                "no_empty": ["{p}"]
            },
            "Team_player": {
                "no_empty": ["of the {p}", "belonging to {p}", ", a {p} player,", "of the {p} team",""]
            },
            "Action_active": {
                "no_empty": ["do a {p}", "{p}"]
            },
            "Action_active_continue": {
                "no_empty": ["is doing {p}", "continuously {p}"]
            },
            "Action_active_ball": {
                "no_empty": ["{p} the ball", "{p}"]
            },
            "Action_passive": {
                "no_empty": ["receives a {p}", "has a {p}"]
            },
            "Action_passive_continue": {
                "no_empty": ["is receiving {p}", "continuously {p}"]
            },
            "Action_passive_ball": {
                "no_empty": ["receive the ball", "get a {p}"]
            },
            "Action_zone_from": {
                "no_empty": ["from {p} of the field", "from the {p}"]
            },
            "Action_zone_in": {
                "no_empty": ["in the {p} of the field", "inside {p} of the field"]
            },
            "Receiver_player": {
                "no_empty": ["to {p}", "towards the {p}"]
            },
            "Does_player":{
                "no_empty": ["from {p}", "by the player", "by {p}"]
            }
        }

    def generate(self, sentence_tagged):
        sentence_template = {}
        for key, value in sentence_tagged.items():
            # insert or not insert the element with empty
            # The subject is always present
            if key == "Subject_player" and value == "{empty}":
                template = random.choice(self.leaf[key]["empty"])
                sentence_template[key] = template
            else:
                if value != "{empty}":
                    # find the correct sub-template, random
                    template = random.choice(self.leaf[key]["no_empty"])
                    # substitute with correct word, if action is part of the final comment
                    template = template.replace("{p}", value)

                    sentence_template[key] = template

        final_comment = self.to_comment(sentence_template)

        return final_comment

    def to_comment(self, comment_tagged):
        return ' '.join(comment_tagged.values())