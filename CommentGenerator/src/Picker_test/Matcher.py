# needed c++14.0, download windows 10 sdk from Microsoft Visual C++ build tools
from fuzzywuzzy import fuzz


class Matcher:
    """
    Match the given tagged sentence with a correct phrase composition
    The phrase composition for now is based on input json given by other group
    Will be easy to add more composition here
    """
    def __init__(self):
        self.phrase = [
            "SUBJECT SUBJECT_TEAM SUBTYPE ZONE",
            "SUBJECT SUBJECT_TEAM SUBTYPE",
            "SUBJECT SUBTYPE",
            "SUBJECT ZONE",
            "SUBJECT ACTION_TYPE"
        ]

    def match_sentence_tagged(self, sentence_tagged):
        """
        Compare the sentence with it's internal phrases composition
        The matching is unordered but the resulting phrase corresponds to one of the internal phrases
        (for syntactical reason with ordered chosen a priori)
        :param sentence_tagged: [(json tag, entity tagged), (json tag, entity tag), ...]
        :return: ["SUBJECT", "ACTION TYPE", ...]
        """
        to_evaluate_tags = []
        for couple in sentence_tagged:
            to_evaluate_tags.append(couple[1])

        to_evaluate_phrase = ' '.join([str(elem) for elem in to_evaluate_tags])

        corresponding_index = self.fuzzy_matching(to_evaluate_phrase)

        phrase_chosen = self.phrase[corresponding_index]
        # needed for the template generator phase
        ordered_sentence_tagged = self.order_sentence_tagged(sentence_tagged, phrase_chosen)

        return phrase_chosen, ordered_sentence_tagged


    def fuzzy_matching(self, tags):
        """
        Do fuzzy matching implemented in fuzzywuzzy library with Levenshtein distance
        Comparing the tags with all internal phrase
        :param tags: list only of tags in the sentence, without the content
        :return: index of self.phrase with better fuzzy value
        """
        scores = []
        for phr in self.phrase:
            scores.append(fuzz.token_sort_ratio(tags, phr))

        # Threshold to casually remove information, i will explain
        if max(scores) < 80:
            raise Exception("Custom error: Not implemented combination")
        else:
            return scores.index(max(scores))

    def order_sentence_tagged(self, sentence_tagged, phrase_chosen):
        """
        Order the tagged sequence according to syntass of phrase chosen
        This allow a correct matching between placeholder and content in the next phase
        # very bad complexity (for now O(n^2)) to ordering
        :param sentence_tagged:
        :param phrase_chosen:
        :return:
        """
        ordered = []
        for elem in phrase_chosen.split():
            for tag in sentence_tagged:
                if tag[1] == elem:
                    ordered.append(tag)
        return ordered