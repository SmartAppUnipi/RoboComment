from .Picker import Picker
from .Filler import Filler
from .Sentimentalizer import Sentimentalizer
import json

class Commentator:

    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.config = 'CommentGenerator/assets/config.json'
        self.template = 'CommentGenerator/assets/templates.json'
        self.picker = Picker(self.template)
        self.filler = Filler(knowledge_base,self.config)
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

