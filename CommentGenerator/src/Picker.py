import json
import re
import random


class Picker:

    def __init__(self, template_path):
        self.picking_strategy = PickingStrategy()
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
            possible_templates = self.filter_comments_by_details(input_json["details"])

            template = self.picking_strategy.random_picking(possible_templates)

        # else TODO match with a filler template, here with empty template
        else:
            template = None

        return template

    def subtype_exists(self, subtype: str) -> bool:
        '''check if the subtype passed is in categories recognized'''
        return subtype in self.valid_categories["elementary"]

    def filter_comments_by_details(self, details):
        ''' it returns a list of the most specific templates according to the details '''
        subtype_templates = self.template_pool[details["subtype"]]
        most_specific_templates = {
            "template" : [],
            "number_of_placeholders" : -1
        }
        for template in subtype_templates:
            # this wouldn't work with escaped placeholders like {{team1}}, use (?<=(?<!\{)\{)[^{}]*(?=\}(?!\})) to fix it
            placeholders = re.findall(r'{(.*?)}', template)
            
            # removing the placeholder *_modifier beacause here it is not needed for the comparison
            regex = re.compile(r'\w*_modifier')
            placeholders = [i for i in placeholders if not regex.match(i)]

            if set(placeholders) <= set(details.keys()):
                if len(placeholders) > most_specific_templates['number_of_placeholders']:
                    # having more placeholders means to be a more specific template w.r.t the previous ones
                    most_specific_templates['template'] = [template]
                    most_specific_templates['number_of_placeholders'] = len(placeholders)
                elif len(placeholders) == most_specific_templates['number_of_placeholders']:
                    # if templates are equally specific a list is returned
                    most_specific_templates['template'].append(template)

        
        return most_specific_templates['template']
    

class PickingStrategy:
    def __init__(self):
        self.comments_history = {}

    def probability_picking(self,templates,action_subtype):

        # TODO 
        # each template will have an id
        # to each id we will associate a probability PROBVAL initially set to 1
        # and incremented each time that template is used 
        # we will pick the templates with probability 1/PROBVAL
        pass

    def random_picking(self,templates):
        return random.choice(templates)