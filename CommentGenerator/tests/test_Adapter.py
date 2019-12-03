import json
import unittest
from src.Adapter import Adapter

class TestFiller(unittest.TestCase):
    def setUp(self):
        self.adapter = Adapter()

    def test_adapt_pass1(self):
        input1 = None
        with open("CommentGenerator/tests/mock_assets/elementary/pass/input_symbolic1.json", 'r') as mock_json:
            input1 = json.load(mock_json)
        jsonobj = self.adapter.adapt(input1)

        # jsonobj = json.dumps(jsonobj, sort_keys=False)
        json_expected = {
            "user_id": 10,
            "time": {"start": 10,
                     "end": 20
                     },
            "type": "elementary",
            "details":{
                "player1": 10,
                "team1": 42,
                "player2": 11,
                "team2": 42
            }
        }
        # Todo compare json in a unordered way
        #json_expected = json.dumps(json_expected, sort_keys=True)

        assert jsonobj['details']['player1'] == 42
        assert jsonobj['user_id'] == 10

"""
    def test_adapt_possession1(self):
        input1 = None
        with open("CommentGenerator/tests/mock_assets/elementary/possession/input_symbolic1.json", 'r') as mock_json:
            input1 = json.load(mock_json)
        jsonobj = self.adapter.adapt(input1)

        assert jsonobj == "{player1} from {team1} has passed to {player2} in the {field_zone}"


    def test_adapt_intercept1(self):
        input1 = None
        with open("CommentGenerator/tests/mock_assets/elementary/intercept/input_symbolic1.json", 'r') as mock_json:
            input1 = json.load(mock_json)
        jsonobj = self.adapter.adapt(input1)

        assert jsonobj == "{player1} from {team1} has passed to {player2} in the {field_zone}"
"""