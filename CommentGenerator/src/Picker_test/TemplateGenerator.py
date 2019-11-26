import random


class TemplateGenerator:

    def __init__(self):
        self.leaf = {
            "Subject_player": {
                "empty" : ["the player"],
                "no_empty": ["{p}"]
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
            # The subject is always present
            if key == "Subject_player" and value == "{empty}":
                template = random.sample(self.leaf[key]["empty"], 1)[0]
                sentence_template[key] = template
            else:
                if value != "{empty}":
                    # find the correct sub-template, random
                    template = random.sample(self.leaf[key]["no_empty"], 1)[0]
                    # substitute with correct word, if action is part of the final comment
                    template = template.replace("{p}", value)

                    sentence_template[key] = template

        final_comment = self.to_comment(sentence_template)

        return final_comment

    def to_comment(self, comment_tagged):
        return ' '.join(comment_tagged.values())