import re
import json

#TODO use a file for this
template_modifiers = {
    "good" : {
        "simple_modifier" : ["good", "nice"],
        "complex_modifier" : ["what a fantastic action!"] #TODO just an example need better definition
    },
    "bad" : {
        "simple_modifier" : ["bad", "not nice"],
        "complex_modifier" : ["He could have done better ... "]
    }
    # also a neutral bias could be provided
}
class Filler:

    def __init__(self, config=None):
        if config is None:
            self.config = {"user_type" : "" ,"favourite_player" : "", "favourite_team" : ""}
        else:
            with open(config,'r') as conf:
                self.config = json.load(conf)

    def update_comment(self, comment, details):  

        # getting the placeholders {*_modifier} 
        placeholders = re.findall(r'{(.*?)}', comment)
        regex = re.compile(r'\w*_modifier')
        modifiers = [i for i in placeholders if regex.match(i)]

        if len(modifiers) > 0: # there are some modifier placeholders
            # bias allows to pick the right set of modifiers
            bias = "good" if  details['team1'] == self.config['favourite_team'] else "bad"            
            for mod in modifiers:
                # here we require a better picking strategy
                details[mod] = template_modifiers[bias][mod][0]

        comment = comment.format(**details)

        return comment
