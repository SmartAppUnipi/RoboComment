from nltk import RecursiveDescentParser
from nltk import data

class Tagger:
    """
    Tagger to tag the passed sentence, here define policy to tag information
    Taken various tag information from a json, based on some policy, applying the tagging rules
    """

    def __init__(self):
        self.grammar = data.load('file:json_grammar.cfg')

    def tag_sentence(self, sentence):
        result = self.create_tree(sentence)

        dict_result = self.to_dictionary(result)

        return dict_result

    def create_tree(self, sentence):
        if len(sentence) == 6:
            try:
                rd_parser = RecursiveDescentParser(self.grammar)
                for tree in rd_parser.parse(sentence):
                    result = tree
                return result
            except:
                raise Exception("ERROR: Not matched passed data")
        else:
            raise Exception("Lentgh passed mismatch")

    def to_dictionary(self, result):
        final_result = {}
        # This method select the most specific tag for the json content
        for tags in result[0]:
            str_cleaned = str(tags).replace("(","").replace(")","")
            content = str_cleaned.split()
            final_result[content[len(content)-2]] = content[len(content)-1]

        return final_result