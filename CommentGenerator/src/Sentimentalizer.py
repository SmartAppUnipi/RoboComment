import nltk
import numpy
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class Sentimentalizer:

    def __init__(self):
        nltk.download('vader_lexicon')
        self.__analyzer = SentimentIntensityAnalyzer()

    def get_sentiment(self, comment):
        """
        Inference of the sentiment returned as
        positive: [0-1]
        neutral: [0-1]
        negative: [0-1]
        :param comment:
        :return:
        """
        results = self.__analyzer.polarity_scores(comment)
        # positive, neutral, negative
        values = [ results["pos"], results["neu"], results["neg"]]
        index = numpy.argmax(values)

        if index == 0:
            return "happy"
        elif index == 1:
            return "neutral"
        elif index == 2:
            return "angry"

