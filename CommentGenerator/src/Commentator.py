#from .Picker import Picker
try:
    from .Filler import Filler
    from .Sentimentalizer import Sentimentalizer
    from .Picker_grammar import Picker
except:
    from Filler import Filler
    from Sentimentalizer import Sentimentalizer
    from Picker_grammar import Picker
import json

class Commentator:

    def __init__(self, knowledge_base):
        self.kb = knowledge_base

        self.picker = Picker()
        self.filler = Filler(knowledge_base)
        self.sentimentalizer = Sentimentalizer()

    def run(self, jsonobj:json):
        
        ''' Extract the time where the json is occurred and match and update the resulting template'''

        user_id = jsonobj['user_id']

        # Comment matching and updating
        comment = self.picker.pick_comment(jsonobj)
        comment = self.filler.update_comment(comment, jsonobj, user_id)
        sentiment = self.sentimentalizer.add_emphasis(comment)

        output = {
            'comment': comment,
            'emphasis': sentiment,
            'startTime': jsonobj['start_time'],
            'endTime' : jsonobj['end_time'],
            'priority' : 4,
            'id' : user_id
        }
        return output



if __name__== "__main__":
    print("Hello")