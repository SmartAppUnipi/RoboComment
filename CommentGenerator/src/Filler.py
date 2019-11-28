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

    def __init__(self, kb, config=None):
        self.kb = kb
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

        details = self.replace_id_with_names(details)

        comment = comment.format(**details)

        return comment
    
    def replace_id_with_names(self,details):
        def check_and_replace(key,details, get_from_kb):
            if key in details.keys():
                details[key] = get_from_kb(details[key])
            return details
        
        details = check_and_replace('team1', details, self.kb.get_team)
        details = check_and_replace('team2', details, self.kb.get_team)
        details = check_and_replace('player1', details, self.kb.get_player)
        details = check_and_replace('player2', details, self.kb.get_player)
        
        return details
