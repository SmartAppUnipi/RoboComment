import unittest
from src.Filler import Filler
import json
import requests_mock
from tests.MockKnowledgeBase import MockKB


class TestFiller(unittest.TestCase):

    def setUp(self):
        self.kb = MockKB()
        self.comment_filler = Filler(self.kb, user_id=42, match_id = 42)
    
    def test_filler1(self):

        comment = "it seems that {player_modifier1} {player1} , {team1} man,  has blocked what it looks like {player_modifier2} {player2}"
        placeholders = {'player1': 7, 'team1': 7, 'player2': 41}
          
        comment = self.comment_filler.update_comment(comment, placeholders)
        print(comment)