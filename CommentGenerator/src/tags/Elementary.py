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
        :return:
        """
        action_info = []
        time_info = []

        # express POSSESSION
        if self.__type == 'possession':
            action_info.append(random.choice(["take possession ", "take the ball "]))
            # customizing it based on time
            if self.__time_start != None and self.__time_end != None:
                if (self.__time_end - self.__time_start) > 5:
                    time_info.append(random.choice(["for a long time ", ""]))
            else:
                time_info.append(random.choice(["who knows how long it will continue to do so", ""]))

        # express PASS
        elif self.__type == 'pass':
            action_info.append(random.choice(["has made a pass towards ", "gave the ball to "]))
            # customizing it based on time
            if self.__time_start != None and self.__time_end != None:
                if (self.__time_end - self.__time_start) > 5:
                    time_info.append(random.choice([", and who knows how many passes will do, ", ""]))
            else:
                time_info.append("")

        # express INTERCEPT
        elif self.__type == 'intercept':
            action_info.append(random.choice(["intercepted ", "has blocked "]))
            if self.__time_start != None and self.__time_end != None:
                if self.__time_end >= 2700:
                    time_info.append(random.choice([", in the second part of the match, ", ""]))
                elif self.__time_end < 2700:
                    time_info.append(random.choice([", in the first half, ", ""]))

        return action_info+time_info


    def print_info(self):
        print("Action info:", self.__type, self.__time_start, self.__time_end, self.__zone_value_x, self.__zone_value_y)