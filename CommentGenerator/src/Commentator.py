import logging

try:
    from .Filler import Filler
    from .Sentimentalizer import Sentimentalizer
    from .Picker_grammar import Picker
    from .Automaton import CommentAutomata
    from .Translate import Translate
    from .Rephraser import Rephraser
except:
    from .Filler import Filler
    from .Sentimentalizer import Sentimentalizer
    from .Picker_grammar import Picker
    from .Automaton import CommentAutomata
    from .Translate import Translate
    from .Rephraser import Rephraser
import json

class Commentator:

    def __init__(self, knowledge_base, user_id, match_id):
        self.user_id = user_id
        self.kb = knowledge_base
        self.user_lang = self.kb.get_user_language(self.user_id)
        self.automa = CommentAutomata()
        self.picker = Picker()
        self.filler = Filler(knowledge_base, self.user_id, match_id)
        self.translator = Translate(self.user_lang)
        self.rephraser = Rephraser(source=self.user_lang)
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
        sentiment = self.sentimentalizer.get_sentiment(comment)
        # translate in the correct language
        # comment = self.translator.get_translation(comment)
        # rephrase the comment
        # comment = self.rephraser.safe_random_reprase(comment)

        output = {
            'comment': comment,
            'language' : self.user_lang,
            'voice': 'en-US-Wavenet-D',
            'emphasis': sentiment,
            'startTime': jsonobj['start_time'],
            'endTime': jsonobj['end_time'],
            'priority' : priority,
            'id' : self.user_id # it is better to use 'user_id' as key but the audio group looks for 'id'
        }
        return output
