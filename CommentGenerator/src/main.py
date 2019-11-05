from .Picker import Picker
from .Filler import Filler
from .Sentimentalizer import Sentimentalizer
import json


class Commnter:

    def __init__(self, config, template):
        self.config = config
        self.template = template

    def run(self, jsonobj):
        # TODO capire come avviena la comunicazione tra i gruppi
        # se siamo noi a dover chidere in poll nuove azioni
        # se è il gruppo symbolic ad inviarci azioni
        # se è il gruppo audio a richiedere nuovi commenti <- ci piace

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
