import json

from CommentGenerator.src.Picker_test.Tagger import Tagger
from CommentGenerator.src.Picker_test.TemplateGenerator import TemplateGenerator

class Picker:

    def __init__(self):
        self.tagger = Tagger()
        self.template_generator = TemplateGenerator()

        # order of tags
        self.sentence_order = ['player1', 'team1', 'subtype', 'field_zone', 'player2', 'team2']
        # element where insert value instead of key
        self.tag_to_value = ["subtype", "field_zone"]

    def pick_comment(self, input_json: json):
        ''' From json extract information and save in a ordered list according to sentence_order '''

        information = input_json['details']

        # extract information from json
        sentence = self.create_sentence(information)
        print("\nResulting sentence:", sentence)

        # tag the information in the json
        sentence_tagged = self.tagger.tag_sentence(sentence)
        print("\nResulting sentence tagged:", sentence_tagged)

        #
        comment = self.template_generator.generate(sentence_tagged)
        print("\nComment produced:", comment)
        return

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


if __name__ == '__main__':

    picker = Picker()

    with open("../../assets/input1.json", 'r') as input1_json:
        input_json = json.load(input1_json)

        comment = picker.pick_comment(input_json)

