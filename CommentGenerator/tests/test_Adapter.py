import json
import unittest
from src.Adapter import Adapter

class TestFiller(unittest.TestCase):
    def setUp(self):
        self.adapter = Adapter()

    def test_adapt_comment1(self):
        input1 = None
        with open("CommentGenerator/tests/mock_assets/elementary/pass/input_real1.json", 'r') as mock_json:
            input1 = json.load(mock_json)
        jsonobj = self.adapter.adapt(input1)

        assert jsonobj == "{player1} from {team1} has passed to {player2} in the {field_zone}"


