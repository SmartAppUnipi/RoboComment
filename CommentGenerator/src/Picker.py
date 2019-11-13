import json
import re


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

    def filter_comments_by_details(self, details):
        ''' it returns the most specific template according to the details '''
        subtype_templates = self.template_pool[details["subtype"]]
        most_specific_template = {
            "template" : "",
            "number_of_placeholders" : -1
        }
        for template in subtype_templates:
            # this wouldn't work with escaped placeholders like {{team1}}, use (?<=(?<!\{)\{)[^{}]*(?=\}(?!\})) to fix it
            placeholders = re.findall(r'{(.*?)}', template)
            
            # removing the placeholder {modifier} beacause here it is not needed for the comparison
            if 'modifier' in placeholders:
                placeholders.remove('modifier')

            if set(placeholders) <= set(details.keys()):
                if len(placeholders) >= most_specific_template['number_of_placeholders']:
                    # having more placeholders means to be a more specific template w.r.t the previous ones
                    most_specific_template['template'] = template
                    most_specific_template['number_of_placeholders'] = len(placeholders)

        # in this case there is no policy in selecting the template 
        # if there are more possible templates it will return just one of them quite randomly
        return most_specific_template['template']