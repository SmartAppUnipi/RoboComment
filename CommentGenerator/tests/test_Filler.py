import unittest
from src.Filler import Filler
import json
import requests_mock
from tests.MockKnowledgeBase import MockKnowledgeBase


class TestFiller(unittest.TestCase):

    def setUp(self):
        self.kb = MockKnowledgeBase()
        self.comment_filler = Filler(self.kb)
    

    def test_update_comment1(self):
        details = {
            "team1" : 42,
            "team2": 7,
            "player1": 42,
            "player2": 7,
            "field_zone" : "middle",
            "subtype"  : "pass",
            "confidence" : 0.4
        }

        updated_comment = self.comment_filler.update_comment("{player1} from {team1} has passed to {player2} in the {field_zone}", details, 4)

        assert updated_comment == "Player42 from Team42 has passed to Player7 in the middle"

    def test_update_comment2(self):
        with open("CommentGenerator/tests/mock_assets/config1.json",'r') as conf1:
            self.comment_filler.config = json.load(conf1)
        
        details = {
            "team1" : 4,
            "player1": 42,
            "subtype"  : "pass",
            "confidence" : 0.4
        }

            
        updated_comment = self.comment_filler.update_comment("{player1} has passed {simple_modifier}", details, 4)

        assert updated_comment == "Player42 has passed good"
    
    def update_comment3(self): #TODO fix this
        with open("CommentGenerator/tests/mock_assets/config1.json",'r') as conf2:
            self.comment_filler.config = json.load(conf2)
        
        details = {
            "team1" : "team B",
            "player1": "Ruicosta",
            "subtype"  : "pass",
            "confidence" : 0.4
        }

        updated_comment = self.comment_filler.update_comment("{player1} has passed {simple_modifier}", details, 4)

        assert updated_comment == "Ruicosta has passed bad"

    def update_comment4(self): #TODO fix this
        with open("CommentGenerator/tests/mock_assets/config1.json",'r') as conf2:
            self.comment_filler.config = json.load(conf2)
        
        details = {
            "team1" : "team A",
            "player1": "Ruicosta",
            "subtype"  : "pass",
            "confidence" : 0.4
        }

        updated_comment = self.comment_filler.update_comment("{player1} has passed the ball, {complex_modifier}", details, 4)

        assert updated_comment == "Ruicosta has passed the ball, what a fantastic action!"
