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

    def __init__(self, knowledge_base, user_id):
        self.user_id = user_id
        self.kb = knowledge_base
        self.user_lang = self.kb.get_user_language(self.user_id)
        self.automa = CommentAutomata()
        self.picker = Picker()
        self.filler = Filler(knowledge_base, self.user_id)
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
        comment = self.translator.get_translation(comment)
        # rephrase the comment
        # comment = self.rephraser.random_rephrase(comment)

        output = {
            'comment': comment,
            'language' : 'en',
            'voice': 'en-US-Wavenet-D',
            'emphasis': sentiment,
            'startTime': jsonobj['start_time'],
            'endTime': jsonobj['end_time'],
            'priority' : priority,
            'id' : self.user_id # it is better to use 'user_id' as key but the audio group looks for 'id'
        }
        return output

if __name__ == '__main__':
    test1 = {
    "type": "penalty",
    "match_id" : 42,
    "clip_uri" : "http://clip.of.the.match/juve/napoli",
    "user_id": 10,
    "time": 10,
    #"team": 5,
    "start_time": 10,
    "end_time" : 20
}
    picker = Picker()
    comment, placeholders, priority = picker.pick_comment(test1, "Hybrid comment")

    print("Comment:", comment)
    print("Placeholders:",placeholders)
    print("Priority", priority)


    filler  = Filler()
    filler.update_comment(comment,placeholders)