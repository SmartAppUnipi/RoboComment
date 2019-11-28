import random


class TemplateGenerator:
    """
    In the leaf variable are stored the leaf possible value corresponding to the leaf defined in the grammar.
    The file json_grammar will solve you doubt about the node meaning
    """
    def __init__(self):
        self.leaf = {
            "Active_player": {
                "empty": ["a player", "so the player", " a player therefore,"],
                "no_empty": ["{p}", "{p} therefore,"]
            },
            "Passive_player": {
                "empty": ["a player", "so the player", "therefore the player"],
                "no_empty": ["{p}", "therefore {p}"]
            },
            "Team_player": {
                "no_empty": ["of the {p}", "belonging to {p}", " a {p} player", "of the {p} team", ""]
            },
            "Team_receiver": {
                "no_empty": ["belonging to {p}", "of the {p}", "of the {p} team", "", " a {p} player"]
            },
            "Action_active": {
                "no_empty": ["do a {p}", "perform a {p}", "{p}", "make a {p}"]
            },
            "Action_active_continue": {
                "no_empty": ["is doing {p}", "continuously {p}", "keep doing {p}"]
            },
            "Action_active_ball": {
                "no_empty": ["{p} the ball", "execute a {p}", "{p}", "make a {p}"]
            },
            "Action_passive": {
                "no_empty": ["receives a {p}", "has a {p}", "obtain a {p}"]
            },
            "Action_passive_continue": {
                "no_empty": ["is receiving {p}", "continuously {p}"]
            },
            "Action_passive_ball": {
                "no_empty": ["receive the ball", "get a {p}", "obtain the ball"]
            },
            "Action_zone_from": {
                "no_empty": ["from {p} of the field", "from the {p}", "arrive from {p}"]
            },
            "Action_zone_in": {
                "no_empty": ["in the {p} of the field", "inside {p} of the field", "cutting the {p} part of the field", "inner {p} part"]
            },
            "Receiver_player": {
                "no_empty": ["to {p}", "towards {p}", "direct to {p}"]
            },
            "Does_player": {
                "no_empty": ["from {p}", "by the player", "by {p}", "coming out of {p}"]
            }
        }

    def generate(self, sentence_tagged):
        sentence_template = {}
        for key, value in sentence_tagged.items():
            # insert or not insert the element with empty
            # The subject is always present
            if key == "Active_player" and value == "{empty}" or key == "Passive_player" and value == "{empty}":
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
