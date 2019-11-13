import unittest
from src.Filler import Filler
import json


class TestFiller(unittest.TestCase):

    def setUp(self):
        self.comment_filler = Filler()
        with open("assets/input1.json",'r') as input1_json:
            self.input1 = json.load(input1_json)


    def test_update_comment1(self):

        updated_comment = self.comment_filler.update_comment("{player1} has made a {modifier} pass", self.input1["details"])

        assert updated_comment == "Ruicosta has made a fantastic pass"

