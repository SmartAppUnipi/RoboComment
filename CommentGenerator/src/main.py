from .Picker import Picker
from .Filler import Filler
from .Sentimentalizer import Sentimentalizer
import json


class Commentator:

    def __init__(self, config, template):
        self.config = config
        self.template = template

    def run(self, jsonobj):

        time = jsonobj['time']

        picker = Picker(self.template)
        filler = Filler(self.config)
        sentimentalizer = Sentimentalizer(self.config)

        comment = picker.pick_comment(jsonobj)
        comment = filler.update_comment(comment)

        sentiment = sentimentalizer.add_emphasis(comment)

        output = {
            'comment': comment,
            'emphasis': sentiment,
            'time': time,
        }

        output = json.dumps(output)

        print(output)
