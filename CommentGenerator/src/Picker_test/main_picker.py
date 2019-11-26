from CommentGenerator.src.Picker_test.Tagger import Tagger
from CommentGenerator.src.Picker_test.TemplateGenerator import TemplateGenerator

if __name__ == '__main__':
    """
    Order to follow:
        Subject_player Team_player ACTION_PLAYER ACTION_ZONE Receiver_player Team_receiver
    if there are missing information from json populate with empty.
    Insert only sensible combination according to names upward with correlative domain
    """

    sentence = ['{player1}','{team1}','{cross}','{empty}','{player2}','{team2}']

    # Tagged input with syntactical meaning
    tagger = Tagger()
    sentence_tagged = tagger.tag_sentence(sentence)
    print("\nResulting sentence tagged:", sentence_tagged)


    # Given content of the tagged construct the template
    template_generator = TemplateGenerator()
    comment_tagged = template_generator.generate(sentence_tagged)
    comment = template_generator.to_comment(comment_tagged)
    print("\nComment produced:", comment)
