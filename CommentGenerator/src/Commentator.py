from .Picker import Picker
from .Filler import Filler
from .Sentimentalizer import Sentimentalizer
import json


class Commentator:

    def __init__(self):

        self.config = 'assets/config_test.json'
        self.template = 'assets/templates.json'
        self.picker = Picker(self.template)
        self.filler = Filler(self.config)
        self.sentimentalizer = Sentimentalizer(self.config)

    def run(self, jsonobj):
        ''' Extract the time where the json is occurred and match and update the resulting template'''

        # Comment matching and updating
        comment = self.picker.pick_comment(jsonobj)
        comment = self.filler.update_comment(comment, jsonobj["details"])
        sentiment = self.sentimentalizer.add_emphasis(comment)

        time = jsonobj['time']

        output = {
            'comment': comment,
            'emphasis': sentiment,
            'startTime': time['start'],
            'endTime' : time['end'],
            'priority' : 4
        }
        return output


cm = Commentator()
with open("assets/input1.json", 'r') as input1_json:
    input_json = json.load(input1_json)
    cm.run(input_json)