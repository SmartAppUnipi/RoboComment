import re

class Filler:

    def __init__(self, config=None):
        if config is None:
            self.config = {"user_type" : "" ,"favourite_player" : "", "favourite_team" : ""}
        else:
            self.config = config

        self.good_modifiers = ['good','nice']
        self.bad_modifiers = ['bad']

    def update_comment(self, comment, details):
        # TODO just trying a demo/simple version, this needs a better implementation
        details['modifier'] = '{modifier}'
        comment = comment.format(**details)

        if 'modifier' in re.findall(r'{(.*?)}', comment):
            if details['team1'] == self.config['favourite_team']:
                comment = comment.format(modifier=self.good_modifiers[0])
            else:
                comment = comment.format(modifier=self.bad_modifiers[0])

        return comment
