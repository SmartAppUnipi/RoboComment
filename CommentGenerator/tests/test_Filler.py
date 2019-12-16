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

        comment = "it seems that {player_modifier1} {player1} , {team1} man,  has blocked what it looks like {player_modifier2} {player2}"
        placeholders = {'player1': 10, 'team1': 44, 'player2': 5}
    
        print("COMMENT:", comment)
        print("PLACEHOLDERS:", placeholders)
        user_id = 42
        filler = Filler(kb=self.kb,user_id = user_id)
        comment = filler.update_comment(comment, placeholders)
        print(comment)