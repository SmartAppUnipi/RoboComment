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

        assert comment == "{subject} has made a {modifier} pass"