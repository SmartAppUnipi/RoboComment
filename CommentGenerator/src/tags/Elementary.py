import random


class Elementary:
    """
    Expresses action type
    """

    def __init__(self):
        self.__type = None
        self.__time_start = None
        self.__time_end = None
        self.__zone_value_x = None
        self.__zone_value_y = None


    def obtain_info(self, info:tuple):
        """
        Receive info in this order : (type, time_start, time_end, zone_value_x, zone_value_y)
        :param info:
        :return:
        """
        self.__type = info[0]
        self.__time_start = info[1]
        self.__time_end = info[2]
        self.__zone_value_x = info[3]
        self.__zone_value_y = info[4]

    def get_template(self)->list:
        """
        Based on info about action return the best descriptive comment, they are mutually exclusive
        At least 5 different expression for every action
        :return:
        """
        action_info = []
        time_info = []

        # express POSSESSION
        if self.__type == 'possession':
            action_info.append(random.choice(["takes possession ", "takes the responsibility of changing something ",
                                              "takes the ball ", "takes the witness ",
                                              "receives the ball ", "earns the ball ",
                                              "has the ability to change the match "
                                              ]))
            # customizing it based on time
            if self.__time_start != None and self.__time_end != None:
                if (self.__time_end - self.__time_start) > 5:
                    time_info.append(random.choice([", repetitively ",
                                                    ", teammates trust him ",
                                                    ", will have the courage to dare? "]))

        # express PASS
        elif self.__type == 'pass':
            action_info.append(random.choice(["has made a pass to", "gives the ball to",
                                              "passes to", "passes the ball to",
                                              "gives importance to ", "welcomes the request of",
                                              "circulates the ball towards"
                                              ]))

        # express INTERCEPT
        elif self.__type == 'intercept':
            action_info.append(random.choice(["intercepts the ball of", "has blocked", "intercepts",
                                              "stops the ball of", "interrupts dreams of", "dirty the game of"
                                              ]))

        # express PENALTY
        elif self.__type == 'penalty':
            action_info.append(random.choice(["this is a penalty for the referee, the game has been stopped",
                                              "the referee whistles and has something to say to the player",
                                              "whistled a foul, there will be a penalty"
                                              ]))
        # express SHOT ON TARGET
        elif self.__type == "shot_on_target":
            action_info.append(random.choice(["kicks the ball towards the soccer goal",
                                              "tries to surprise the goalkeeper with a shot on target",
                                              "uses the moment to kick the ball towards the goal"
                                              ]))

        return action_info+time_info


    def print_info(self):
        print("Action info:", self.__type, self.__time_start, self.__time_end, self.__zone_value_x, self.__zone_value_y)