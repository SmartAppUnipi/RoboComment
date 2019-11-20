
class Tagger:
    """
    Tagger to tag the passed sentence, here define policy to tag information
    Taken various tag information from a json, based on some policy, applying the tagging rules
    """
    def __init__(self):
        self.rules = {
            "{player1}": "SUBJECT",
            "{team1}": "SUBJECT_TEAM",
            "{player2}" : "OBJECT_PRONOUNS",
            "{team2}" : "OBJECT_PRONOUNS_TEAM",
            "{type}": "ACTION_TYPE",
            "{subtype}": "SUBTYPE",
            "{field_zone}": "ZONE"
        }

    def tag_sentence(self, sentence):
        """
        In this method is solved the ordered dependency, thanks to dictionary
        :param sentence: ["{player1}", "{team1}", ...]
        :return: ["{player1}", entity tagged), ("{team1}", entity tag), ...]
        """
        sentence_tagged = []
        for tag in sentence:
            sentence_tagged.append((tag, self.rules[tag]))
        return sentence_tagged
