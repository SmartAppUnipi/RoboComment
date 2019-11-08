import json


class Picker():

    def __init__(self, template_path):
        with open(template_path,'r') as json_file:
            self.template_pool = json.load(json_file)

    def pick_comment(self, action):
        ''' it gets the action in input so that it can decide which template choose '''
    
        template = self.template_pool[action][0]

        return  template
