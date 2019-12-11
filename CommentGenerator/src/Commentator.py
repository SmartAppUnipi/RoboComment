#from .Picker import Picker
import logging

try:
    from .Filler import Filler
    from .Sentimentalizer import Sentimentalizer
    from .Picker_grammar import Picker
    from .Automaton import CommentAutomata
except:
    from Filler import Filler
    from Sentimentalizer import Sentimentalizer
    from Picker_grammar import Picker
    from Automaton import CommentAutomata
import json

class Commentator:

    def __init__(self, knowledge_base, user_id):
        self.user_id = user_id
        self.kb = knowledge_base
        self.user_lang = self.kb.get_user_language(self.user_id)
        self.automa = CommentAutomata()
        self.picker = Picker(self.user_lang)
        self.filler = Filler(knowledge_base, user_id)
        self.sentimentalizer = Sentimentalizer()

    def run(self, jsonobj:json):
        
        ''' Extract the time where the json is occurred and match and update the resulting template'''
        # get next state
        state = self.automa.NextState()
        # create comment
        (comment, placeholders, priority) = self.picker.pick_comment(jsonobj, state)
        # update it with kb
        comment = self.filler.update_comment(comment, placeholders)
        # retrieve sentiment
        # TODO modify sentiment
        sentiment = self.sentimentalizer.add_emphasis(comment)

        # TODO modify priority
        output = {
            'comment': comment,
            'emphasis': sentiment,
            'startTime': jsonobj['start_time'],
            'endTime' : jsonobj['end_time'],
            'priority' : priority,
            'id' : self.user_id
        }
        return output

if __name__ == '__main__':

    comm = Commentator("", 1)
    comm.run({
    "type": "pass",
    "user_id": 10,
    "start_time": 10,
    "end_time" : 20,
    "player_active": {
      "id": {
        "value": 42,
        "confidence": 0.5
      },
      "team": {"value" : 42}
    },
    "player_passive": {
      "id": {
        "value": 41,
        "confidence": 0.5
      },
      "team": {"value" : 42}
    }
})
    comm.run({
    "type": "pass",
    "user_id": 10,
    "start_time": 10,
    "end_time" : 20,
    "player_active": {
      "id": {
        "value": 42,
        "confidence": 0.5
      },
      "team": {"value" : 42}
    },
    "player_passive": {
      "id": {
        "value": 41,
        "confidence": 0.5
      },
      "team": {"value" : 42}
    }
})