from googletrans import Translator
import googletrans
from random import randrange


class Rephraser:

    def __init__(self, source):
        self.source = source

    def rephrase(self, comment, pivot):
        translator = Translator()
        for lang in pivot:
            comment = translator.translate(comment, dest=lang).text
        comment = translator.translate(comment, src=pivot[len(pivot) - 1], dest=self.source).text
        return comment

    def random_rephrase(self, comment, k=2):
        pivot = []

        languages = list(googletrans.LANGUAGES.keys())
        for i in range(k):
            idx = randrange(len(languages))
            pivot.append(languages.pop(idx))

        return self.rephrase(comment, pivot)
