import unittest
from src.Sentimentalizer import Sentimentalizer
import nltk

class TestSentimentalizer(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        nltk.download('vader_lexicon')


    def setUp(self):
        self.sen = Sentimentalizer()

    def test_sentiment1(self):
        sentiment = self.sen.get_sentiment("The bad player is passing the ball")
        assert sentiment in set([1,3,5])