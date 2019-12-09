import re
import json

#TODO use a file for this
template_modifiers = {
    "good" : {
        "simple_modifier" : ["good", "nice"],
        "complex_modifier" : ["what a fantastic action!"], #TODO just an example need better definition
        "player_modifier" : ["skilled"],
        "team_modifier" : ["supreme"]
    },
    "bad" : {
        "simple_modifier" : ["bad", "not nice"],
        "complex_modifier" : ["He could have done better ... "],
        "player_modifier" : ["banana-footed"],
        "team_modifier" : ["awful"]
    }
    # also a neutral bias could be provided
}
class Filler:

    def __init__(self, kb):
        self.__kb = kb


    def update_comment(self, comment:str, placeholders:dict)->str:
        """
        Update commet with placeholders value, querying the kb
        :param comment:
        :param placeholders:
        :return:
        """

        for placeh in placeholders:
            new_value = "ERROR"
            if placeh == 'player1' or placeh == 'player2':
                pass
                #new_value = self.__kb.get_player(placeholders[placeh])
            elif placeh == 'team1' or placeh == 'team2':
                pass
                #new_value = self.__kb.get_team(placeholders[placeh])

            comment = comment.replace("{"+placeh+"}", str(new_value))

        """

        # getting the placeholders {*_modifier} 
        placeholders = re.findall(r'{(.*?)}', comment)
        regex = re.compile(r'\w*_modifier')
        modifiers = [i for i in placeholders if regex.match(i)]

        details = self.replace_id_with_names(details)
        user_team = self.kb.get_user_team(user_id)
        
        # BUGFIX
        details[details['subtype']] = details['subtype']
        if 'field_zone' in details.keys():
            details[details['field_zone']] = details['field_zone']


        if len(modifiers) > 0: # there are some modifier placeholders
            # bias allows to pick the right set of modifiers
            bias = "good" if  details['team1'] == user_team else "bad"            
            for mod in modifiers:
                # here we require a better picking strategy
                details[mod] = template_modifiers[bias][mod][0]

        comment = comment.format(**details)
        
        """

        return comment

    """
    def replace_id_with_names(self,details):
        def check_and_replace(key:str, details, get_from_kb):
            if key in details.keys():
                if  details[key] != '{empty}':
                    details[key] = get_from_kb(details[key])
                else:
                    details[key] = ""
            return details
        
        details = check_and_replace('team1', details, self.kb.get_team)
        details = check_and_replace('team2', details, self.kb.get_team)
        details = check_and_replace('player1', details, self.kb.get_player)
        details = check_and_replace('player2', details, self.kb.get_player)
        
        return details
    """

if __name__ == '__main__':

    comment = "it seems that {player1} belonging to {team1} intercepts the ball of the player"
    placeholders = {'player1': 42, 'team1': 42}

    print("COMMENT:", comment)
    print("PLACEHOLDERS:", placeholders)

    filler = Filler("")
    comment = filler.update_comment(comment, placeholders)
    print(comment)