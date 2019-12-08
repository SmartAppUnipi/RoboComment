import json
import logging
import random

from .tags.Elementary import Elementary
from .tags.Extractor import Extractor
from .tags.Player import Player


class Picker:
    """
    This class constructs the sentence according to input json and the state of the commentator
    """

    def __init__(self):
        # this class will be responsible to extract info inside json
        self.__extractor = Extractor()
        with open('CommentGenerator/assets/comments_empty_moments.txt', "r") as f:
            self.__lulls = [str(line) for line in f.readlines()]

    def pick_comment(self, input_json: json, template_type: int)->str:
        """
        Call this method to start the template generator
        Try to follow the state of the machine, but if the error is some error try another level template
        :param template_type: int category representing the state of who call this method
            template_type=0 : pure comment
            template_type=1 : comment/lulls
            template_type=2 : pure lulls
        :param input_json:
        :return: string comment generated with placeholder
        """
        if 0 > template_type > 2:
            raise Exception("PICKER_receives: wrong input")

        # store input into tagger
        self.__extractor.set_input(input_json)

        # pure comment
        if template_type == 0:
            (success, comment) = self.__pure_comment()
            if success:
                return " ".join(str(word) for subtempl in comment for word in subtempl)
            else:
                template_type += 1

        # hybrid comment
        if template_type == 1:
            (success, comment) = self.__hybrid_comment()
            if success:
                return " ".join(str(word) for word in comment)
            else:
                template_type += 1

        # pure lulls
        if template_type == 2:
            (success, comment) = self.__lulls_comment()
            if success:
                return " ".join(str(word) for word in comment)
            else:
                template_type += 1

        raise Exception("PICKER_receives: not possible construct template")

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

                if element == "Elementary":
                    # create elementary object, passing extraction info by tags
                    action1 = Elementary()
                    action1.obtain_info(self.__extractor.get_action_info())
                    sub_template = action1.get_template()


                template_generated.append(sub_template)

            return True, template_generated

        else:
            raise Exception("Picker_pure-comment: action is not present")

    def __hybrid_comment(self)-> tuple:
        """
        Construct the sentence according based hybrid info
        :return: tuple composed (success result (true, false), comment list)
        :return:
        """
        result = self.__extractor.get_random_info_and_value()
        # the random info is not inside the json
        if result[1] == None:
            return (False, [""])
        # here we are sure that json contain that info
        return (True, [""])

    def __lulls_comment(self)-> tuple:
        """
        Construct the sentence completely lulls
        :return: tuple composed (success result (true, false), comment list)
        :return:
        """
        return (True, random.choice(self.__lulls))