import unittest
from src.Sentimentalizer import Sentimentalizer


class TestSentimentalizer(unittest.TestCase):

    def setUp(self):
        self.sentimentalizer = Sentimentalizer()

    def test_add_emphasis1(self):

        output_json = self.sentimentalizer.add_emphasis("Cristiano Ronaldo has made a goal,fantastic!")

        print(output_json)