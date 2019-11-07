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

        

        comment = self.picker.pick_comment(jsonobj)
        comment = self.filler.update_comment(comment)

        sentiment = self.sentimentalizer.add_emphasis(comment)

        output = {
            'comment': comment,
            'emphasis': sentiment,
            'time': time,
        }

        output = json.dumps(output)

        print(output)


cm = Commentator("assets/config_test.json","assets/templates.json")
input_json = { "time" :
                {
                    "start": 800,
                    "end": 810
                }
             }
cm.run(input_json)