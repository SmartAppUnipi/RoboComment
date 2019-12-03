from nltk import RecursiveDescentParser
from nltk import data
from itertools import permutations

class Tagger:
    """
    Tagger to tag the passed sentence
    """

    def __init__(self):
        self.grammar = data.load('file:CommentGenerator/assets/json_grammar.cfg')

    def tag_sentence(self, sentence):

        print("\n sentence passed",sentence)
        for comb in permutations(sentence):
            try:
                print(comb)
                result = self.create_tree(comb)
                print(result)
            except:
                pass

        raise Exception("Not found compatible info")

    def create_tree(self, sentence):

        try:
            rd_parser = RecursiveDescentParser(self.grammar)
            for tree in rd_parser.parse(sentence):
                result = tree
            return result
        except:
            raise Exception("ERROR: Not matched passed data")

    def to_dictionary(self, result):
        final_result = {}
        # This method select the most specific tag for the json content
        for tags in result[0]:
            str_cleaned = str(tags).replace("(","").replace(")","")
            content = str_cleaned.split()
            final_result[content[len(content)-2]] = content[len(content)-1]

        return final_result