import json
import random
import re


class Extractor:
    """
    Giving input and key element search and store the relative information
    """

    def __init__(self):
        # store locally the input
        self.__input = None
        # prior assumption of min information given an action, the value corresponds to instance of class in tag folder
        self.__mapping_action = {
            "possession": ['Player_active', 'Elementary'],
            "intercept": ['Player_active', 'Elementary', 'Player_passive'],
            "pass": ['Player_active', 'Elementary', 'Player_passive'],
            "shot_on_target": ['Player_active','Elementary'],
            "shot_off_target": ['Player_active', 'Elementary'],
            "goal":['Player_active', 'Elementary'],
            "tikitaka": ["Team_active", "Elementary"],
            "penalty": ["Elementary", "Team_passive"],
            "offside": ["Elementary"],
            "revoked_goal":["Elementary"],
            "duel":['Player_active', 'Elementary','Player_passive']
        }
        # randomly select one of this info to produce a comment based on this
        self.__possible_category_hybrid = ["player", 'team']
        # priority value of this json
        self.__priority = -1
        self.__welcome_message = ["Welcome to the match is speaking RoboComment and it will be with you to comment this match",
                                  "Welcome, I am RoboComment and I will be your commentator for the rest of the game, let's start"]


    def set_input(self, jsonobj:json):
        self.__input = jsonobj
        self.has_action()

    def has_action(self) -> bool:
        """
        Check if the action is present, if yes set the priority
        :return:
        """
        # define priority of the actions in the range of [3-9]
        priority_mapping = {
            "possession": 3,
            "intercept": 5,
            "pass": 4,
            "penalty": 8,
            "shot_on_target":8,
            "shot_off_target": 6,
            "goal":8,
            "tikitaka":4,
            "offside":8,
            "revoked_goal":9,
            "duel":5
        }
        if "type" in self.__input:
            if self.__input["type"] in priority_mapping:
                self.__priority = priority_mapping[self.__input['type']]
                return True
        return False

    def get_order(self) -> list:
        """
        Get the corret order of words based on action
        :return:
        """
        return self.__mapping_action[self.__input["type"]]

    def get_player_info(self, role:str) -> tuple:
        """
        DON'T touch the order
        Search and return information about the player in
        :return: tuple ordered (syntactic_rule, value, confidence, team_value, team_confidence)
        """
        syntactic_rule = None
        value = None
        confidence = None
        team_value = None
        team_confidence = None

        if role == 'active':
            syntactic_rule = 'player_active'
        elif role == 'passive':
            syntactic_rule = 'player_passive'

        # search syntactic rule trying to reducing if
        if syntactic_rule in self.__input:
            if 'id' in self.__input[syntactic_rule]:
                if 'value' in self.__input[syntactic_rule]['id']:
                    value = self.__input[syntactic_rule]['id']['value']
                if 'confidence' in self.__input[syntactic_rule]['id']:
                    confidence = self.__input[syntactic_rule]['id']['confidence']

            if 'team' in self.__input[syntactic_rule]:
                if 'value' in self.__input[syntactic_rule]['team']:
                    team_value = self.__input[syntactic_rule]['team']['value']

                if 'confidence' in self.__input[syntactic_rule]['team']:
                    team_confidence = self.__input[syntactic_rule]['team']['confidence']

        return syntactic_rule, value, confidence, team_value, team_confidence

    def get_action_info(self) -> tuple:
        """
        Search and return information about the action
        :return: tuple ordered (type, value, time_start, time_end, zone_value_x, zone_value_y)
        """
        type = None
        time_start = None
        time_end = None
        zone_value_x = None
        zone_value_y = None

        # search syntactic rule trying to reducing if
        if 'type' in self.__input:
            type = self.__input['type']
        if 'start_time' in self.__input:
            time_start = self.__input['start_time']
        if 'end_time' in self.__input:
            time_end = self.__input['end_time']

        if 'position' in self.__input:
            if 'x' in self.__input['position']:
                zone_value_x = self.__input['position']['x']
            if 'y' in self.__input['position']:
                zone_value_y = self.__input['position']['x']

        return type, time_start, time_end, zone_value_x, zone_value_y

    def get_team_info(self)-> tuple:
        """
        Search and return information about the subject team
        :return: tuple ordered (value)
        """
        value = None
        start = None
        end = None

        if 'team' in self.__input:
            value = self.__input['team']
            if 'start_time' in self.__input:
                start = self.__input['start_time']
            if 'end_time' in self.__input:
                start = self.__input['end_time']


        return value, start, end

    def get_random_info_and_value(self)-> tuple:
        """
        Called in case of hybrid comment, get one of the key and search in the input if is present
        :return: tuple composed by (key chosen, value of key if is present (else None))
        """
        key = random.choice(self.__possible_category_hybrid)
        value = None

        # randomly take info about active or passive player
        if key == "player":
            rule = random.choice(["player_active","player_passive"])
            # if has information
            if rule in self.__input:
                if self.__input[rule]['id']:
                    value = self.__input[rule]['id']['value']

        # extract action of match
        if key == "action":
            if 'type' in self.__input:
                value = self.__input['type']

        # extract minutes of match
        if key == "time":
            if 'end_time' in self.__input and 'start_time' in self.__input:
                time_second = (self.__input['end_time'] - self.__input['start_time'])/2
                time_minute = int(time_second/60)
                value = time_minute

        # randomly take team of active player or passive player
        if key == "team":
            rule = random.choice(["team_active", "team_passive"])
            if rule == 'team_active':
                if 'player_active' in self.__input:
                    if 'team' in self.__input['player_active']:
                        value = self.__input['player_active']['team']['value']
            elif rule == 'team_passive':
                if 'player_passive' in self.__input:
                    if 'team' in self.__input['player_passive']:
                        value = self.__input['player_passive']['team']['value']

        return (key, value)

    def get_value_from_placeholders(self, comment:str)->dict:
        """
        Search the value belonging to the placeholders in the comment, returning it as dictionary
        Take sync this placeholders with the possible ones
        :param comment:
        :return: dict{placeholder:value}
        """

        pairs = {}
        placeholders = re.findall(r'{(.*?)}', comment)

        for plh in placeholders:
            if plh == "player1":
                pairs[plh]= self.get_player_info('active')[1]
            if plh == "player2":
                pairs[plh] = self.get_player_info('passive')[1]
            if plh == "team1":
                # or it is inside the player
                if self.get_player_info('active')[3] != None:
                    pairs[plh] = self.get_player_info('active')[3]
                # or it is outside in the team tag
                else:
                    pairs[plh] = self.get_team_info()[0]
            if plh == "team2":
                pairs[plh] = self.get_player_info('passive')[3]

        return pairs

    def get_priority(self)->int:
        return self.__priority

    def get_welcome_message(self)->str:
        """
        Return some intro before the pure comment, miming the consideration of "real commentator"
        :return:
        """
        return random.choice(self.__welcome_message)