# from xml.dom import minidom

# "<comment> <subject> Cristiano Ronaldo </subject> has made a pass </comment>"


class Picker():

    def __init__(self, template_pool):
        self.template_pool = template_pool

    def pick_comment(self, input_json):
        ''' it gets a json object in input '''

        return template_dictionary["pass"][0]
