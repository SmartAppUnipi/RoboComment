import json


class Picker:

    def __init__(self, template_path):
        # Load templates
        with open(template_path, 'r') as json_file:
            self.template_pool = json.load(json_file)
        # load recognized categories
        categories_path = 'assets/categories.json'
        with open(categories_path, 'r') as json_file:
            self.valid_categories = json.load(json_file)

    def pick_comment(self, input_json: json):
        ''' it gets the json in input so that it can decide which template match '''

        # check if the subtype match other
        subtype = input_json["details"]["subtype"]
        if self.subtype_exists(subtype):
            # TODO find a way to match, here implement as first comment in the pool
            template = self.template_pool[subtype][0]

        # else TODO match with a filler template, here with empty template
        else:
            template = None

        return template

    def subtype_exists(self, subtype: str) -> bool:
        '''check if the subtype passed is in categories recognized'''
        return subtype in self.valid_categories["elementary"]