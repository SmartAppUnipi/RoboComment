from CommentGenerator.src.Picker.Matcher import Matcher
from CommentGenerator.src.Picker.Tagger import Tagger
from CommentGenerator.src.Picker.TemplateGenerator import TemplateGenerator

if __name__ == '__main__':
    """
    This file should be deleted and insert the content into picker class
    i've implemented this few (check the matcher to discover phrase)
    Works also with different order

!!!!!
IMPORTANT
There are fake example, could make no sense is only tho show how the architecture works
!!!!!!!!!! 

    examples:
    "{player1}", "{subtype}"
    "{player1}", "{subtype}", "{field_zone}"
    "{player1}", "{field_zone}"
    "{team1}", "{type}"   
    "{player1}", "{team1}", "{subtype}"
    "{player1}", "{team1}", "{field_zone}", "{subtype}"
    ...
    ...
    """
    # TODO we need to define phrase mutual exclusive (we will discuss it)
    sentence = ["{player1}", "{field_zone}"]

    # Tagged input with syntactical meaning
    tagger = Tagger()
    sentence_tagged = tagger.tag_sentence(sentence)
    print("\nResulting sentence tagged:", sentence_tagged)

    # Based on syntactical meaning find the correct phrase order
    matcher = Matcher()
    phrase_typology,sentence_tagged_ordered = matcher.match_sentence_tagged(sentence_tagged)
    print("\nResulting phrase typology:", phrase_typology)
    print("Resulting sentence tagged ordered:", sentence_tagged_ordered)

    # Given content of the tagged input and the typology of phrase construct the template
    template_generator = TemplateGenerator()
    comment = template_generator.generate(sentence_tagged_ordered, phrase_typology)
    print("\nComment produced:", comment)