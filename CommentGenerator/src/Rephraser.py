from googletrans import Translator
import googletrans
from random import randrange

class Rephraser:

    def __init__(self, source, pivot):
        self.pivot = pivot
        self.source = source

    def rephrase(self, comment):
        translator = Translator()
        for lang in self.pivot:
            comment = translator.translate(comment, dest=lang).text
        comment = translator.translate(comment, src=self.pivot[len(self.pivot) - 1], dest=self.source).text
        return comment


if __name__ == '__main__':
    pivot = []

    languages = list(googletrans.LANGUAGES.keys())
    for k in range(2):
        idx = randrange(len(languages))
        pivot.append(languages.pop(idx))

    r = Rephraser(source='en', pivot=pivot)
    print([googletrans.LANGUAGES[x] for x in pivot])
    print(r.rephrase('A player from Napoli intercepts the ball.'))
