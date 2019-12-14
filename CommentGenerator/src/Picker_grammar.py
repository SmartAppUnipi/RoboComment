import json
import logging
import random
try:
    from .tags.Extractor import Extractor
    from .tags.Player import Player
    from .tags.Elementary import Elementary
    from .tags.Team import Team
    from .Filler import Filler
except:
    from tags.Extractor import Extractor
    from tags.Player import Player
    from tags.Team import Team
    from tags.Elementary import Elementary
    from Filler import Filler


class Picker:
    """
    This class constructs the sentence according to input json and the state of the commentator
    """

    def __init__(self):
        # this class will be responsible to extract info inside json
        self.__extractor = Extractor()
        with open('CommentGenerator/assets/comments_empty_moments.txt', "r") as f:
            self.__lulls = [line for line in f.readlines()]


    def pick_comment(self, input_json: json, template_type: str)->tuple:
        """
        Call this method to start the template generator
        Try to follow the state of the machine, but if the error is some error try another level template
        :param template_type: int category representing the state of who call this method
            comment/lulls, priority[2]
            pure comment, priority [3-9]
            pure comment repeated , [4-10]
            pure lulls , priority[1]
        :param input_json:
        :return: tuple with (string comment generated, placeholders (maybe empty), priority
        """

        # store input into tagger
        self.__extractor.set_input(input_json)

        # hybrid comment
        if template_type == "Hybrid comment":
            (success, comment) = self.__hybrid_comment()
            if success:
                comment = " ".join(str(word) for word in comment)
                return comment, {}, 2
            else:
                template_type = "Pure comment"

        # pure comment
        if template_type == "Pure comment":
            (success, comment) = self.__pure_comment()
            if success:
                comment =  " ".join(str(word) for subtempl in comment for word in subtempl)
                placeholders = self.__extractor.get_value_from_placeholders(comment)
                return comment, placeholders, self.__extractor.get_priority()

        # pure lulls
        if template_type == "Lulls comment":
            (success, comment) = self.__lulls_comment()
            if success:
                return comment, {}, 1


        if template_type == "Welcome state":
            comment = self.__extractor.get_welcome_message()
            return comment, {}, 1

        raise Exception("PICKER_receives: registers error")

    def __pure_comment(self) -> tuple:
        """
        Construct the sentence according to the json input
        :return: tuple composed (success result (true, false), comment list produced)
        """
        # check if the fundamental type is in the json
        if self.__extractor.has_action():
            # take the order for corresponding action
            sentence_order = self.__extractor.get_order()

            # instantiate object given information, the logic of sub-template is moved into respective class
            template_generated = []
            # are mutually exclusive obviously
            for element in sentence_order:
                sub_template = ""
                if element == "Player_active":
                    # create player object, passing extraction info by tags
                    player1 = Player()
                    player1.obtain_info(self.__extractor.get_player_info('active'))
                    sub_template = player1.get_template()
                elif element == "Player_passive":
                    # create player object, passing extraction info by tags
                    player2 = Player()
                    player2.obtain_info(self.__extractor.get_player_info('passive'))
                    sub_template = player2.get_template()
                elif element == "Team_active":
                    # create player object, passing extraction info by tags
                    team_subject = Team()
                    team_subject.obtain_info(self.__extractor.get_team_info())
                    sub_template = team_subject.get_template()

                if element == "Elementary":
                    # create elementary object, passing extraction info by tags
                    action1 = Elementary()
                    action1.obtain_info(self.__extractor.get_action_info())
                    sub_template = action1.get_template()

                template_generated.append(sub_template)

            return True, template_generated

        else:
            return False, [""]

    def __hybrid_comment(self)-> tuple:
        """
        Construct the sentence according based hybrid info
        :return: tuple composed (success result (true, false), comment list)
        :return:
        """
        key,value = self.__extractor.get_random_info_and_value()
        # the random info is not inside the json
        if value == None:
            return (False, [""])
        # here we are sure that json contain that info
        return (True, ["{"+key+"}:{"+str(value)+"}"+"{space_where_get_info_from_kb}"])

    def __lulls_comment(self)-> tuple:
        """
        Construct the sentence completely lulls
        :return: tuple composed (success result (true, false), comment list)
        :return:
        """
        return (True, random.choice(self.__lulls))


if __name__ == '__main__':
    test1 = {
        "type": "revoked_goal",
        "reason":"offside",
        "match_id" : 42,
        "clip_uri" : "http://clip.of.the.match/juve/napoli",
        "user_id": 10,
        "time": 10,
        "start_time": 10,
        "end_time" : 20
}
    picker = Picker()
    comment, placeholders, priority = picker.pick_comment(test1, "Pure comment")

    print("Comment:", comment)
    print("Placeholders:",placeholders)
    print("Priority", priority)