import unittest
from src.Picker import Picker


class TestPicker(unittest.TestCase):
    def setUp(self):
        self.comment_picker = Picker("assets/templates.json")

    def test_pick_comment1(self):
        jsonobj = {}
        comment = self.comment_picker.pick_comment(jsonobj)

        print(comment)