import random


class Player:
    """
    Expresses player information
    """

    def __init__(self):
        # active or passive
        self.__syntactic_rule = None
        # integer id
        self.__value = None
        # [0,1]
        self.__confidence = None
        # integer id
        self.__team_value = None
        # [0,1]
        self.__team_confidence = None

    def obtain_info(self, info:tuple):
        """
        Receive info in this order : (syntactic_rule, value, confidence, team_value, team_confidence)
        :param info:
        :return:
        """
        self.__syntactic_rule = info[0]
        self.__value = info[1]
        self.__confidence = info[2]
        self.__team_value = info[3]
        self.__team_confidence = info[4]

    def get_template(self)->list:
        """
        Based on info about player return the best descriptive comment
        :return:
        """
        player_info = []
        team_info = []

        # subject information, so the starting of the sentence
        if self.__syntactic_rule == 'player_active':

            # start sentence based on PLAYER CONFIDENCE
            if self.__confidence != None:
                if self.__confidence <= 0.5:
                    player_info.append(random.choice(["it seemed to me that ", "maybe "]))
                elif self.__confidence >= 0.7:
                    player_info.append(random.choice(["it was clearly seen that ", "I saw that "]))
            else:
                player_info.append("")

            # continue sentence based on PLAYER INFO
            if self.__value != None:
                player_info.append(random.choice(["{player_modifier} {player1} ","{player1} " ]))
            else:
                player_info.append("a player ")

            # continue sentence based on TEAM INFO
            if self.__team_value != None:
                if self.__team_confidence != None:
                    if self.__team_confidence <= 0.5:
                        team_info.append(random.choice([", of the well-known team, ", ""]))
                    else:
                        team_info.append(random.choice[(", of {team_modifier}{team1} team, ", ", of {team1} ")])
                else:
                    team_info.append(random.choice([", {team1} man, ", ""]))

        # receiver information
        elif self.__syntactic_rule == 'player_passive':
            # start sentence based on PLAYER CONFIDENCE
            if self.__confidence != None:
                if self.__confidence <= 0.5:
                    if self.__value != None:
                        player_info.append(random.choice(["perhaps {player_modifier} {player2} ", "maybe {player2} ", ""]))

                elif self.__confidence >= 0.7:
                    player_info.append(random.choice(["definitely {player_modifier} {player2} ", "resolutely {player2} "]))
            else:
                player_info.append("teammate ")

            # continue sentence based on TEAM INFO
            if self.__team_value != None:
                if self.__team_confidence != None:
                    if self.__team_confidence <= 0.5:
                        team_info.append(random.choice([", probably ", ", supposing, i can't see well "]))
                    else:
                        team_info.append(random.choice[(", of same team, ", "")])
            else:
                team_info.append(random.choice([", of same team, ", ""]))


        return player_info+team_info

    def print_info(self):
        print("Player info:", self.__syntactic_rule, self.__value, self.__confidence, self.__team_value, self.__team_confidence)