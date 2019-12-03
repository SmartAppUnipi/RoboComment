import random

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
        print("WINNER", winner)
        result = self.to_dictionary(winner)
        print("RISULTATO ", result)
        return ""

    def try_descent_until_no_error(self, combinations):
        for i in range(0, len(combinations)):
            for tree in self.parser.parse(combinations[i]):
                return tree

        raise Exception("Not found compatible grammar rules with sentence")

    def to_dictionary(self, result):
        for leaf in result.leaves():
            print(leaf)

        return ""
