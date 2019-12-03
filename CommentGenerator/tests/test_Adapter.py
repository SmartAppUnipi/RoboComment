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

        


    def test_adapt_possession1(self):
        input1 = None
        with open("CommentGenerator/tests/mock_assets/elementary/possession/input_symbolic1.json", 'r') as mock_json:
            input1 = json.load(mock_json)
        jsonobj = self.adapter.adapt(input1)

        assert jsonobj['details']['subtype'] == 'possession'
        assert jsonobj['user_id'] == 10
        assert jsonobj["time"]["end"] == 20


    def test_adapt_intercept1(self):
        input1 = None
        with open("CommentGenerator/tests/mock_assets/elementary/intercept/input_symbolic1.json", 'r') as mock_json:
            input1 = json.load(mock_json)
        jsonobj = self.adapter.adapt(input1)

        assert jsonobj['details']['subtype'] == 'intercept'
        assert jsonobj['user_id'] == 10
        assert jsonobj["time"]["start"] == 10
