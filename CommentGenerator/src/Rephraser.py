from googletrans import Translator
import googletrans
from random import randrange


class Rephraser:

    def __init__(self, source):
        self.source = source
        self.safe_pivots = ['it', 'fr', 'iw', 'tr', 'he', 'el', 'sq', 'ru', 'ar', 'lb']

    def rephrase(self, comment, pivot):
        translator = Translator()
        for lang in pivot:
            comment = translator.translate(comment, dest=lang).text
        comment = translator.translate(comment, src=pivot[len(pivot) - 1], dest=self.source).text
        return comment

    def random_rephrase(self, comment, r=1, s=3, languages=list(googletrans.LANGUAGES.keys())):
        for i in range(s):
            pivot = []
            for j in range(r):
                idx = randrange(len(languages))
                pivot.append(languages.pop(idx))
            comment = self.rephrase(comment, pivot)
        return comment

    def safe_random_reprase(self, comment, r=1, s=3):
        return self.random_rephrase(comment, r, s, self.safe_pivots)
