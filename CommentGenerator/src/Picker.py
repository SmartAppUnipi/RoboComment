import json


class Picker():

    def __init__(self, template_path):
        with open(template_path,'r') as json_file:
            self.template_pool = json.load(json_file)

    def pick_comment(self, input_json):
        ''' it gets a json object in input '''

        return self.template_pool["pass"][0]
