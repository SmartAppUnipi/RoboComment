import unittest
from src.Filler import Filler
import json
import requests_mock


class TestFiller(unittest.TestCase):

    def setUp(self):
        self.kb = MockKB()
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

        updated_comment = self.comment_filler.update_comment("{player1} from {team1} has passed to {player2} in the {field_zone}", details)

        assert updated_comment == "Pippo from TeamPippo has passed to Topolino in the middle"

    def test_update_comment2(self):
        with open("CommentGenerator/tests/mock_assets/config1.json",'r') as conf1:
            self.comment_filler.config = json.load(conf1)
        
        details = {
            "team1" : 42,
            "player1": 42,
            "subtype"  : "pass",
            "confidence" : 0.4
        }

            
        updated_comment = self.comment_filler.update_comment("{player1} has passed {simple_modifier}", details)

        assert updated_comment == "Pippo has passed bad"
    
    def update_comment3(self): #TODO fix this
        with open("CommentGenerator/tests/mock_assets/config1.json",'r') as conf2:
            self.comment_filler.config = json.load(conf2)
        
        details = {
            "team1" : "team B",
            "player1": "Ruicosta",
            "subtype"  : "pass",
            "confidence" : 0.4
        }

        updated_comment = self.comment_filler.update_comment("{player1} has passed {simple_modifier}", details)

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

        updated_comment = self.comment_filler.update_comment("{player1} has passed the ball, {complex_modifier}", details)

        assert updated_comment == "Ruicosta has passed the ball, what a fantastic action!"



class MockKB():
    def __init__(self):
        pass

    def get_player(self, player_id):
        if player_id == 42:
            return "Pippo"
        elif player_id == 7:
            return "Topolino"
        else:
            return "undefined"
    
    def get_team(self, team_id):
        if team_id == 42:
            return "TeamPippo"
        elif team_id == 7:
            return "TeamTopolino"
        else:
            return "undefined"