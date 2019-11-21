import unittest
from src.Filler import Filler
import json
from pathlib import Path


class TestFiller(unittest.TestCase):

    def setUp(self):
        self.comment_filler = Filler()

    def test_update_comment1(self):
        details = {
            "team1" : "team A",
            "team2": "team B",
            "player1": "Ruicosta",
            "player2": "Ronaldo",
            "field_zone" : "middle",
            "subtype"  : "pass",
            "confidence" : 0.4
        }

        updated_comment = self.comment_filler.update_comment("{player1} from {team1} has passed to {player2} in the {field_zone}", details)

        assert updated_comment == "Ruicosta from team A has passed to Ronaldo in the middle"

    def test_update_comment2(self):
        with open(Path("CommentGenerator/tests/mock_assets/config1.json"),'r') as conf1:
            self.comment_filler.config = json.load(conf1)
        
        details = {
            "team1" : "team A",
            "player1": "Ruicosta",
            "subtype"  : "pass",
            "confidence" : 0.4
        }

        updated_comment = self.comment_filler.update_comment("{player1} has passed {simple_modifier}", details)

        assert updated_comment == "Ruicosta has passed good"
    
    def test_update_comment3(self):
        with open(Path("CommentGenerator/tests/mock_assets/config1.json"),'r') as conf2:
            self.comment_filler.config = json.load(conf2)
        
        details = {
            "team1" : "team B",
            "player1": "Ruicosta",
            "subtype"  : "pass",
            "confidence" : 0.4
        }

        updated_comment = self.comment_filler.update_comment("{player1} has passed {simple_modifier}", details)

        assert updated_comment == "Ruicosta has passed bad"

    def test_update_comment4(self):
        with open(Path("CommentGenerator/tests/mock_assets/config1.json"),'r') as conf2:
            self.comment_filler.config = json.load(conf2)
        
        details = {
            "team1" : "team A",
            "player1": "Ruicosta",
            "subtype"  : "pass",
            "confidence" : 0.4
        }

        updated_comment = self.comment_filler.update_comment("{player1} has passed the ball, {complex_modifier}", details)

        assert updated_comment == "Ruicosta has passed the ball, what a fantastic action!"