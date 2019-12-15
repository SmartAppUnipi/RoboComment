import unittest
from src.Filler import Filler
import json
import requests_mock
from tests.MockKnowledgeBase import MockKB


class TestFiller(unittest.TestCase):

    def setUp(self):
        self.kb = MockKB()
        self.comment_filler = Filler(self.kb, user_id=7)
    
    def test_filler1(self):

        print("THIS TEST NEEDS TO BE IMPLEMENTED")
        raise NotImplementedError