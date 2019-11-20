import random


class TemplateGenerator:
    """
    Find the most depth path from the keywords passed.
    # TODO add support to nested node in a recursive way
    """

    def __init__(self):
        self.nodes = {
            "SUBJECT": ["The {placeholder}", "The never old {placeholder}"],
            "SUBJECT_TEAM": ["player of {placeholder}", "{placeholder} player"],
            "SUBTYPE": ["do {placeholder}", "make a {placeholder}"],
            "ZONE": ["in the {placeholder} of the field", "in the {placeholder} zone", "insists in the {placeholder}"],
            "ACTION_TYPE": ["is doing a {placeholder}", "as according to coach {placeholder}"]
        }

    def generate(self, sentence_tagged, phrase_typology):
        composition = self.depth_visit(phrase_typology)
        comment = []
        for element, content in zip(composition, sentence_tagged):
            comment.append(element.replace("{placeholder}", content[0]))

        return ' '.join([str(elem) for elem in comment])

    def depth_visit(self, phrase_typology):
        """Depth visit for every node"""
        composition = []
        for phrase_id in phrase_typology.split():
            composition.append(self.find_leaf(phrase_id))
        return composition

    def find_leaf(self, phrase_id):
        """For now the nodes are all leaf, randomizing result"""
        return random.choice(self.nodes[phrase_id])
