#from .Picker import Picker
from .Filler import Filler
from .Sentimentalizer import Sentimentalizer
from .Picker_grammar import Picker
from .Adapter import Adapter
import json

class Commentator:

    def __init__(self, knowledge_base):
        self.kb = knowledge_base

        self.adapter = Adapter()
        self.picker = Picker()
        self.filler = Filler(knowledge_base)
        self.sentimentalizer = Sentimentalizer()

    def run(self, jsonobj):
        
        ''' Extract the time where the json is occurred and match and update the resulting template'''

        jsonobj = self.adapter.adapt(jsonobj)

        user_id = jsonobj['user_id']

        # Comment matching and updating
        comment = self.picker.pick_comment(jsonobj)
        comment = self.filler.update_comment(comment, jsonobj["details"],user_id )
        sentiment = self.sentimentalizer.add_emphasis(comment)

        time = jsonobj['time']

        output = {
            'comment': comment,
            'emphasis': sentiment,
            'startTime': time['start'],
            'endTime' : time['end'],
            'priority' : 4,
            'id' : user_id
        }
        return output

