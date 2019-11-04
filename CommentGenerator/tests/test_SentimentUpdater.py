import unittest
from src.SentimentUpdater import SentimentUpdater

def test_add_emphasis1():

    su = SentimentUpdater()
    output_json = su.add_emphasis("Cristiano Ronaldo has made a goal,fantastic!")

    print(output_json)