import unittest
from src.Picker import Picker
import json


class TestPicker(unittest.TestCase):
    def setUp(self):
        self.comment_picker = Picker("assets/templates.json")
        
    def test_pick_comment1(self):
        input1 = None
        with open("tests/mock_assets/input1.json",'r') as mock_json:
            input1 = json.load(mock_json)
        comment = self.comment_picker.pick_comment(input1)

        assert comment == "{player1} from {team1} has passed to {player2} in the {field_zone}"        
    
    def test_pick_comment2(self):
        input2 = None
        with open("tests/mock_assets/input2.json",'r') as mock_json:
            input2 = json.load(mock_json)
        comment = self.comment_picker.pick_comment(input2)

        assert comment in ["{player1} decides to pass the ball","{player1} has made a {simple_modifier} pass"]
    
    def test_filter_comments_by_details1(self):
        details = {
            "team1" : "team A",
            "team2": "team B",
            "player1": "Ruicosta",
            "player2": "Ronaldo",
            "field_zone" : "middle",
            "subtype"  : "pass",
            "confidence" : 0.4
        }
        templates = self.comment_picker.filter_comments_by_details(details)

        assert templates[0] == "{player1} from {team1} has passed to {player2} in the {field_zone}"
    
    def test_filter_comments_by_details2(self):
        details = {
            "player2": "Ronaldo",
            "subtype"  : "pass",
            "confidence" : 0.4
        }
        templates = self.comment_picker.filter_comments_by_details(details)

        assert templates[0] == "{player2} has received a pass"
    
    def test_filter_comments_by_details3(self):
        details = {
            "player1": "Ronaldo",
            "subtype"  : "pass",
            "confidence" : 0.4
        }
        templates = self.comment_picker.filter_comments_by_details(details)
      
        assert set(templates) == set(["{player1} has made a {simple_modifier} pass","{player1} decides to pass the ball"])

    def test_filter_comments_by_details4(self):
        ''' test with poor information '''
        details = {
            "field_zone" : "middle",
            "subtype"  : "pass",
            "confidence" : 0.4
        }
        templates = self.comment_picker.filter_comments_by_details(details)

        assert templates == []