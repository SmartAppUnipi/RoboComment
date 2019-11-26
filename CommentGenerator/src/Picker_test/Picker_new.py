import json
import random

from CommentGenerator.src.Picker_test.Tagger import Tagger
from CommentGenerator.src.Picker_test.TemplateGenerator import TemplateGenerator

class Picker:

    def __init__(self):
        self.tagger = Tagger()
        self.template_generator = TemplateGenerator()
        # list of possible comments to extract where no info are passed
        with open('./comments_others.txt', "r") as f:
            self.comment_others = [str(line) for line in f.readlines()]

        # order of tags
        self.sentence_order = ['player1', 'team1', 'subtype', 'field_zone', 'player2', 'team2']
        # element where insert value instead of key
        self.tag_to_value = ["subtype", "field_zone"]

    def pick_comment(self, input_json: json):
        ''' From json extract information and save in a ordered list according to sentence_order '''

        input_json = {
            'time': {'start': 10, 'end': 20},
            'type': 'elementary',
            'details': {'subtype': 'pass', 'team1': 'Team A'}
        }

        print("Input:", input_json)
        comment = ""
        # extract information from json
        # if json is empty
        if self.check_empty_json(input_json):
            comment = random.sample(self.comment_others, 1)[0]
        # if json is not empty
        else:
            sentence = self.create_sentence(input_json['details'])
            print("\nCreated sentence:", sentence)

            # tag the information in the json
            sentence_tagged = self.tagger.tag_sentence(sentence)
            print("\nTagged created sentence:", sentence_tagged)

            # validate the grammar before generate template


            # create base sentence
            comment = self.template_generator.generate(sentence_tagged)

        return comment

    def create_sentence(self, information):
        """
        Structure the sentence in a predefine way.
        The order is formalize according to sentence_order
        Some tags are substitute with the value, useful to generate correct template
        """
        # insert in a sentence the information in order,
        # substitute key with value in some field
        sentence = []
        for element in self.sentence_order:
            # we have the information
            if element in information:
                # if value is needed
                if element in self.tag_to_value:
                    sentence.append("{" + str(information[element]) + "}")
                # if key is needed
                else:
                    sentence.append("{" + str(element) + "}")
            # info is not present
            else:
                sentence.append('{empty}')

        return sentence

    def check_empty_json(self, input_json)->bool:
        """
        Check if the json has useful information, if not create a contextual template
        :param input_json:
        :return:
        """
        if len(input_json) == 0:
            return True
        else:
            return False


if __name__ == '__main__':

    """
    Call this class from commentator
    """
    picker = Picker()

    with open("../../assets/input1.json", 'r') as input1_json:
        input_json = json.load(input1_json)

        comment = picker.pick_comment(input_json)
        print("\nFINAL comment:", comment)

