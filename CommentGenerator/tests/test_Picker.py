import unittest
from src.Picker import Picker
import json


class TestPicker(unittest.TestCase):
    def setUp(self):
        self.comment_picker = Picker("assets/templates.json")
        with open("assets/input1.json",'r') as input1_json:
            self.input1 = json.load(input1_json)

    def test_pick_comment1(self):
        comment = self.comment_picker.pick_comment(self.input1)

        assert comment == "{player1} has made a {modifier} pass"
    
    def test_filter_comments_by_details1(self):
        details = {
            "team1" : "team A",
            "team2": "team B",
            "player1": "Ruicosta",
            "player2": "Ronaldo",
            "field-zone" : "middle",
            "subtype"  : "pass",
            "confidence" : 0.4
        }
        templates = self.comment_picker.filter_comments_by_details(details)

        assert templates[0] == "{player1} from {team1} has passed to {player2} in the {field-zone}"
    
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
      
        assert set(templates) == set(["{player1} has made a {modifier} pass","{player1} decides to pass the ball"])

    def test_filter_comments_by_details4(self):
        ''' test with poor information '''
        details = {
            "field-zone" : "middle",
            "subtype"  : "pass",
            "confidence" : 0.4
        }
        templates = self.comment_picker.filter_comments_by_details(details)

        assert templates == []