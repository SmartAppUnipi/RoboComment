import re
import json
from MockKnowledgeBase import MockKB
import numpy as np
class Filler:

    def __init__(self, kb,user_id):
        self.__kb = kb
        self.__user_id = user_id
        self.__modifier = {
            "player_modifier":{
                "good": ["skilled","terrific","great"],
                "neutral": [""],
                "bad": ["stupid","boot",""]
            },
            "team_modifier":{
                "good": ["great","victorious"],
                "neutral": [""],
                "bad" : ["disgusting","terrible","awful",""]
            }
        }


    def update_comment(self, comment:str, placeholders:dict)->str:
        """
        Update commet with placeholders values
        :param comment:
        :param placeholders:
        :return:
        """
        # placeholder stored in dictionary (only the real value)
        for placeh in placeholders:
            new_value = "ERROR"
            if placeh[:6] == 'player':
                new_value = self.__kb.get_player(placeholders[placeh])

            if placeh[:4] == 'team':
                new_value = self.__kb.get_team(placeholders[placeh])
            comment = comment.replace("{"+placeh+"}", str(new_value))

        # placeholder to obtain bias comment
        comment = self.update_comment_biased(comment,placeholders)

        return comment


    def update_comment_biased(self,comment:str,placeholders:dict):
        """
        Here process the comment in order to insert bias
        :param comment:
        :return:
        """

        fav_play_id = self.__kb.get_user_player(self.__user_id)
        fav_team_id = self.__kb.get_user_team(self.__user_id)
        positive_player = -1
        """
        Check if fav player is present, if it is, check if it's under the 1 or under the 2
        """
        for k in placeholders.keys():
            if  k[:6] =="player":
                if placeholders[k]==fav_play_id:
                    positive_player = k[-1]
        for k in placeholders.keys():
            if  k[:4] =="team":
                if placeholders[k]==fav_team_id:
                    positive_team = k[-1]
                else:
                    negative_team = k[-1]
        
        # placeholder to process internally
    
        if 'player_modifier' in comment and positive_player!='-1':
            comment = comment.replace("{player_modifier"+str(positive_player)+"}", np.random.choice(self.__modifier["player_modifier"]["good"]))

        if 'player_modifier' in comment and positive_player!='-1':
            comment = comment.replace("{team_modifier"+str(positive_player)+"}", np.random.choice(self.__modifier["team_modifier"]["good"]))

        #The remaining placeholders are modifiers that are not referred to the best team of player
        placeholders = re.findall(r'{(.*?)}', comment)
        
        for placeh in placeholders:
            print(placeh,placeh[:6])
            if placeh[:6] == 'player':
                comment = comment.replace("{"+placeh+"}", np.random.choice(self.__modifier["player_modifier"]["bad"]))
            if placeh[:4] == 'team':
                comment = comment.replace("{"+placeh+"}", np.random.choice(self.__modifier["team_modifier"]["bad"]))
        return comment

    """
    
    # getting the placeholders {*_modifier} 
    placeholders = re.findall(r'{(.*?)}', comment)
    regex = re.compile(r'\w*_modifier')
    modifiers = [i for i in placeholders if regex.match(i)]

    details = self.replace_id_with_names(details)
    
    
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

    comment = "it seems that {player_modifier1} {player1} , {team1} man,  has blocked what it looks like {player_modifier2} {player2}"
    placeholders = {'player1': 18, 'team1': 42, 'player2': 7}

    print("COMMENT:", comment)
    print("PLACEHOLDERS:", placeholders)
    user_id = 42
    filler = Filler(kb=MockKB(),user_id = user_id)
    comment = filler.update_comment(comment, placeholders)
    print(comment)