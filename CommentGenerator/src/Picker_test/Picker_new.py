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

        # order of tags, corresponding to definition of the grammar
        self.sentence_order = {
            "active": ['player1', 'team1', 'subtype', 'field_zone', 'player2', 'team2'],
            "passive": ['player2', 'team2', 'subtype', 'field_zone', 'player1', 'team1']
        }
        # element where insert value instead of key
        self.tag_to_value = ["subtype", "field_zone"]

    def pick_comment(self, input_json: json) -> str:
        """
        From json extract information and produce a comment.
        The comment is stored and filled from comments_others if the input is empty
        The comment is produced with a partial comment if the json has not consistent information
        The comment is tagged and produce if the json has useful information
        :param input_json:
        :return:
        """
        if self.check_empty_json(input_json):
            final_comment = self.create_others()
        else:
            sentence = self.create_sentence(input_json["details"])
            # try to tag the sentence
            try:
                sentence_tagged = self.tagger.tag_sentence(sentence)
                final_comment = self.template_generator.generate(sentence_tagged)
            # if an error is found means that inconsistency was found
            except:
                # TODO try to create a comment with less possible information and querying kb
                final_comment = self.create_others()

        return final_comment

    def create_others(self) -> str:
        """
        This method pick a random template inside the comments_others.txt to fill the empty moments
        :return:
        """
        return random.choice(self.comment_others)

    def create_sentence(self, information) -> list:
        """
        Structures the sentence according to order in sentence_order
        Some tags are substitute with the value, useful to generate correct template
        :param information:
        :return:
        """
        sentence = []
        # randomly chose between active and passive comment
        sorting = random.choice(list(self.sentence_order))

        for element in self.sentence_order[sorting]:
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

    def check_empty_json(self, input_json) -> bool:
        """
        Check if the json has useful information, if not create a contextual template
        :param input_json:
        :return:
        """
        if len(input_json) == 0:
            return True
        return False


if __name__ == '__main__':
    """
    Call this class from commentator
    """
    picker = Picker()

    with open("../../assets/input1.json", 'r') as input1_json:
        input_json = json.load(input1_json)
        # TODO add test test and test
        print("INPUT:", input_json)
        comment = picker.pick_comment(input_json)
        print("\nFINAL comment:", comment)

    # TODO idea, use a model to rephrase the comment to obtain human readable and grammar spell checks
    # check python paraphrase sentence and evaluate if split correction to paraphrase