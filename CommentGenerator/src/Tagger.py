import random
import re

import nltk
from nltk import RecursiveDescentParser
from nltk import data
from itertools import permutations


class Tagger:
    """
    Tagger to tag the passed sentence
    """

    def __init__(self):
        self.grammar = data.load('file:CommentGenerator/assets/json_grammar.cfg')
        self.parser = RecursiveDescentParser(self.grammar)

    def tag_sentence(self, sentence):

        combinations_tuple = list(permutations(sentence))
        combinations = []
        for comb in combinations_tuple:
            combinations.append(list(comb))

        random.shuffle(combinations)
        winner = self.try_descent_until_no_error(combinations)
        result = self.to_dictionary(winner)

        return result

    def try_descent_until_no_error(self, combinations):
        for i in range(0, len(combinations)):
            for tree in self.parser.parse(combinations[i]):
                return tree

        raise Exception("Not found compatible grammar rules with sentence")

    def to_dictionary(self, result):
        tree_as_string = str(result)
        dict_resulting = {}
        for leaf in result.leaves():
            custom_escape = re.escape("(")
            d = re.search(custom_escape+'(.+) '+str(leaf), tree_as_string)

            dict_resulting[d.group(1)] = leaf

        return dict_resulting
