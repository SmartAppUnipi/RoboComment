import unittest
from src.SentimentUpdater import SentimentUpdater


class TestSentimentUpdater(unittest.TestCase):

    def setUp(self):
        self.sentiment_updater = SentimentUpdater()

    def test_add_emphasis1(self):

        output_json = self.sentiment_updater.add_emphasis("Cristiano Ronaldo has made a goal,fantastic!")

        print(output_json)