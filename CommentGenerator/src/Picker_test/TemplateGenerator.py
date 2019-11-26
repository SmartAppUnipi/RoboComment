import random


class TemplateGenerator:

    def __init__(self):
        self.leaf = {
            "Subject_player": {
                "no_empty": ["{p}", "the player"]
            },
            "Team_player": {
                "no_empty": ["of the {p}", "belonging to {p}", ", a {p} player,", ""]
            },
            "Action_player_active": {
                "no_empty": ["do a {p}", "{p}"]
            },
            "Action_player_continue": {
                "no_empty": ["is doing {p}"]
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
            "Team_receiver": {
                "no_empty": ["of the {p} team", ""]
            }
        }

    def generate(self, sentence_tagged):
        sentence_template = {}
        for key, value in sentence_tagged.items():
            # insert or not insert the element with empty
            if value != "{empty}":
                # find the correct sub-template, random
                template = random.sample(self.leaf[key]["no_empty"], 1)[0]
                # substitute with correct word, if action is part of the final comment
                if key == "Action_player_active":
                    value_action = value.replace("{","").replace("}","")
                    template = template.replace("{p}", value_action)
                else:
                    template = template.replace("{p}", value)

                sentence_template[key] = template

        return sentence_template

    def to_comment(self, comment_tagged):
        return ' '.join(comment_tagged.values())