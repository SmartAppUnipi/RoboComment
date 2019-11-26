from CommentGenerator.src.Picker_test.Matcher import Matcher
from CommentGenerator.src.Picker_test.Tagger import Tagger
from CommentGenerator.src.Picker_test.TemplateGenerator import TemplateGenerator

if __name__ == '__main__':
    """
    Order to follow:
        Subject_player Team_player Action_player ACTION_ZONE Receiver_player Team_receiver
    if there are missing information from json populate with empty.
    Insert only sensible combination according to names upward
    """

    sentence = ['{player1}','{empty}','{shot}','{right}','{player2}','{empty}']

    # Tagged input with syntactical meaning
    tagger = Tagger()
    sentence_tagged = tagger.tag_sentence(sentence)
    print("\nResulting sentence tagged:", sentence_tagged)

    # Given content of the tagged construct the template
    template_generator = TemplateGenerator()
    comment = template_generator.generate(sentence_tagged)
    print("\nComment produced:", comment)
