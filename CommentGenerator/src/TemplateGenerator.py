import random


class TemplateGenerator:
    """
    In the leaf variable are stored the leaf possible value corresponding to the leaf defined in the grammar.
    According to user preferences there are two adjective modifier:
        one relative to the preferences like the favourite player
        one relative to the register like a funny commentator
    # mod register change register according to commentator preferences
        # mod preference change adjective according user preference (player or team)
    The file json_grammar will solve you doubt about the node meaning
    """

    def __init__(self):
        self.leaf = {
            "Active_player": {
                "empty": ["A player", "So the player", " A {player_modifier} player therefore,"],
                "no_empty": ["{player_modifier} {p}", "{player_modifier} {p} therefore"]
            },
            "Passive_player": {
                "empty": ["a player", "so the {player_modifier} player", "therefore the player"],
                "no_empty": ["{player_modifier} {p}", "therefore {player_modifier} {p}"]
            },
            "Team_player": {
                "empty" : "",
                "no_empty": ["of the {team_modifier} {p}", "belonging to {team_modifier} {p}", " a {p} player", "of the {p} team", ""]
            },
            "Team_receiver": {
                "empty" : "",
                "no_empty": ["belonging to {p}", "of the {p}", "of the {team_modifier} {p} team", "", " a {p} player"]
            },
            "Action_active": {
                "no_empty": ["do a {simple_modifier} {p}", "perform a {p}", "{p}", "make a {p}"]
            },
            "Action_active_continue": {
                "no_empty": ["keep {p} in a {simple_modifier} way"]
            },
            "Action_active_ball": {
                "no_empty": ["{p} the ball", "execute a {p}", "{p}", "make a {simple_modifier} {p}"]
            },
            "Action_passive": {
                "no_empty": ["receives a {p}", "has a {p}", "obtain a {p}"]
            },
            "Action_passive_continue": {
                "no_empty": ["is receiving a {simple_modifier} {p}", "continuously {p}"]
            },
            "Action_passive_ball": {
                "no_empty": ["{p} the ball", "get a {p}", "do a {p} with the ball"]
            },
            "Action_zone_from": {
                "empty" : [""],
                "no_empty": ["from {p} of the field", "from the {p}", "arrive from {p}"]
            },
            "Action_zone_in": {
                "empty" : [""],
                "no_empty": ["in the {p} of the field", "inside {p} of the field", "cutting the {p} part of the field",
                             "inner {p} part"]
            },
            "Receiver_player": {
                "empty" : ["to another player"],
                "no_empty": ["to {player_modifier} {p}", "towards {p}", "direct to {p}"]
            },
            "Does_player": {
                "empty" : ["by another player"],
                "no_empty": ["from {p}", "by the {player_modifier} player", "by {p}", "coming out of {p}"]
            }
        }

        self.modifier = {
            "register": {
                "neutral": "",
                "happy": "{mod_register_happy}",
                "angry": "{mod_register_angry}",
                "funny": "{mod_register_funny}"
            },
            "preference": {
                "neutral": "",
                "positive": "{mod_preference_positive}",
                "negative": "{mod_preference_negative}"
            }
        }

    def generate(self, sentence_tagged, register, preference):
        sentence_template = {}
        for key, value in sentence_tagged.items():
            
            # The subject is always present even if empty
            if value == "{empty}":
                template = random.choice(self.leaf[key]["empty"])
            else:
                # find the correct sub-template, random
                template = random.choice(self.leaf[key]["no_empty"])
                # substitute with correct word, if action is part of the final comment
                template = template.replace("{p}", value)

            # specialize modifier according to register
            template = template.replace("{mod_register}", self.modifier["register"][register])
            # specialize modifier according to preference
            # template = template.replace("{mod_preference}", self.modifier["preference"][preference])
            # and store the template
            sentence_template[key] = template

        final_comment = self.to_comment(sentence_template)

        return final_comment

    def to_comment(self, comment_tagged):
        return ' '.join(comment_tagged.values())
