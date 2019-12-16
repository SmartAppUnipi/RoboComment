import random


class Team:
    """
    Expresses player information
    """

    def __init__(self, rule):
        # integer id
        self.__rule = rule
        self.__value = None
        self.__start_time = None
        self.__end_time = None

    def obtain_info(self, info:tuple):
        """
        Receive info in this order : (value, start time, end time)
        :param info:
        :return:
        """
        self.__value = info[0]
        self.__start_time = info[1]
        self.__end_time = info[2]

    def get_template(self)->list:
        """
        Based on info about player return the best descriptive comment
        "confidence, player_value, team_confidence, team_value"
        :return:
        """
        team_info = []

        if self.__value != None:
            if self.__rule == "active":
                    team_info.append(random.choice(["now it is several minutes that {team1}", "{team1}"]))
            elif self.__rule == "passive":
                team_info.append(random.choice([", {team_modifier1} {team1} gets the ball"]))

        return team_info

    def print_info(self):
        print("Team info:", self.__value, self.__start_time, self.__end_time)