from Picker import Picker
from Filler import Filler
from Sentimentalizer import Sentimentalizer
import json


class Commentator:

    def __init__(self, config, template):
        self.config = config
        self.template = template
        self.picker = Picker(self.template)
        self.filler = Filler(self.config)
        self.sentimentalizer = Sentimentalizer(self.config)
		

    def run(self, jsonobj):

        time = jsonobj['time']

        action = jsonobj["details"]["subtype"]

        comment = self.picker.pick_comment(action)
        comment = self.filler.update_comment(comment,jsonobj["details"])

        sentiment = self.sentimentalizer.add_emphasis(comment)

        output = {
            'comment': comment,
            'emphasis': sentiment,
            'time': time,
        }

        output = json.dumps(output)

        print(output)


cm = Commentator("assets/config_test.json","assets/templates.json")
with open("assets/input1.json",'r') as input1_json:
    input_json = json.load(input1_json)
    cm.run(input_json)