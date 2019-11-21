import nltk
from nltk import CFG


class Tagger:
    """
    Tagger to tag the passed sentence, here define policy to tag information
    Taken various tag information from a json, based on some policy, applying the tagging rules
    """

    def __init__(self):
        self.rules = {
            "{player1}": "SUBJECT",
            "{team1}": "SUBJECT_TEAM",
            "{player2}": "OBJECT_PRONOUNS",
            "{team2}": "OBJECT_PRONOUNS_TEAM",
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


if __name__ == '__main__':
    print("hello")
    """
    Syntax:
    WORD are Node
    Word are leaf
    """
    grammar = CFG.fromstring("""
    JSON -> Subject DETAILS | TIME Subject DETAILS
    Subject -> '{player1}' | '{team1}'
    
    SUBTYPE -> ELEMENTARY | STRATEGY | SCENARIO
    Elementary -> 'pass' | 'shot' | 'holderMove' | 'move' | 'possession' | 'cross' | 'foul' | 'duel' | 'clearance' | 'possession lost' | 'interception'
    Details -> '{team1}' | '{team2}' | '{player1}' | '{player2}' | '{field_zone}' | '{subtype}' | '{confidence}'
    """)

    print('A Grammar:', grammar)
    print('grammar.start()   =>', grammar.start())
    print('grammar.productions() =>')
    # Use string.replace(...) is to line-wrap the output.
    print(grammar.productions())

    try:
        input = ['{player1}']
        grammar.check_coverage(input)
        print("\nJson covered")

        rd_parser = nltk.RecursiveDescentParser(grammar)
        for tree in rd_parser.parse(input):
            print(tree)
    except:
        print("Same Json tag passed are not covered")