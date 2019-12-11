import logging

try:
    from .Filler import Filler
    from .Sentimentalizer import Sentimentalizer
    from .Picker_grammar import Picker
    from .Automaton import CommentAutomata
    from .Translate import Translate
except:
    from Filler import Filler
    from Sentimentalizer import Sentimentalizer
    from Picker_grammar import Picker
    from Automaton import CommentAutomata
    from Translate import Translate
import json

class Commentator:

    def __init__(self, knowledge_base, user_id):
        self.user_id = user_id
        self.kb = knowledge_base
        #self.user_lang = self.kb.get_user_language(self.user_id)
        self.automa = CommentAutomata()
        self.picker = Picker()
        self.filler = Filler(knowledge_base, self.user_id)
        #self.translator = Translate(self.user_lang)
        self.translator = Translate('it')
        self.sentimentalizer = Sentimentalizer()

    def run(self, jsonobj:json):
        
        ''' Extract the time where the json is occurred and match and update the resulting template'''
        # get next state
        state = self.automa.NextState()
        # create comment
        (comment, placeholders, priority) = self.picker.pick_comment(jsonobj, state)
        # update it with kb
        #comment = self.filler.update_comment(comment, placeholders)
        # retrieve sentiment
        sentiment = self.sentimentalizer.get_sentiment(comment)
        # translate in the correct language
        comment = self.translator.get_translation(comment)
        print(comment)

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