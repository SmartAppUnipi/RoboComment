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
                "empty": ["A {player_modifier} player", "look at the player"],
                "no_empty": ["A {player_modifier} player", "A player", "look at {p}"]
            },
            "Passive_player": {
                "empty": ["A {player_modifier} player"],
                "no_empty": ["{player_modifier} {p}", "therefore {player_modifier} {p}", "therefore, {p}"]
            },
            "Receiver_player":{
                "empty": ["towards a player"],
                "no_empty": ["towards a {player_modifier} {p}", "towards a player"]
            },
            "Action_active_continue_ball":{
                "no_empty": ["maintain the {p}", "do {simple_modifier} {p}"]
            },
            "Action_active_ball":{
                "no_empty": ["do a {simple_modifier} {p}", "makes a {simple_modifier} {p}", "makes a {p}"]
            },
            "Does_player":{
                "empty": ["by a {player_modifier} player"],
                "no_empty": ["from {player_modifier} {p}", "by {player_modifier} {p}"]
            },
            "Action_passive_ball":{
                "no_empty": ["receives a {simple_modifier} {p}", "obtain {simple_modifier} {p}"]
            },
            "Team_player":{
                "no_empty": ["playing in {p}", "a {team_modifier} {p} ", ""]
            },
            "Team_receiver":{
                "no_empty": ["playing in {p}", "a {team_modifier} {p} player", ""]
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
